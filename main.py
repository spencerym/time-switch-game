import pygame

# Initialize pygame
pygame.init()

WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
GRAVITY = 0.5

#Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer Game")

#Sprite guy
running_sprite_sheet = pygame.image.load("assets/FreeCatCharacterAnimations/2_Cat_Run-Sheet.png")
idle_sprite_sheet = pygame.image.load("assets/FreeCatCharacterAnimations/1_Cat_Idle-Sheet.png")
sprite_sheet = pygame.image.load("assets/sprites.png")
#idle_sprite_sheet = pygame.transform.scale(idle_sprite_sheet, (100, 100))

# Right frames animation?
frame_width_run, frame_height_run = 20, 20
frame_width_idle, frame_height_idle = 20, 20
frame_width, frame_height = 500/6, 100
running_frames = [running_sprite_sheet.subsurface(pygame.Rect(i * frame_width_run, 0, frame_width_run, frame_height_run)) for i in range(1, 10)]
idle_frames = [idle_sprite_sheet.subsurface(pygame.Rect(x * frame_width_idle, 0, frame_width_idle, frame_height_idle)) for x in range(8)]

jump_up_frame = sprite_sheet.subsurface(pygame.Rect(0, 163, frame_width, frame_height))
jump_down_frame = sprite_sheet.subsurface(pygame.Rect(frame_width, 163, frame_width, frame_height))

# Player stats
player_x, player_y = 100, HEIGHT - 150
player_speed = 5
jump_power = -10
player_velocity_y = 0
on_ground = False
frame_index = 0
idle_index = 0
animation_timer = 0
idle_timer = 0
facing_right = True

# Platform stuf
platforms = [
    pygame.Rect(100, HEIGHT - 100, 200, 20),
    pygame.Rect(400, HEIGHT - 200, 200, 20),
    pygame.Rect(600, HEIGHT - 300, 200, 20)
]

#Clock thing
running = True
clock = pygame.time.Clock()
while running:
    screen.fill(WHITE)
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Player movement
    keys = pygame.key.get_pressed()
    moving = False
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
        moving = True
        facing_right = False
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
        moving = True
        facing_right = True
    if keys[pygame.K_SPACE] and on_ground:
        player_velocity_y = jump_power
        on_ground = False
    
    #gravity
    player_velocity_y += GRAVITY
    player_y += player_velocity_y
    
    # Collision
    player_rect = pygame.Rect(player_x, player_y, frame_width_run, frame_height_run)
    for platform in platforms:
        if player_rect.colliderect(platform) and player_velocity_y > 0:
            player_y = platform.top - frame_height_run
            player_velocity_y = 0
            on_ground = True
    
    # Lose
    if player_y > HEIGHT:
        print("You died!")
        running = False
    
    #  animation
    if on_ground:
        if moving:
            animation_timer += 1
            if animation_timer % 3 == 0:
                frame_index = (frame_index + 1) % len(running_frames)
            current_frame = running_frames[frame_index]
        else:
            idle_timer += 1
            if idle_timer % 10 == 0:
                idle_index = (idle_index + 1) % len(idle_frames)
            current_frame = idle_frames[idle_index]
    else:
        current_frame = jump_up_frame if player_velocity_y < 0 else jump_down_frame
    
    if not facing_right:
        current_frame = pygame.transform.flip(current_frame, True, False)
    
    # Draw player
    screen.blit(current_frame, (player_x, player_y))
    
    # Draw platforms
    for platform in platforms:
        pygame.draw.rect(screen, (0, 255, 0), platform)
    
    # Update display
    pygame.display.flip()
    clock.tick(30)

pygame.quit()



