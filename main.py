# main.py
import sys
import pygame
from player import Player
from world import World

pygame.init()

# Display setup
SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Era Switch Platformer")

# Backgrounds
backgrounds = {
    "past":   pygame.image.load("assets/game_elements/bg_autumn.png").convert(),
    "future": pygame.image.load("assets/game_elements/bg_green.png").convert()
}
SCREEN_WIDTH  = backgrounds["past"].get_width()
SCREEN_HEIGHT = backgrounds["past"].get_height()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

WORLD_WIDTH = 3000
clock = pygame.time.Clock()

player = Player(100, SCREEN_HEIGHT - 200, None)
world  = World(WORLD_WIDTH, SCREEN_HEIGHT, None)
camera_x = 0

running = True
while running:
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
            world.current_era = "future" if world.current_era == "past" else "past"

    keys = pygame.key.get_pressed()
    player.handle_input(keys)
    player.update(dt, world, world.current_era)
    world.update(player.rect.x)

    # Smooth camera
    target_x = player.rect.x - screen.get_width() // 2
    camera_x += (target_x - camera_x) * 0.1

    # Draw
    screen.fill((0, 0, 0))
    bg = backgrounds[world.current_era]
    bg_w = bg.get_width()
    for i in range((screen.get_width() // bg_w) + 2):
        x_pos = (i * bg_w) - (camera_x // 2) % bg_w
        screen.blit(bg, (x_pos, 0))

    world.draw(screen, camera_x)
    player.draw(screen, camera_x)
    pygame.display.flip()

pygame.quit()
sys.exit()
