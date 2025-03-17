import pygame

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
GRAVITY = 0.5

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer Game")

# Load sprite sheet
sprite_sheet = pygame.image.load("assets/sprites.png")

# Extract correct frames based on the updated sprite sheet
frame_width, frame_height = 64, 64  # Adjust these if needed
running_frames = [sprite_sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height)) for i in range(6)]
jump_up_frame = sprite_sheet.subsurface(pygame.Rect(0, frame_height, frame_width, frame_height))
jump_down_frame = sprite_sheet.subsurface(pygame.Rect(frame_width, frame_height, frame_width, frame_height))

# Player settings
player_x, player_y = 100, HEIGHT - 150
player_speed = 5
jump_power = -10
player_velocity_y = 0
on_ground = False
frame_index = 0
animation_timer = 0

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
    moving = False
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
        moving = True
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
        moving = True
    if keys[pygame.K_SPACE] and on_ground:
        player_velocity_y = jump_power
        on_ground = False
    
    # Apply gravity
    player_velocity_y += GRAVITY
    player_y += player_velocity_y
    
    # Collision detection
    player_rect = pygame.Rect(player_x, player_y, frame_width, frame_height)
    on_ground = False
    for platform in platforms:
        if player_rect.colliderect(platform) and player_velocity_y > 0:
            player_y = platform.top - frame_height
            player_velocity_y = 0
            on_ground = True
    
    # Check if player falls off the screen
    if player_y > HEIGHT:
        print("You died!")
        running = False
    
    # Update animation
    if on_ground:
        if moving:
            animation_timer += 1
            if animation_timer % 5 == 0:
                frame_index = (frame_index + 1) % len(running_frames)
            current_frame = running_frames[frame_index]
        else:
            current_frame = running_frames[0]
    else:
        current_frame = jump_up_frame if player_velocity_y < 0 else jump_down_frame
    
    # Draw player
    screen.blit(current_frame, (player_x, player_y))
    
    # Draw platforms
    for platform in platforms:
        pygame.draw.rect(screen, (0, 255, 0), platform)
    
    # Update display
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
