import sys
import pygame
from player import Player
from world import World
from assets import load_assets

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Era Switch Platformer")

clock = pygame.time.Clock()

assets = load_assets()

current_era = "past"
# Adjust player spawn: spawn higher so the player falls onto the platforms.
player = Player(100, SCREEN_HEIGHT - 300, assets)
world = World(world_width=3000, screen_height=SCREEN_HEIGHT, assets=assets)

camera_x = 0

running = True
while running:
    dt = clock.tick(60) / 1000.0
    f_pressed = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                f_pressed = True
                
    keys = pygame.key.get_pressed()
    player.handle_input(keys)
    player.update(dt, world, current_era)
    
    if f_pressed:
        for sw in world.switches:
            if player.rect.colliderect(sw):
                current_era = "future" if current_era == "past" else "past"
                print("Era switched to", current_era)
                break
    
    camera_x = player.rect.x - SCREEN_WIDTH // 2
    if camera_x < 0:
        camera_x = 0
    
    screen.blit(assets["background"], (0, 0))
    world.draw(screen, camera_x, current_era)
    player.draw(screen, camera_x)
    
    pygame.display.flip()

pygame.quit()
sys.exit()
