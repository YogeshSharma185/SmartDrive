from stable_baselines3 import PPO
from src.game.driving_rl_wrapper import DrivingRLWrapper
import pygame
import sys

def main():
    env = DrivingRLWrapper(render_mode=True)
    model = PPO.load("ppo_speak2steer")

    obs, _ = env.reset()
    clock = pygame.time.Clock()

    pygame.init()
    screen = pygame.display.set_mode((800, 600))  # adjust if needed
    pygame.display.set_caption("SmartDrive - Where Manual Thrill meets AI Skills")
    font = pygame.font.SysFont(None, 30)

    last_reward = 0
    total_reward = 0
    step_count = 0

    while True:
        # Predict action from model
        action, _ = model.predict(obs)
        obs, reward, done, _, info = env.step(action)
        env.render()

        # Reward tracking
        last_reward = reward
        total_reward += reward
        step_count += 1

        # Display info (Speed, Score, Reward)
        speed = info.get("speed", 0)
        coins = info.get("coins_collected", 0)

        info_surface = pygame.Surface((800, 50))
        info_surface.fill((30, 30, 30))
        txt = font.render(
            f"AI Action: {['Left', 'Stay', 'Right', 'SpeedUp', 'SlowDown'][action]} | "
            f"Speed: {speed} | Coins: {coins} | Last Reward: {last_reward:.2f} | Total Reward: {total_reward:.2f}",
            True, (255, 255, 255))
        info_surface.blit(txt, (10, 10))
        screen.blit(info_surface, (0, 0))
        pygame.display.update()

        if done:
            font_big = pygame.font.SysFont(None, 50)
            text1 = font_big.render("Game Over!", True, (255, 0, 0))
            text2 = font_big.render("Press R to restart, ESC to quit", True, (255, 255, 255))

            screen.fill((0, 0, 0))
            screen.blit(text1, text1.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 30)))
            screen.blit(text2, text2.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 30)))
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
                            total_reward = 0
                            step_count = 0
                            waiting = False
                        elif event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()

        clock.tick(60)

if __name__ == "__main__":
    main()
