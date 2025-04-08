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
                # Switch era when F is pressed
                world.current_era = "future" if world.current_era == "past" else "past"
    
    # Get player input
    keys = pygame.key.get_pressed()
    player.handle_input(keys)
    
    # Update player and world
    player.update(dt, world, world.current_era)
    world.update(player.rect.x)
    
    # Update camera to follow player
    target_x = player.rect.x - screen.get_width() // 2
    camera_x += (target_x - camera_x) * 0.1  # Smooth camera movement
    
    # Clear screen
    screen.fill((0, 0, 0))
    
    # Draw background based on era
    if world.current_era == "past":
        bg = backgrounds["past"]
    else:
        bg = backgrounds["future"]
    
    # Calculate how many background tiles we need to cover the screen
    bg_width = bg.get_width()
    num_tiles = (screen.get_width() // bg_width) + 2  # +2 to ensure we have enough tiles
    
    # Draw the background tiles
    for i in range(num_tiles):
        x_pos = (i * bg_width) - (camera_x // 2) % bg_width
        screen.blit(bg, (x_pos, 0))
    
    # Draw world
    world.draw(screen, camera_x)
    
    # Draw player
    player.draw(screen, camera_x)
    
    # Update display
    pygame.display.flip()

pygame.quit()
sys.exit()
