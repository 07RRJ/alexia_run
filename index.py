import pygame
from dataclasses import dataclass, field
import sys, os
import random


def get_game_folder():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))


game_folder = get_game_folder()
images_folder = os.path.join(game_folder, "img")

pygame.init()

# Window setup
WIDTH, HEIGHT = 500, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("alexia run")

# Player image load
PLAYER_WIDTH, PLAYER_HEIGHT = 30, 30
player_img = pygame.image.load(os.path.join(images_folder, "player.png")).convert_alpha()
# player_img = pygame.image.load(os.path.join(images_folder, "monek.png")).convert_alpha()
# player_img = pygame.image.load(os.path.join(images_folder, "monkey.svg")).convert_alpha()
player_img = pygame.transform.scale(player_img, (PLAYER_WIDTH, PLAYER_HEIGHT))

# Player fixed horizontal position (centered)
x = WIDTH // 10 - PLAYER_WIDTH // 2
y = 400
vel = 5
y_vel = 0
gravity = 1
jump_power = 16
isJump = False

COLOURS = {
    "GREEN" : (50, 170, 60),
    "BLUE" : (60, 50, 170),
    "RED" : (170, 60, 50)
}

@dataclass
class N_Platform:
    x: int
    width: int
    attribute: int

    platform_y: list = field(default_factory=lambda: [
        [390, 440],
        [240, 290, 340],
        [90, 140, 190]
    ])
    colours: list = field(default_factory=lambda: [
        [50, 170, 60], 
        [60, 50, 170], 
        [170, 60, 50]
    ])
    random: int = field(default_factory=lambda: (random.randint(0, 2)))
    y: int = field(init=False)

    def __post_init__(self):
        self.y = random.choice(self.platform_y[self.attribute])

    def rect(self):
        height = 5
        width = 120

        return pygame.Rect(self.x, self.y, width, height)

    def display(self, screen):
        colour = self.colours[self.attribute]
        pygame.draw.rect(screen, colour, self.rect())

# Initial platforms
platforms = []

for i in range(2000):
    # platforms.append(N_Platform(220, 10, 0))
    # platforms.append(N_Platform(300, 10, 1))
    # platforms.append(N_Platform(300, 10, 2))
    platforms.append(N_Platform(500 + i * 320, 10, 0))
    platforms.append(N_Platform(660 + i * 320, 10, 1))
    platforms.append(N_Platform(500 + i * 320, 10, 2))

run = True
clock = pygame.time.Clock()

score = 0
points = 0

#=============#
# SCORE BOARD #
#=============#

# CAPITALIST: 3293
# 07RRJ: 3129
# ERROR: 3061

clock_time = 70
# while run:
for runing in range(50):
    score += int((((points) // 1000) - 40) * -2.1)
    print(runing, score, "+", int((((points) // 1000) - 40) * -2.1))
    points = 0
    # if clock_time < 110:
    clock_time += 1
    for i in range(100):
        clock.tick(35)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()

        # Horizontal player intent
        move_x = clock_time / 10

        # Simulate horizontal movement by shifting platforms
        for platform in platforms:
            platform.x -= move_x

        # Jump handling
        if not isJump and keys[pygame.K_UP]:
            isJump = True
            y_vel = -jump_power
        elif isJump and keys[pygame.K_DOWN]:
            y_vel = jump_power
            # isJump = False

        # Apply gravity
        y_vel += gravity
        y += y_vel

        points += y
        print(int(((y // 10) - 40) * -2.1))

        player_rect = pygame.Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)

        # --- Vertical collision resolution ---
        for platform in platforms:
            plat_rect = platform.rect()
            if player_rect.colliderect(plat_rect):
                if y_vel > 0 and player_rect.bottom - y_vel <= plat_rect.top:
                    y = plat_rect.top - PLAYER_HEIGHT
                    y_vel = 0
                    isJump = False
                elif y_vel < 0 and player_rect.top - y_vel >= plat_rect.bottom:
                    y = plat_rect.bottom
                    y_vel = 0

        # Horizontal collision (strong snap)
        player_rect = pygame.Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
        for platform in platforms:
            plat_rect = platform.rect()
            if player_rect.colliderect(plat_rect):
                if move_x > 0 and player_rect.right > plat_rect.left and player_rect.left < plat_rect.left:
                    # Snap back to prevent passing through left side
                    for p in platforms:
                        p.x += vel
                    break
                elif move_x < 0 and player_rect.left < plat_rect.right and player_rect.right > plat_rect.right:
                    # Snap back to prevent passing through right side
                    for p in platforms:
                        p.x -= vel
                    break

        # Floor boundary
        if y + PLAYER_HEIGHT >= HEIGHT - 10:
            y = HEIGHT - PLAYER_HEIGHT - 10
            y_vel = 0
            isJump = False

        # Drawing
        win.fill((50, 50, 50))
        pygame.draw.rect(win, COLOURS["GREEN"], pygame.Rect(0, 490, 500, 10))
        win.blit(player_img, (x, y))
        for platform in platforms:
            platform.display(win)
        pygame.display.update()

print(f"tot: {score}")

pygame.quit()