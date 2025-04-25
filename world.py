import pygame
import random

class Platform:
    def __init__(self, x, y, width, height, type, assets):
        self.rect = pygame.Rect(x, y, width, height)
        self.type = type

class Pillar:
    def __init__(self, x, y, width, height, pillar_type, assets):
        self.rect = pygame.Rect(x, y, width, height)

class World:
    def __init__(self, world_width, screen_height, assets):
        self.world_width   = world_width
        self.screen_height = screen_height
        self.tile_width    = 94
        self.current_era   = "past"

        self.platforms = []
        self.pillars   = []
        self.switches  = []

        # Load sapling (2×) and pine-tree
        sap = pygame.image.load("assets/game_elements/sapling.png").convert_alpha()
        self.sapling = pygame.transform.scale(
            sap,
            (sap.get_width() * 2, sap.get_height() * 2)
        )
        self.pine_tree = pygame.image.load(
            "assets/game_elements/grow pine tree copy.png"
        ).convert_alpha()

        # Load your tiles with transparency
        self.past_tile   = pygame.image.load("assets/game_elements/yellow_tile_1.png").convert_alpha()
        self.future_tile = pygame.image.load("assets/game_elements/green_tile_1.png").convert_alpha()
        self.past_tile   = pygame.transform.scale(self.past_tile,   (94, 30))
        self.future_tile = pygame.transform.scale(self.future_tile, (94, 30))

        # ——— Campfire animation setup ———
        sheet = pygame.image.load(
            "assets/game_elements/Animated Sprites/Campfire sheet.png"
        ).convert_alpha()
        self.frame_width_fire, self.frame_height_fire = 32, 32
        self.campfire_frames = [
            sheet.subsurface(pygame.Rect(i * self.frame_width_fire, 0,
                                         self.frame_width_fire, self.frame_height_fire))
            for i in range(40)
        ]
        new_w, new_h = 75, 75
        for i in range(len(self.campfire_frames)):
            self.campfire_frames[i] = pygame.transform.scale(
                self.campfire_frames[i], (new_w, new_h)
            )
        self.campfire_index = 0
        self.campfire_timer = 0
        self.campfire_speed = 6
        # ————————————————————————

        self._make_initial_platforms()

    def _make_initial_platforms(self):
        base_y = self.screen_height - 120

        # Spawn starting platform
        first = Platform(50, base_y, self.tile_width * 3, 30, "ground", None)
        self.platforms.append(first)
        self.switches.append(pygame.Rect(100, base_y - 70, 40, 40))

        x = 50 + self.tile_width * 3
        last_y = base_y
        gaps = 0

        while x < self.world_width:
            if gaps >= 2:
                self._make_segment(x, last_y)
                gaps = 0
            else:
                if random.random() < 0.2:
                    gaps += 1
                else:
                    max_jump = 100
                    max_horiz_tiles = int(self.tile_width * 1.3)

                    v = random.randint(-max_jump, max_jump)
                    horiz_max = max_horiz_tiles
                    if v != 0:
                        allowed = (horiz_max**2 - v**2)**0.5
                        horiz_max = int(max(94, min(allowed, horiz_max)))

                    h = random.randint(94, horiz_max)
                    next_y = max(base_y - (max_jump - 2 - 25), min(base_y, last_y + v))

                    self._make_segment(x + h, next_y)
                    last_y = next_y
                    gaps = 0
            x += 94

    def _make_segment(self, x, y):
        width = self.tile_width * random.randint(2, 3)
        rect = pygame.Rect(x, y, width, 30)
        for p in self.platforms:
            if rect.colliderect(p.rect):
                return
        self.platforms.append(Platform(x, y, width, 30, "ground", None))

        if random.random() < 0.30:
            tw, th = self.pine_tree.get_size()
            px = x + (self.tile_width - tw)//2
            py = y - th
            self.pillars.append(Pillar(px, py, tw, th, "vertical", None))

        if random.random() < 0.10:
            sx = x + (width//2) - 20
            sy = y - 70
            self.switches.append(pygame.Rect(sx, sy, 40, 40))

    def update(self, player_x):
        if player_x > self.platforms[-1].rect.x - 1000:
            last = self.platforms[-1]
            base_y = self.screen_height - 120

            max_jump = 100
            horiz_limit = int(self.tile_width * 1.3)

            v = random.randint(-max_jump, max_jump)
            allowed = (horiz_limit**2 - v**2)**0.5
            h_max = int(max(94, min(allowed, horiz_limit)))
            h = random.randint(94, h_max)

            next_y = max(base_y - (max_jump - 2 - 25), min(base_y, last.rect.y + v))
            self._make_segment(last.rect.x + h, next_y)

    def draw(self, screen, camera_x):
        # Draw platforms
        overlap = 2
        tile = self.past_tile if self.current_era == "past" else self.future_tile
        for p in self.platforms:
            count = p.rect.width // (94 - overlap)
            for i in range(count):
                screen.blit(tile,
                            (p.rect.x + i*(94 - overlap) - camera_x,
                             p.rect.y))

        # Draw pillars as images
        for pillar in self.pillars:
            dx = pillar.rect.x - camera_x
            cx = dx + pillar.rect.width//2

            if self.current_era == "future":
                screen.blit(self.pine_tree, (dx, pillar.rect.y))
            else:
                sw, sh = self.sapling.get_size()
                sx = cx - sw//2
                sy = pillar.rect.bottom - sh
                screen.blit(self.sapling, (sx, sy))

        # Animate campfire in place of switches
        self.campfire_timer += 1
        if self.campfire_timer >= self.campfire_speed:
            self.campfire_timer = 0
            self.campfire_index = (self.campfire_index + 1) % len(self.campfire_frames)

        for sw in self.switches:
            x = sw.x - camera_x
            y = sw.y
            frame = self.campfire_frames[self.campfire_index]
            screen.blit(frame, (x, y))
