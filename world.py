import pygame
import random

class Platform:
    def __init__(self, x, y, width, height, type, assets):
        self.rect = pygame.Rect(x, y, width, height)
        self.type = type  # "ground" or "floating"
        if type == "ground":
            self.sprite = assets["platform_ground"]
        else:
            self.sprite = assets["platform_floating"]
            
    def draw(self, screen, camera_x):
        draw_rect = self.rect.copy()
        draw_rect.x -= camera_x
        screen.blit(self.sprite, draw_rect)

class Pillar:
    def __init__(self, x, y, width, height, pillar_type, assets):
        self.pillar_type = pillar_type
        if pillar_type == "sideways":
            # For sideways pillars, swap width and height.
            self.rect = pygame.Rect(x, y, height, width)
            self.sprite = assets["pillar_sideways"]
        elif pillar_type == "broken":
            self.rect = pygame.Rect(x, y, width, height)
            self.sprite = assets["pillar_broken"]
        else:
            self.rect = pygame.Rect(x, y, width, height)
            self.sprite = assets["pillar_normal"]
            
    def draw(self, screen, camera_x):
        draw_rect = self.rect.copy()
        draw_rect.x -= camera_x
        screen.blit(self.sprite, draw_rect)

class World:
    def __init__(self, world_width, screen_height, assets):
        self.world_width = world_width
        self.screen_height = screen_height
        self.assets = assets
        
        self.platforms = []  # Both ground and floating platforms
        self.pillars = []    # Obstacles on ground platforms
        self.switches = []   # Era switch blocks
        
        self.generate_platforms()
        self.generate_floating_platforms()
        self.generate_pillars()
        self.generate_switches()
        
    def generate_platforms(self):
        # Generate ground platforms along the bottom with occasional gaps.
        segment_width = 50
        x = 0
        base_ground_y = self.screen_height - 120
        while x < self.world_width:
            # 20% chance to create a gap (hole)
            if random.random() < 0.2:
                x += segment_width
                continue
            # Use a smaller variation for smoother terrain.
            y_variation = random.randint(-5, 5)
            y = base_ground_y + y_variation
            platform = Platform(x, y, segment_width, 20, "ground", self.assets)
            self.platforms.append(platform)
            x += segment_width
            
    def generate_floating_platforms(self):
        # Generate floating platforms randomly in the level.
        count = int(self.world_width / 300)  # roughly one every 300 pixels
        for _ in range(count):
            x = random.randint(0, self.world_width - 50)
            y = random.randint(100, self.screen_height - 200)
            platform = Platform(x, y, 50, 15, "floating", self.assets)
            self.platforms.append(platform)
            
    def generate_pillars(self):
        # On ground platforms, with some probability, add a pillar.
        for platform in self.platforms:
            if platform.type == "ground" and random.random() < 0.15:
                pillar_type = random.choice(["normal", "broken", "sideways"])
                pillar_width = 30
                # Increase pillar height range for taller pillars.
                pillar_height = random.randint(100, 200)
                # Position the pillar roughly centered on the platform.
                x = platform.rect.x + (platform.rect.width - pillar_width) // 2
                y = platform.rect.y - pillar_height
                pillar = Pillar(x, y, pillar_width, pillar_height, pillar_type, self.assets)
                self.pillars.append(pillar)
                
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
            
    def draw(self, screen, camera_x, current_era):
        # Draw all platforms.
        for platform in self.platforms:
            platform.draw(screen, camera_x)
        # In the past era, draw pillars.
        if current_era == "past":
            for pillar in self.pillars:
                pillar.draw(screen, camera_x)
        # Draw era switches.
        for sw in self.switches:
            draw_rect = sw.copy()
            draw_rect.x -= camera_x
            screen.blit(self.assets["era_switch"], draw_rect)
