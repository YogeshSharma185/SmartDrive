from stable_baselines3 import PPO
from src.game.driving_rl_wrapper import DrivingRLWrapper
from src.game.driving_env import CAR_WIDTH_PX, CAR_HEIGHT_PX
import gymnasium as gym
import pygame
import numpy as np


class SaferDrivingWrapper(gym.Wrapper):
    def __init__(self, env):
        super().__init__(env)

    def step(self, action):
        obs, reward, terminated, truncated, info = self.env.step(action)
        done = terminated or truncated

        custom_reward = 0

        # Extract car and obstacles
        player_x = self.env.env.player_x
        player_y = self.env.env.player_y
        player_rect = pygame.Rect(player_x, player_y, CAR_WIDTH_PX, CAR_HEIGHT_PX)

        # STRONG PENALTY on crash
        if done:
            custom_reward = -1000
            return obs, custom_reward, terminated, truncated, info

        # Small reward for surviving
        custom_reward += 1

        # Reward for fuel and coin collection already handled in env.step()
        # Now, ADD stronger proximity penalties

        SAFE_DISTANCE_Y = 180  # pixels
        for obs_car in self.env.env.obstacles:
            obs_rect = pygame.Rect(obs_car['x'], obs_car['y'], CAR_WIDTH_PX, CAR_HEIGHT_PX)

            dx = abs(obs_rect.centerx - player_rect.centerx)
            dy = obs_rect.top - player_rect.bottom

            same_lane = dx < CAR_WIDTH_PX // 2

            # Apply exponential proximity penalty
            if same_lane and 0 < dy < SAFE_DISTANCE_Y:
                # The closer, the harsher
                proximity_penalty = 50 * np.exp(-dy / 40)
                custom_reward -= proximity_penalty

            elif same_lane and dy >= SAFE_DISTANCE_Y:
                # Mild disincentive to stay long in risky lane
                custom_reward -= 2

        return obs, custom_reward, terminated, truncated, info


def main():
    base_env = DrivingRLWrapper(render_mode=False)
    wrapped_env = SaferDrivingWrapper(base_env)

    model = PPO("CnnPolicy", wrapped_env, verbose=1)
    model.learn(total_timesteps=150_000)
    model.save("ppo_speak2steer")

    wrapped_env.close()


if __name__ == "__main__":
    main()
