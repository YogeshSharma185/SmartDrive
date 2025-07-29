import gymnasium as gym
from gymnasium import spaces
import numpy as np
import pygame
import cv2

from src.game.driving_env import DrivingEnv


class DrivingRLWrapper(gym.Env):
    def __init__(self, render_mode=False):
        super(DrivingRLWrapper, self).__init__()
        pygame.init()

        self.render_mode = render_mode
        self.screen = pygame.display.set_mode((800, 600)) if render_mode else pygame.Surface((800, 600))
        self.env = DrivingEnv(self.screen)

        self.action_space = spaces.Discrete(5)  # 0: Left, 1: Stay, 2: Right, 3: Speed Up, 4: Slow Down
        self.observation_space = spaces.Box(low=0, high=255, shape=(84, 84, 3), dtype=np.uint8)

    def get_obs(self):
        surface = pygame.display.get_surface() if self.render_mode else self.screen
        raw_image = pygame.surfarray.array3d(surface)
        image = cv2.resize(np.transpose(raw_image, (1, 0, 2)), (84, 84))
        return image

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.env.reset()
        obs = self.get_obs()
        return obs, {}

    def step(self, action):
        action = int(action)

        # Simulate keypresses
        keys = {
            pygame.K_LEFT: False,
            pygame.K_RIGHT: False,
            pygame.K_UP: False,
            pygame.K_DOWN: False,
            pygame.K_SPACE: False
        }

        if action == 0:
            keys[pygame.K_LEFT] = True
        elif action == 2:
            keys[pygame.K_RIGHT] = True
        elif action == 3:
            keys[pygame.K_UP] = True
        elif action == 4:
            keys[pygame.K_DOWN] = True

        crashed = self.env.update(keys)

        reward = 0
        done = False

        if crashed:
            reward = -1000
            done = True
        else:
            reward += 1 + self.env.speed * 0.05

            # Attempt very simple danger detection using raw image
            obs = self.get_obs()
            danger_zone = obs[50:84, 20:64]  # bottom center zone
            avg_red = np.mean(danger_zone[:, :, 0])

            if avg_red > 180:  # red could mean human or hazard
                reward -= 10  # possible human/car ahead
            else:
                avg_yellow = np.mean(danger_zone[:, :, 1])  # coins/fuel often yellow
                if avg_yellow > 150:
                    reward += 5  # maybe picked up something good

        obs = self.get_obs()
        return obs, reward, done, False, {}

    def render(self):
        if self.render_mode:
            self.env.render()
            pygame.display.flip()

    def close(self):
        pygame.quit()
