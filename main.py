import sys
import pygame
from player import Player
from world import World

pygame.init()

# Set up initial display mode
SCREEN_WIDTH = 800  # Temporary size
SCREEN_HEIGHT = 600  # Temporary size
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Era Switch Platformer")

# Now load background images
backgrounds = {
    "past": pygame.image.load("assets/game_elements/bg_autumn.png").convert(),
    "future": pygame.image.load("assets/game_elements/bg_green.png").convert()
}

# Update screen size to match background
SCREEN_WIDTH = backgrounds["past"].get_width()
SCREEN_HEIGHT = backgrounds["past"].get_height()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

WORLD_WIDTH = 3000
clock = pygame.time.Clock()

current_era = "past"
# Adjust player spawn: spawn higher so the player falls onto the platforms.
player = Player(100, SCREEN_HEIGHT - 200, None)  # None for assets since we're not using them yet
world = World(WORLD_WIDTH, SCREEN_HEIGHT, None)  # None for assets since we're not using them yet

camera_x = 0

running = True
while running:
    dt = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                # Check for era switch collision
                for switch in world.switches:
                    if player.rect.colliderect(switch):
                        current_era = "future" if current_era == "past" else "past"
                        print(f"Switched to {current_era} era")
                        break
    
    keys = pygame.key.get_pressed()
    player.handle_input(keys)
    player.update(dt, world, current_era)
    
    # Update world to generate new platforms
    world.update(player.rect.x)
    
    # Update camera position
    camera_x = player.rect.x - SCREEN_WIDTH // 2
    camera_x = max(0, min(camera_x, WORLD_WIDTH - SCREEN_WIDTH))
    
    # Clear screen and draw background
    screen.fill((0, 0, 0))  # Clear with black first
    # Draw future background slightly lower to fix alignment
    if current_era == "future":
        screen.blit(backgrounds[current_era], (0, 2))
    else:
        screen.blit(backgrounds[current_era], (0, 0))
    
    world.draw(screen, camera_x, current_era)
    player.draw(screen, camera_x)
    
    pygame.display.flip()

pygame.quit()
sys.exit()
