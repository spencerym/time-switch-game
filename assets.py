import pygame

def load_assets():
    assets = {}
    
    # Create player idle image (30x50)
    player_idle = pygame.Surface((30, 50), pygame.SRCALPHA)
    player_idle.fill((255, 0, 0))
    pygame.draw.rect(player_idle, (0, 0, 0), player_idle.get_rect(), 2)
    pygame.draw.circle(player_idle, (0,0,0), (15, 15), 3)  # simple face
    assets["player_idle"] = player_idle
    
    # Create walking animation frames (4 frames)
    walk_frames = []
    for i in range(4):
        frame = pygame.Surface((30, 50), pygame.SRCALPHA)
        frame.fill((255, 0, 0))
        pygame.draw.rect(frame, (0, 0, 0), frame.get_rect(), 2)
        # Draw a simple face
        pygame.draw.circle(frame, (0,0,0), (15, 15), 3)
        # Simulate leg movement: alternate leg positions
        leg_offset = 5 * ((i % 2) * 2 - 1)  # alternates between +5 and -5
        pygame.draw.line(frame, (0, 0, 0), (10, 50), (10 + leg_offset, 40), 3)
        pygame.draw.line(frame, (0, 0, 0), (20, 50), (20 - leg_offset, 40), 3)
        walk_frames.append(frame)
    assets["player_walk"] = walk_frames
    
    # Create a jumping frame (legs tucked in)
    player_jump = pygame.Surface((30, 50), pygame.SRCALPHA)
    player_jump.fill((255, 0, 0))
    pygame.draw.rect(player_jump, (0, 0, 0), player_jump.get_rect(), 2)
    pygame.draw.circle(player_jump, (0,0,0), (15, 15), 3)
    pygame.draw.line(player_jump, (0, 0, 0), (15, 50), (15, 40), 3)
    assets["player_jump"] = player_jump
    
    # Ground platform sprite (50x20)
    platform_ground = pygame.Surface((50, 20), pygame.SRCALPHA)
    platform_ground.fill((139, 69, 19))
    pygame.draw.line(platform_ground, (100, 50, 20), (0, 10), (50, 10))
    assets["platform_ground"] = platform_ground
    
    # Floating platform sprite (50x15)
    platform_floating = pygame.Surface((50, 15), pygame.SRCALPHA)
    platform_floating.fill((160, 82, 45))
    pygame.draw.line(platform_floating, (120, 60, 30), (0, 7), (50, 7))
    assets["platform_floating"] = platform_floating
    
    # Pillar sprites
    # Normal pillar (30x80)
    pillar_normal = pygame.Surface((30, 80), pygame.SRCALPHA)
    pillar_normal.fill((128, 128, 128))
    pygame.draw.rect(pillar_normal, (100, 100, 100), pillar_normal.get_rect(), 3)
    assets["pillar_normal"] = pillar_normal
    
    # Broken pillar (30x80)
    pillar_broken = pygame.Surface((30, 80), pygame.SRCALPHA)
    pillar_broken.fill((128, 128, 128))
    pygame.draw.line(pillar_broken, (0, 0, 0), (15, 0), (15, 80), 2)
    pygame.draw.line(pillar_broken, (0, 0, 0), (0, 40), (30, 40), 2)
    assets["pillar_broken"] = pillar_broken
    
    # Sideways pillar (80x30)
    pillar_sideways = pygame.Surface((80, 30), pygame.SRCALPHA)
    pillar_sideways.fill((128, 128, 128))
    pygame.draw.rect(pillar_sideways, (100, 100, 100), pillar_sideways.get_rect(), 3)
    assets["pillar_sideways"] = pillar_sideways
    
    # Era switch sprite (blue block 40x40)
    era_switch = pygame.Surface((40, 40), pygame.SRCALPHA)
    era_switch.fill((0, 0, 255))
    assets["era_switch"] = era_switch
    
    # Background: a gradient sky (800x600)
    bg = pygame.Surface((800, 600))
    top_color = (135, 206, 235)   # sky blue
    bottom_color = (25, 25, 112)  # midnight blue
    for y in range(600):
        ratio = y / 600
        r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
        g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
        b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
        pygame.draw.line(bg, (r, g, b), (0, y), (800, y))
    assets["background"] = bg
    
    return assets
