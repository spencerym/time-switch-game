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
        self.segment_width = 50
        
        self.platforms = []  # Both ground and floating platforms
        self.pillars = []    # Obstacles on ground platforms
        self.switches = []   # Era switch blocks
        
        # Generate initial platforms
        self.generate_initial_platforms()
        
    def generate_initial_platforms(self):
        # Generate ground platforms along the bottom with occasional gaps.
        x = 0
        base_ground_y = self.screen_height - 120
        
        # First, ensure there's a platform at the spawn point (around x=100)
        spawn_platform = Platform(50, base_ground_y, self.segment_width * 2, 20, "ground", None)
        self.platforms.append(spawn_platform)
        
        # Add a time switcher at the spawn point
        spawn_switch = pygame.Rect(100, base_ground_y - 50, 40, 40)
        self.switches.append(spawn_switch)
        
        # Generate initial platforms
        x = 150  # Start after the spawn platform
        while x < self.world_width:
            self.generate_platform_segment(x, base_ground_y)
            x += self.segment_width
            
    def generate_platform_segment(self, x, base_ground_y):
        # 20% chance to create a gap (hole)
        if random.random() < 0.2:
            return
            
        # Use a smaller variation for smoother terrain.
        y_variation = random.randint(-5, 5)
        y = base_ground_y + y_variation
        platform = Platform(x, y, self.segment_width, 20, "ground", None)
        self.platforms.append(platform)
        
        # 15% chance to add a pillar
        if random.random() < 0.15:
            pillar_width = 30
            pillar_height = random.randint(100, 200)
            pillar_x = x + (self.segment_width - pillar_width) // 2
            pillar_y = y - pillar_height
            pillar = Pillar(pillar_x, pillar_y, pillar_width, pillar_height, "normal", None)
            self.pillars.append(pillar)
            
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
        last_platform_x = max(p.rect.x for p in self.platforms)
        while last_platform_x < player_x + self.world_width:
            self.generate_platform_segment(last_platform_x + self.segment_width, self.screen_height - 120)
            last_platform_x += self.segment_width
            
    def draw(self, screen, camera_x, current_era):
        # Draw all platforms.
        for platform in self.platforms:
            platform.draw(screen, camera_x, current_era)
        # In the past era, draw pillars.
        if current_era == "past":
            for pillar in self.pillars:
                pillar.draw(screen, camera_x)
        # Draw era switches.
        for sw in self.switches:
            draw_rect = sw.copy()
            draw_rect.x -= camera_x
            pygame.draw.rect(screen, (0, 0, 255), draw_rect)  # Blue rectangles for switches
