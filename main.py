import pygame
import sys
from src.game.driving_env import DrivingEnv

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("SmartDrive - Where Manual Thrill meets AI Skills")
clock = pygame.time.Clock()

env = DrivingEnv(screen)
font_big = pygame.font.SysFont(None, 50)
font_small = pygame.font.SysFont(None, 32)

def show_restart_popup():
    # Fill black background after crash
    screen.fill((0, 0, 0))

    text1 = font_big.render("Game Over!", True, (255, 0, 0))
    text2 = font_small.render("Press R to Restart, ESC to Quit", True, (255, 255, 255))

    screen.blit(text1, (SCREEN_WIDTH//2 - text1.get_width()//2, SCREEN_HEIGHT//2 - 40))
    screen.blit(text2, (SCREEN_WIDTH//2 - text2.get_width()//2, SCREEN_HEIGHT//2 + 10))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                    env.reset()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()

def main():
    while True:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        screen.fill((0, 150, 0))  # Normal green background
        game_over = env.update(keys)
        env.render()
        pygame.display.flip()

        if game_over:
            show_restart_popup()

        clock.tick(60)

if __name__ == "__main__":
    main()
