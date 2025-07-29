import pygame
import sys
import subprocess
import math
import time

pygame.init()

# Screen setup
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SmartDrive - Self Driving Car")

# Fonts
title_font = pygame.font.SysFont("arialblack", 58)
slogan_font = pygame.font.SysFont("verdana", 26)
desc_font = pygame.font.SysFont("arial", 20)
button_font = pygame.font.SysFont("arial", 26)
copyright_font = pygame.font.SysFont("arial", 16)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (10, 140, 255)
GREEN = (34, 200, 94)
BG_COLOR = (10, 10, 30)
WAVE_COLOR = (40, 40, 90)

# Button setup
manual_btn = pygame.Rect(WIDTH // 2 - 140, 340, 280, 50)
auto_btn = pygame.Rect(WIDTH // 2 - 140, 420, 280, 50)

# Animation
def draw_animated_background():
    screen.fill(BG_COLOR)
    for y in range(0, HEIGHT, 25):
        wave_y = y + math.sin((time.time() * 2 + y / 30.0)) * 10
        pygame.draw.line(screen, WAVE_COLOR, (0, wave_y), (WIDTH, wave_y), 1)

def draw_glass_panel():
    glass = pygame.Surface((700, 400), pygame.SRCALPHA)
    glass.fill((255, 255, 255, 25))
    screen.blit(glass, (WIDTH // 2 - 350, 100))
    pygame.draw.rect(screen, (255, 255, 255, 80), (WIDTH // 2 - 350, 100, 700, 400), 2)

def draw_ui():
    draw_animated_background()
    draw_glass_panel()

    # Logo Title
    title_surface = title_font.render("SmartDrive", True, WHITE)
    screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, 120))

    # Slogan
    slogan = slogan_font.render("Where Manual Thrill meets AI Skills", True, (180, 180, 180))
    screen.blit(slogan, (WIDTH // 2 - slogan.get_width() // 2, 190))

    # Description
    desc1 = desc_font.render("• Manual Mode: Control using keyboard arrows.", True, WHITE)
    desc2 = desc_font.render("• Auto Mode: Watch AI drive using Reinforcement Learning.", True, WHITE)
    screen.blit(desc1, (WIDTH // 2 - desc1.get_width() // 2, 240))
    screen.blit(desc2, (WIDTH // 2 - desc2.get_width() // 2, 265))

    # Manual Mode Button
    pygame.draw.rect(screen, BLUE, manual_btn, border_radius=12)
    text1 = button_font.render("Play - Manual Mode", True, WHITE)
    screen.blit(text1, (manual_btn.centerx - text1.get_width() // 2, manual_btn.centery - 15))

    # Auto Mode Button
    pygame.draw.rect(screen, GREEN, auto_btn, border_radius=12)
    text2 = button_font.render("Run - AI Agent Mode", True, WHITE)
    screen.blit(text2, (auto_btn.centerx - text2.get_width() // 2, auto_btn.centery - 15))

    # Copyright footer
    copyright_text = copyright_font.render("© 2025 Yogesh Sharma. All rights reserved.", True, (160, 160, 160))
    screen.blit(copyright_text, (WIDTH // 2 - copyright_text.get_width() // 2, HEIGHT - 30))

    pygame.display.flip()

def main():
    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(60)
        draw_ui()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                python_exec = sys.executable
                if manual_btn.collidepoint(event.pos):
                    pygame.quit()
                    subprocess.call([python_exec, "main.py"])
                elif auto_btn.collidepoint(event.pos):
                    pygame.quit()
                    subprocess.call([python_exec, "play_rl_agent.py"])

if __name__ == "__main__":
    main()
