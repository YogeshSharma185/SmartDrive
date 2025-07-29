import gymnasium as gym
from gymnasium import spaces
import numpy as np
import pygame
import cv2

# Importing your game environment
from src.game.driving_env import DrivingEnv


class DrivingRLWrapper(gym.Env):
    def __init__(self, render_mode=False):
        super(DrivingRLWrapper, self).__init__()
        pygame.init()

        self.render_mode = render_mode
        self.screen = pygame.display.set_mode((800, 600)) if render_mode else pygame.Surface((800, 600))
        self.env = DrivingEnv(self.screen)

        # Define action and observation space
        self.action_space = spaces.Discrete(3)  # [0: left, 1: stay, 2: right]
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

    # List of all keys that driving_env.update() might check
        all_keys = [
            pygame.K_LEFT,
            pygame.K_RIGHT,
            pygame.K_UP,
            pygame.K_DOWN,
            pygame.K_SPACE
        ]

    # Initialize all keys to False
        keys = {k: False for k in all_keys}

    # Only enable the selected action key
        if action == 0:
            keys[pygame.K_LEFT] = True
        elif action == 2:
            keys[pygame.K_RIGHT] = True
    # You can map more actions if needed

        crashed = self.env.update(keys)

        reward = 0
        done = False

        if crashed:
            reward = -1000
            done = True
        else:
            reward = 1 + self.env.speed * 0.05

        obs = self.get_obs()
        return obs, reward, done, False, {}



    def render(self):
        if self.render_mode:
            self.env.render()
            pygame.display.flip()

    def close(self):
        pygame.quit()
