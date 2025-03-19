import pygame

GRAVITY = 900      # Increased gravity for a stronger pull.
MOVE_SPEED = 200
JUMP_SPEED = 400   # Reduced jump speed so players can't jump over pillars.

class Player:
    def __init__(self, x, y, assets):
        self.rect = pygame.Rect(x, y, 30, 50)
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        
        # Set up animations from assets.
        self.animations = {
            "idle": assets["player_idle"],
            "walk": assets["player_walk"],   # list of frames
            "jump": assets["player_jump"]
        }
        self.state = "idle"
        self.animation_index = 0
        self.animation_timer = 0.0
        self.animation_speed = 0.1  # seconds per frame
        
    def handle_input(self, keys):
        self.vel_x = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.vel_x = -MOVE_SPEED
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.vel_x = MOVE_SPEED
        if (keys[pygame.K_w] or keys[pygame.K_UP] or keys[pygame.K_SPACE]) and self.on_ground:
            self.vel_y = -JUMP_SPEED
            self.on_ground = False
            
    def update(self, dt, world, current_era):
        # Apply gravity.
        self.vel_y += GRAVITY * dt
        
        # Horizontal movement and collision with platforms.
        self.rect.x += int(self.vel_x * dt)
        for platform in world.platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_x > 0:
                    self.rect.right = platform.rect.left
                elif self.vel_x < 0:
                    self.rect.left = platform.rect.right
        if current_era == "past":
            for pillar in world.pillars:
                if self.rect.colliderect(pillar.rect):
                    if self.vel_x > 0:
                        self.rect.right = pillar.rect.left
                    elif self.vel_x < 0:
                        self.rect.left = pillar.rect.right
        
        # Vertical movement and collision.
        self.rect.y += int(self.vel_y * dt)
        self.on_ground = False
        for platform in world.platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0 and abs(self.rect.bottom - platform.rect.top) < 20:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
        if current_era == "past":
            for pillar in world.pillars:
                if self.rect.colliderect(pillar.rect):
                    if self.vel_y > 0:
                        self.rect.bottom = pillar.rect.top
                        self.vel_y = 0
                        self.on_ground = True
                    elif self.vel_y < 0:
                        self.rect.top = pillar.rect.bottom
                        self.vel_y = 0

        # Determine state: jump if in air, walk if moving horizontally, else idle.
        if not self.on_ground:
            self.state = "jump"
        elif self.vel_x != 0:
            self.state = "walk"
        else:
            self.state = "idle"
        
        # Update walking animation (if applicable).
        if self.state == "walk":
            self.animation_timer += dt
            if self.animation_timer >= self.animation_speed:
                self.animation_timer -= self.animation_speed
                self.animation_index = (self.animation_index + 1) % len(self.animations["walk"])
        else:
            # Reset walking animation when not in walk state.
            self.animation_index = 0
            self.animation_timer = 0.0

    def draw(self, screen, camera_x):
        draw_rect = self.rect.copy()
        draw_rect.x -= camera_x
        
        # Choose the appropriate sprite based on state.
        if self.state == "idle":
            sprite = self.animations["idle"]
        elif self.state == "walk":
            sprite = self.animations["walk"][self.animation_index]
        elif self.state == "jump":
            sprite = self.animations["jump"]
        else:
            sprite = self.animations["idle"]
            
        screen.blit(sprite, draw_rect)
