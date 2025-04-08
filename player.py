import pygame

GRAVITY = 900      # Increased gravity for a stronger pull.
MOVE_SPEED = 200
JUMP_SPEED = 400   # Reduced jump speed so players can't jump over pillars.

# Load and prepare cat sprites
running_sprite_sheet = pygame.image.load("assets/cat/2_Cat_Run-Sheet.png")
idle_sprite_sheet = pygame.image.load("assets/cat/1_Cat_Idle-Sheet.png")
jumping_sprite_sheet = pygame.image.load("assets/cat/3_Cat_Jump-Sheet.png")
falling_sprite_sheet = pygame.image.load("assets/cat/4_Cat_Fall-Sheet.png")

# Frame dimensions
frame_width_run, frame_height_run = 16, 15
frame_width_idle, frame_height_idle = 13, 18
frame_width_jump, frame_height_jump = 11, 17
frame_width_fall, frame_height_fall = 11, 18

# Extract frames from sprite sheets
running_frames = [running_sprite_sheet.subsurface(pygame.Rect(i * frame_width_run, 0, frame_width_run, frame_height_run)) for i in range(10)]
idle_frames = [idle_sprite_sheet.subsurface(pygame.Rect(x * frame_width_idle, 0, frame_width_idle, frame_height_idle)) for x in range(7)]
jump_up_frames = [jumping_sprite_sheet.subsurface(pygame.Rect(f * frame_width_fall, 0, frame_width_jump, frame_height_jump)) for f in range(4)]
jump_down_frames = [falling_sprite_sheet.subsurface(pygame.Rect(j * frame_width_fall, 0, frame_width_fall, frame_height_fall)) for j in range(4)]

# Scale frames
newWidth = 50
newHeight = 50

for i in range(7):
    idle_frames[i] = pygame.transform.scale(idle_frames[i], (newWidth, newHeight))

for i in range(10):
    running_frames[i] = pygame.transform.scale(running_frames[i], (newWidth, newHeight))

for i in range(4):
    jump_up_frames[i] = pygame.transform.scale(jump_up_frames[i], (newWidth, newHeight))
    jump_down_frames[i] = pygame.transform.scale(jump_down_frames[i], (newWidth, newHeight))

class Player:
    def __init__(self, x, y, assets):
        self.rect = pygame.Rect(x, y, 50, 50)  # Updated size to match cat sprite
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        
        # Animation variables
        self.frame_index = 0
        self.idle_index = 0
        self.jump_index = 0
        self.fall_index = 0
        self.animation_timer = 0
        self.idle_timer = 0
        self.jump_timer = 0
        self.fall_timer = 0
        self.facing_right = True
        
    def handle_input(self, keys):
        self.vel_x = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.vel_x = -MOVE_SPEED
            self.facing_right = False
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.vel_x = MOVE_SPEED
            self.facing_right = True
        if (keys[pygame.K_w] or keys[pygame.K_UP] or keys[pygame.K_SPACE]) and self.on_ground:
            self.vel_y = -JUMP_SPEED
            self.on_ground = False
            
    def update(self, dt, world, current_era):
        # Apply gravity
        self.vel_y += GRAVITY * dt
        
        # Store old position for collision resolution
        old_x = self.rect.x
        old_y = self.rect.y
        
        # Update position
        self.rect.x += int(self.vel_x * dt)
        self.rect.y += int(self.vel_y * dt)
        
        # Check collisions with platforms
        self.on_ground = False
        for platform in world.platforms:
            if self.rect.colliderect(platform.rect):
                # First check if this is a vertical collision
                if old_y + self.rect.height <= platform.rect.top or old_y >= platform.rect.bottom:
                    # Vertical collision
                    if self.vel_y > 0:  # Falling
                        self.rect.bottom = platform.rect.top
                        self.vel_y = 0
                        self.on_ground = True
                    elif self.vel_y < 0:  # Jumping
                        self.rect.top = platform.rect.bottom
                        self.vel_y = 0
                else:
                    # Horizontal collision
                    if self.vel_x > 0:  # Moving right
                        if old_x + self.rect.width <= platform.rect.left:
                            self.rect.right = platform.rect.left
                    elif self.vel_x < 0:  # Moving left
                        if old_x >= platform.rect.right:
                            self.rect.left = platform.rect.right
        
        # Check collisions with pillars in past era
        if current_era == "past":
            for pillar in world.pillars:
                if self.rect.colliderect(pillar.rect):
                    # Handle all sides of the pillar
                    # First check if this is a vertical collision
                    if old_y + self.rect.height <= pillar.rect.top or old_y >= pillar.rect.bottom:
                        # Vertical collision
                        if self.vel_y > 0:  # Falling
                            self.rect.bottom = pillar.rect.top
                            self.vel_y = 0
                            self.on_ground = True
                        elif self.vel_y < 0:  # Jumping
                            self.rect.top = pillar.rect.bottom
                            self.vel_y = 0
                    else:
                        # Horizontal collision
                        if self.vel_x > 0:  # Moving right
                            if old_x + self.rect.width <= pillar.rect.left:
                                self.rect.right = pillar.rect.left
                        elif self.vel_x < 0:  # Moving left
                            if old_x >= pillar.rect.right:
                                self.rect.left = pillar.rect.right

    def draw(self, screen, camera_x):
        # Update animation
        if self.vel_y < 0:
            # Jumping up
            self.jump_timer += 1
            if self.jump_timer >= 15:  # Changed from % to >= and reset timer
                self.jump_timer = 0
                self.jump_index = (self.jump_index + 1) % len(jump_up_frames)
            current_frame = jump_up_frames[self.jump_index]
        elif self.vel_y > 1 or not self.on_ground:
            # Falling down
            self.fall_timer += 1
            if self.fall_timer >= 15:  # Changed from % to >= and reset timer
                self.fall_timer = 0
                self.fall_index = (self.fall_index + 1) % len(jump_down_frames)
            current_frame = jump_down_frames[self.fall_index]
        else:
            # On ground — idle or running
            if self.vel_x != 0:
                self.animation_timer += 1
                if self.animation_timer >= 1800:
                    self.animation_timer = 0
                    self.frame_index = (self.frame_index + 1) % len(running_frames)
                current_frame = running_frames[self.frame_index]
            else:
                self.idle_timer += 1
                if self.idle_timer >= 2700:
                    self.idle_timer = 0
                    self.idle_index = (self.idle_index + 1) % len(idle_frames)
                current_frame = idle_frames[self.idle_index]

        # Flip sprite if facing left
        if not self.facing_right:
            current_frame = pygame.transform.flip(current_frame, True, False)
        
        # Draw the sprite
        screen.blit(current_frame, (self.rect.x - camera_x, self.rect.y))
