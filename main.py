import pygame

# Initialize pygame
pygame.init()

WIDTH, HEIGHT = 800, 600
BLACK = (0, 0, 0)
GRAVITY = .4

#Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer Game")


def increaseScale(image, width, height):
    image = pygame.transform.scale(image, (width, height))
    return image

#Sprite guy
running_sprite_sheet = pygame.image.load("assets/FreeCatCharacterAnimations/2_Cat_Run-Sheet.png")
idle_sprite_sheet = pygame.image.load("assets/FreeCatCharacterAnimations/1_Cat_Idle-Sheet.png")
jumping_sprite_sheet = pygame.image.load("assets/FreeCatCharacterAnimations/3_Cat_Jump-Sheet.png")
falling_sprite_sheet = pygame.image.load("assets/FreeCatCharacterAnimations/4_Cat_Fall-Sheet.png")

# Right frames animation?
frame_width_run, frame_height_run = 16, 15
frame_width_idle, frame_height_idle = 13, 18
frame_width_jump, frame_height_jump = 11, 17
frame_width_fall, frame_height_fall = 11, 18


running_frames = [running_sprite_sheet.subsurface(pygame.Rect(i * frame_width_run, 0, frame_width_run, frame_height_run)) for i in range(10)]
idle_frames = [idle_sprite_sheet.subsurface(pygame.Rect(x * frame_width_idle, 0, frame_width_idle, frame_height_idle)) for x in range(7)]
jump_up_frames = [jumping_sprite_sheet.subsurface(pygame.Rect(f * frame_width_fall, 0, frame_width_jump, frame_height_jump)) for f in range(4)]
jump_down_frames = [falling_sprite_sheet.subsurface(pygame.Rect(j * frame_width_fall, 0, frame_width_fall, frame_height_fall)) for j in range(4)]

newWidth = 50
newHeight = 50

for i in range(7):
    idle_frames[i] = increaseScale(idle_frames[i], newWidth, newHeight)

for i in range(10):
    running_frames[i] = increaseScale(running_frames[i], newWidth, newHeight)

for i in range(4):
    jump_up_frames[i] = increaseScale(jump_up_frames[i], newWidth, newHeight)
    jump_down_frames[i] = increaseScale(jump_down_frames[i], newWidth, newHeight)

# Player settings
player_x, player_y = 100, HEIGHT - 150
player_speed = 5
jump_power = -10
player_velocity_y = 0
on_ground = False
frame_index = 0
idle_index = 0
jump_index = 0
fall_index = 0
animation_timer = 0
idle_timer = 0
jump_timer = 0
fall_timer = 0
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
    screen.fill(BLACK)
    
    
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
    if keys[pygame.K_UP] and on_ground:
        player_velocity_y = jump_power
        on_ground = False
    
    #gravity
    player_velocity_y += GRAVITY
    player_y += player_velocity_y
    
    # Collision
    player_rect = pygame.Rect(player_x, player_y, newWidth, newHeight)
    for platform in platforms:
        if player_rect.colliderect(platform) and player_velocity_y > 0:
            player_y = platform.top - newHeight
            player_velocity_y = 0
            on_ground = True
    
    # Lose
    if player_y > HEIGHT:
        print("You died!")
        running = False
    
    # animation
    if player_velocity_y < 0:
        # Jumping up
        jump_timer += 1
        if jump_timer % 8 == 0:
            jump_index = (jump_index + 1) % len(jump_up_frames)
        current_frame = jump_up_frames[jump_index]
    elif player_velocity_y > 1 or not on_ground:  
        # Falling down
        fall_timer += 1
        if fall_timer % 6 == 0:
            fall_index = (fall_index + 1) % len(jump_down_frames)
        current_frame = jump_down_frames[fall_index]
    else:
        # On ground — idle or running
        if moving:
            animation_timer += 1
            if animation_timer % 6 == 0:
                frame_index = (frame_index + 1) % len(running_frames)
            current_frame = running_frames[frame_index]
        else:
            idle_timer += 1
            if idle_timer % 12 == 0:
                idle_index = (idle_index + 1) % len(idle_frames)
            current_frame = idle_frames[idle_index]

    #flipping sprite face    
    if not facing_right:
        current_frame = pygame.transform.flip(current_frame, True, False)
    
    # Draw player
    screen.blit(current_frame, (player_x, player_y))
    
    # Draw platforms
    for platform in platforms:
        pygame.draw.rect(screen, (0, 255, 0), platform)
    
    # Update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()



