# world.py
import pygame
import random

class Platform:
    def __init__(self, x, y, width, height, type, assets):
        self.rect = pygame.Rect(x, y, width, height)
        self.type = type

    def draw(self, screen, camera_x, current_era):
        draw_rect = self.rect.copy()
        draw_rect.x -= camera_x
        color = (100, 100, 100) if current_era == "past" else (150, 150, 150)
        pygame.draw.rect(screen, color, draw_rect)

class Pillar:
    def __init__(self, x, y, width, height, pillar_type, assets):
        self.pillar_type = pillar_type
        self.rect = pygame.Rect(x, y, width, height)

class World:
    def __init__(self, world_width, screen_height, assets):
        self.world_width = world_width
        self.screen_height = screen_height
        self.tile_width = 94
        self.current_era = "past"
        self.platforms = []
        self.pillars   = []
        self.switches  = []

        self.past_tile   = pygame.image.load("assets/game_elements/yellow_tile_1.png")
        self.future_tile = pygame.image.load("assets/game_elements/green_tile_1.png")
        self.past_tile   = pygame.transform.scale(self.past_tile,   (94, 30))
        self.future_tile = pygame.transform.scale(self.future_tile, (94, 30))

        self.generate_initial_platforms()

    def generate_initial_platforms(self):
        x = 0
        base_y = self.screen_height - 120
        spawn = Platform(50, base_y, self.tile_width * 3, 30, "ground", None)
        self.platforms.append(spawn)
        self.switches.append(pygame.Rect(100, base_y - 70, 40, 40))

        x = 50 + self.tile_width * 3
        last_y = base_y
        gaps = 0

        while x < self.world_width:
            if gaps >= 2:
                self.generate_platform_segment(x, last_y)
                gaps = 0
            else:
                if random.random() < 0.2:
                    gaps += 1
                else:
                    max_jump = 140
                    max_horiz = int(94 * 1.5)
                    vert = random.randint(-max_jump, max_jump)
                    if vert != 0:
                        total = max_horiz
                        max_horiz = int(max(94, min((total**2 - vert**2)**0.5, total)))
                    horiz = random.randint(94, max_horiz)
                    next_y = max(base_y - (max_jump - 2 - 25), min(base_y, last_y + vert))
                    self.generate_platform_segment(x + horiz, next_y)
                    last_y = next_y
                    gaps = 0
            x += 94

    def generate_platform_segment(self, x, y):
        num_tiles = random.randint(2, 3)
        width = self.tile_width * num_tiles
        new_rect = pygame.Rect(x, y, width, 30)
        for p in self.platforms:
            if new_rect.colliderect(p.rect):
                return
        self.platforms.append(Platform(x, y, width, 30, "ground", None))

        # 30% chance to spawn ONLY a vertical pillar
        if random.random() < 0.30:
            pw = 30
            ph = random.randint(100, 200)
            px = x + (self.tile_width - pw) // 2
            py = y - ph
            self.pillars.append(Pillar(px, py, pw, ph, "vertical", None))

        # 10% chance for an era‑switch
        if random.random() < 0.10:
            sx = x + (width // 2) - 20
            sy = y - 70
            self.switches.append(pygame.Rect(sx, sy, 40, 40))

    def update(self, player_x):
        if player_x > self.platforms[-1].rect.x - 1000:
            last = self.platforms[-1]
            base_y = self.screen_height - 120
            max_jump = 140
            total = int(94 * 1.5)
            vert = random.randint(-max_jump, max_jump)
            horiz = random.randint(94, int(max(94, min((total**2 - vert**2)**0.5, total))))
            next_y = max(base_y - (max_jump - 2 - 25), min(base_y, last.rect.y + vert))
            self.generate_platform_segment(last.rect.x + horiz, next_y)

    def draw(self, screen, camera_x):
        tile = self.past_tile if self.current_era == "past" else self.future_tile
        overlap = 2
        for p in self.platforms:
            num = p.rect.width // (94 - overlap)
            for i in range(num):
                x_ = p.rect.x + i*(94-overlap) - camera_x
                screen.blit(tile, (x_, p.rect.y))

        # DRAW PILLARS only in future era
        if self.current_era == "future":
            for pillar in self.pillars:
                r = pillar.rect
                pygame.draw.rect(screen, (100,100,100),
                                 (r.x - camera_x, r.y, r.width, r.height))

        # DRAW SWITCHES
        for sw in self.switches:
            color = (0,0,255) if self.current_era=="past" else (255,165,0)
            pygame.draw.rect(screen, color,
                             (sw.x - camera_x, sw.y, sw.width, sw.height))
