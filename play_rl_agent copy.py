from stable_baselines3 import PPO
from src.game.driving_rl_wrapper import DrivingRLWrapper
import pygame
import sys

def main():
    env = DrivingRLWrapper(render_mode=True)
    model = PPO.load("ppo_speak2steer")

    obs, _ = env.reset()
    clock = pygame.time.Clock()

    # Manually get screen from Pygame (since env.game not available)
    pygame.init()
    screen = pygame.display.set_mode((800, 600))  # adjust to your game's resolution
    pygame.display.set_caption("SmartDrive - Where Manual Thrill meets AI Skills")

    while True:
        action, _ = model.predict(obs)
        obs, reward, done, _, _ = env.step(action)

        env.render()

        if done:
            # Show Game Over centered
            font = pygame.font.SysFont(None, 50)
            text1 = font.render("Game Over!", True, (255, 0, 0))
            text2 = font.render("Press R to restart, ESC to quit", True, (255, 255, 255))

            screen.fill((0, 0, 0))
            screen.blit(text1, text1.get_rect(center=(screen.get_width()//2, screen.get_height()//2 - 30)))
            screen.blit(text2, text2.get_rect(center=(screen.get_width()//2, screen.get_height()//2 + 30)))
            pygame.display.flip()

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            obs, _ = env.reset()
                            waiting = False
                        elif event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()

        clock.tick(60)

if __name__ == "__main__":
    main()
