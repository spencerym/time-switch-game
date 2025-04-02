import pygame
import random

class Platform:
    def __init__(self, x, y, width, height, type, assets):
        self.rect = pygame.Rect(x, y, width, height)
        self.type = type  # "ground" or "floating"
            
    def draw(self, screen, camera_x, current_era):
        draw_rect = self.rect.copy()
        draw_rect.x -= camera_x
        # Different colors for past and future eras
        color = (100, 100, 100) if current_era == "past" else (150, 150, 150)
        pygame.draw.rect(screen, color, draw_rect)

class Pillar:
    def __init__(self, x, y, width, height, pillar_type, assets):
        self.pillar_type = pillar_type
        self.rect = pygame.Rect(x, y, width, height)
            
    def draw(self, screen, camera_x):
        draw_rect = self.rect.copy()
        draw_rect.x -= camera_x
        pygame.draw.rect(screen, (139, 69, 19), draw_rect)  # Brown color for pillars

class World:
    def __init__(self, world_width, screen_height, assets):
        self.world_width = world_width
        self.screen_height = screen_height
        self.tile_width = 94  # Width of each tile
        self.segment_width = self.tile_width * 2  # Two tiles per segment
        self.current_era = "past"  # Initialize current era
        
        self.platforms = []  # Both ground and floating platforms
        self.pillars = []    # Obstacles on ground platforms
        self.switches = []   # Era switch blocks
        
        # Load tile images
        self.past_tile = pygame.image.load("assets/game_elements/yellow_tile_1.png")
        self.future_tile = pygame.image.load("assets/game_elements/green_tile_1.png")
        # Scale tiles to match platform height
        self.past_tile = pygame.transform.scale(self.past_tile, (94, 30))
        self.future_tile = pygame.transform.scale(self.future_tile, (94, 30))
        
        # Generate initial platforms
        self.generate_initial_platforms()
        
    def generate_initial_platforms(self):
        # Generate ground platforms along the bottom with occasional gaps.
        x = 0
        base_ground_y = self.screen_height - 120
        
        # First, ensure there's a platform at the spawn point (around x=100)
        spawn_platform = Platform(50, base_ground_y, self.tile_width * 3, 30, "ground", None)  # 3 tiles wide
        self.platforms.append(spawn_platform)
        
        # Add initial time switch above spawn platform
        switch_rect = pygame.Rect(100, base_ground_y - 70, 40, 40)  # 70 pixels above the platform
        self.switches.append(switch_rect)
        
        # Generate initial platforms with controlled gaps
        x = 50 + self.tile_width * 3  # Start after the spawn platform
        last_y = base_ground_y
        gap_counter = 0  # Track consecutive gaps
        last_platform = spawn_platform
        
        while x < self.world_width:
            # Only allow up to 2 consecutive gaps
            if gap_counter >= 2:
                # Force a platform after 2 gaps
                next_y = last_y  # Keep same height for forced platform
                self.generate_platform_segment(x, next_y)
                last_platform = self.platforms[-1]
                gap_counter = 0
            else:
                # 20% chance for a gap
                if random.random() < 0.2:
                    gap_counter += 1
                else:
                    # Calculate maximum allowed gap based on height difference
                    max_jump_height = 150  # Maximum height difference
                    max_jump_distance = self.tile_width * 2  # Maximum gap of 2 tiles
                    
                    # Calculate maximum allowed horizontal gap based on vertical distance
                    vertical_distance = abs(next_y - last_y) if 'next_y' in locals() else 0
                    max_horizontal_gap = max_jump_distance * (1 - (vertical_distance / max_jump_height))
                    max_horizontal_gap = max(self.tile_width, min(max_jump_distance, max_horizontal_gap))
                    
                    # Generate random gap up to maximum allowed
                    horizontal_gap = random.randint(self.tile_width, int(max_horizontal_gap))
                    
                    # Calculate next platform's y position with controlled variation
                    y_variation = random.randint(-max_jump_height, max_jump_height)
                    next_y = last_y + y_variation
                    
                    # Ensure the platform stays within playable bounds
                    next_y = max(base_ground_y - 150, min(base_ground_y + 50, next_y))
                    
                    # Generate the platform segment
                    self.generate_platform_segment(x + horizontal_gap, next_y)
                    last_platform = self.platforms[-1]
                    last_y = next_y
                    gap_counter = 0
            
            x += self.segment_width

    def generate_platform_segment(self, x, y):
        # Create platform with width based on tile size
        num_tiles = random.randint(2, 3)  # 2 or 3 tiles per platform
        platform_width = self.tile_width * num_tiles
        
        # Check if this platform would overlap with any existing platform
        new_platform = pygame.Rect(x, y, platform_width, 30)
        for existing_platform in self.platforms:
            if new_platform.colliderect(existing_platform.rect):
                return  # Skip this platform if it would overlap
        
        # If no overlap, create the platform
        platform = Platform(x, y, platform_width, 30, "ground", None)
        self.platforms.append(platform)
        
        # 30% chance to add a pillar (increased from 15%)
        if random.random() < 0.30:
            # 70% chance for vertical pillar, 30% for horizontal
            if random.random() < 0.70:
                # Vertical pillar
                pillar_width = 30
                pillar_height = random.randint(100, 200)
                pillar_x = x + (self.tile_width - pillar_width) // 2
                pillar_y = y - pillar_height
                pillar = Pillar(pillar_x, pillar_y, pillar_width, pillar_height, "vertical", None)
            else:
                # Horizontal pillar
                pillar_width = random.randint(100, 200)
                pillar_height = 30
                pillar_x = x + (self.tile_width - pillar_width) // 2
                pillar_y = y - 100  # Fixed height above platform for horizontal pillars
                pillar = Pillar(pillar_x, pillar_y, pillar_width, pillar_height, "horizontal", None)
            self.pillars.append(pillar)
            
        # 10% chance to add a time switch above the platform
        if random.random() < 0.10:
            switch_x = x + (platform_width // 2) - 20  # Center on platform
            switch_y = y - 70  # 70 pixels above the platform
            switch_rect = pygame.Rect(switch_x, switch_y, 40, 40)
            self.switches.append(switch_rect)

    def generate_floating_platforms(self):
        # Generate floating platforms randomly in the level.
        count = int(self.world_width / 300)  # roughly one every 300 pixels
        for _ in range(count):
            x = random.randint(0, self.world_width - 50)
            # Adjust height range to make some platforms reachable
            # Most platforms will be lower, but some will be higher
            if random.random() < 0.7:  # 70% chance for lower platforms
                y = random.randint(self.screen_height - 300, self.screen_height - 200)
            else:  # 30% chance for higher platforms
                y = random.randint(self.screen_height - 400, self.screen_height - 300)
            platform = Platform(x, y, 50, 15, "floating", None)
            self.platforms.append(platform)
            
    def generate_switches(self):
        # Place era switches approximately every 500 pixels.
        x = 200
        while x < self.world_width:
            if random.random() < 0.5:
                # Attach the switch near a platform.
                candidates = [p for p in self.platforms if p.rect.x <= x <= p.rect.x + p.rect.width]
                if candidates:
                    platform = random.choice(candidates)
                    sw_x = x
                    sw_y = platform.rect.y - 50  # placed above the platform
                    sw_rect = pygame.Rect(sw_x, sw_y, 40, 40)
                    self.switches.append(sw_rect)
            x += 500
            
    def update(self, player_x):
        # Generate new platforms as the player moves right
        if player_x > self.platforms[-1].rect.x - 1000:  # Start generating 1000 pixels before the end
            last_platform = self.platforms[-1]
            last_y = last_platform.rect.y
            
            # Calculate maximum allowed gap based on height difference
            max_jump_height = 150  # Maximum height difference
            max_jump_distance = self.tile_width * 2  # Maximum gap of 2 tiles
            
            # Calculate maximum allowed horizontal gap based on vertical distance
            vertical_distance = abs(next_y - last_y) if 'next_y' in locals() else 0
            max_horizontal_gap = max_jump_distance * (1 - (vertical_distance / max_jump_height))
            max_horizontal_gap = max(self.tile_width, min(max_jump_distance, max_horizontal_gap))
            
            # Generate random gap up to maximum allowed
            horizontal_gap = random.randint(self.tile_width, int(max_horizontal_gap))
            
            # Calculate next platform's y position with controlled variation
            y_variation = random.randint(-max_jump_height, max_jump_height)
            next_y = last_y + y_variation
            
            # Ensure the platform stays within playable bounds
            base_ground_y = self.screen_height - 120
            next_y = max(base_ground_y - 150, min(base_ground_y + 50, next_y))
            
            # Generate new platform segment with the calculated gap
            self.generate_platform_segment(last_platform.rect.x + horizontal_gap, next_y)
            
    def draw(self, screen, camera_x):
        # Draw platforms with appropriate tile based on era
        current_tile = self.past_tile if self.current_era == "past" else self.future_tile
        
        for platform in self.platforms:
            # Each tile is 94 pixels wide, but we'll overlap them by 2 pixels
            tile_width = 94
            overlap = 2  # How many pixels to overlap
            platform_width = platform.rect.width
            
            # Calculate number of tiles needed (round down to avoid overflow)
            num_tiles = platform_width // (tile_width - overlap)
            
            # Draw the tiles with slight overlap
            for i in range(num_tiles):
                x_pos = platform.rect.x + (i * (tile_width - overlap)) - camera_x
                screen.blit(current_tile, (x_pos, platform.rect.y))
        
        # Draw pillars only in past era
        if self.current_era == "past":
            for pillar in self.pillars:
                pygame.draw.rect(screen, (100, 100, 100), 
                               (pillar.rect.x - camera_x, pillar.rect.y, pillar.rect.width, pillar.rect.height))
        
        # Draw switches
        for switch in self.switches:
            color = (0, 0, 255) if self.current_era == "past" else (255, 165, 0)
            pygame.draw.rect(screen, color, 
                           (switch.x - camera_x, switch.y, switch.width, switch.height))
