# Main
import pygame

import pygame

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GRAVITY = 0.5

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer Game")

# Player settings
player_size = (50, 50)
player_x, player_y = 100, HEIGHT - 150
player_speed = 5
jump_power = -10
player_velocity_y = 0
on_ground = False

# Platform settings
platforms = [
    pygame.Rect(100, HEIGHT - 100, 200, 20),
    pygame.Rect(400, HEIGHT - 200, 200, 20),
    pygame.Rect(600, HEIGHT - 300, 200, 20)
]

# Game loop
running = True
clock = pygame.time.Clock()
while running:
    screen.fill(WHITE)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_SPACE] and on_ground:
        player_velocity_y = jump_power
        on_ground = False
    
    # Apply gravity
    player_velocity_y += GRAVITY
    player_y += player_velocity_y
    
    # Collision detection
    player_rect = pygame.Rect(player_x, player_y, *player_size)
    on_ground = False
    for platform in platforms:
        if player_rect.colliderect(platform) and player_velocity_y > 0:
            player_y = platform.top - player_size[1]
            player_velocity_y = 0
            on_ground = True
    
    # Prevent falling through the floor
    if player_y + player_size[1] >= HEIGHT:
        player_y = HEIGHT - player_size[1]
        player_velocity_y = 0
        on_ground = True
    
    # Draw player
    pygame.draw.rect(screen, BLUE, (player_x, player_y, *player_size))
    
    # Draw platforms
    for platform in platforms:
        pygame.draw.rect(screen, GREEN, platform)
    
    # Update display
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
