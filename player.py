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
        
        # Move horizontally first
        self.rect.x += int(self.vel_x * dt)
        
        # Check horizontal collisions
        for platform in world.platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_x > 0:  # Moving right
                    self.rect.right = platform.rect.left
                elif self.vel_x < 0:  # Moving left
                    self.rect.left = platform.rect.right
        
        # Check pillar collisions horizontally
        if current_era == "past":
            for pillar in world.pillars:
                if self.rect.colliderect(pillar.rect):
                    if self.vel_x > 0:  # Moving right
                        self.rect.right = pillar.rect.left
                    elif self.vel_x < 0:  # Moving left
                        self.rect.left = pillar.rect.right
        
        # Move vertically
        self.rect.y += int(self.vel_y * dt)
        
        # Check vertical collisions
        self.on_ground = False
        for platform in world.platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:  # Falling
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:  # Jumping
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0
        
        # Check pillar collisions vertically
        if current_era == "past":
            for pillar in world.pillars:
                if self.rect.colliderect(pillar.rect):
                    if self.vel_y > 0:  # Falling
                        self.rect.bottom = pillar.rect.top
                        self.vel_y = 0
                        self.on_ground = True
                    elif self.vel_y < 0:  # Jumping
                        self.rect.top = pillar.rect.bottom
                        self.vel_y = 0

    def draw(self, screen, camera_x):
        draw_rect = self.rect.copy()
        draw_rect.x -= camera_x
        pygame.draw.rect(screen, (255, 0, 0), draw_rect)  # Red rectangle for player
