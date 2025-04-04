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

# Initialize current background
current_bg = backgrounds["past"]

# Initialize game objects
player = Player(100, SCREEN_HEIGHT - 200, None)  # None for assets since we're not using them yet
world = World(WORLD_WIDTH, SCREEN_HEIGHT, None)  # None for assets since we're not using them yet

camera_x = 0

# Game loop
running = True
while running:
    dt = clock.tick(60) / 1000.0  # Get delta time in seconds
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                # Toggle era when F is pressed
                world.current_era = "future" if world.current_era == "past" else "past"
                # Update background based on era
                current_bg = backgrounds["future"] if world.current_era == "future" else backgrounds["past"]

    # Update
    keys = pygame.key.get_pressed()
    player.handle_input(keys)
    player.update(dt, world, world.current_era)
    world.update(player.rect.x)

    # Draw
    screen.fill((0, 0, 0))  # Clear screen
    
    # Draw background with offset for future era
    if world.current_era == "future":
        screen.blit(current_bg, (0, 2))  # Move future background down by 2 pixels
    else:
        screen.blit(current_bg, (0, 0))
    
    # Draw world (platforms, pillars, switches)
    world.draw(screen, camera_x)
    
    # Draw player
    player.draw(screen, camera_x)
    
    pygame.display.flip()

pygame.quit()
sys.exit()
