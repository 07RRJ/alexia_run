import pygame, sys, os, random
from dataclasses import dataclass, field

def get_game_folder():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

game_folder = get_game_folder()
images_folder = os.path.join(game_folder, "img")

pygame.init()

# Window setup
text_font = pygame.font.SysFont("Arial", 30, bold=True)
WIDTH, HEIGHT = 500, 500
SCALE = HEIGHT // 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("alexia run")

# Player image load
PLAYER_WIDTH, PLAYER_HEIGHT = 30, 30
player_img = pygame.image.load(os.path.join(images_folder, "player.png")).convert_alpha()
# player_img = pygame.image.load(os.path.join(images_folder, "monek.png")).convert_alpha()
# player_img = pygame.image.load(os.path.join(images_folder, "monkey.svg")).convert_alpha()
player_img = pygame.transform.scale(player_img, (PLAYER_WIDTH, PLAYER_HEIGHT))

# Player fixed horizontal position (centered)
player_x = WIDTH // 10 - PLAYER_WIDTH // 2
player_y = 400
vel = 5
y_vel = 0
gravity = 1
jump_power = 16
isJump = False

COLOURS = [
    (50, 170, 60),  # GREEN
    (60, 50, 170),  # BLUE
    (170, 60, 50)   # RED
]

screen = HEIGHT - HEIGHT / 25
section = screen / 10
sec = []

for i in range(10):
    sec.append(i * section + HEIGHT / 25)

PLATFORM_Y = [
    [sec[7], sec[8], sec[9]],
    [sec[4], sec[5], sec[6]],
    [sec[1], sec[2], sec[3]]]

@dataclass
class N_Platform:
    x: int
    width: int
    colour: int
    y: int

    def rect(self):
        height = 5
        width = 120

        return pygame.Rect(self.x, self.y, width, height)

    def display(self, screen):
        pygame.draw.rect(screen, self.colour, self.rect())

# Initial platforms
platforms = []

# random.seed(7)

for i in range(2000): 
    rand = [random.randint(0, 2), random.randint(0, 2), random.randint(0, 2)] 
    for idx, item in enumerate(rand): 
        if idx == 0 or idx == 2: 
            plat_x = 500 + i * 320 
        else: 
            plat_x = 660 + i * 320 
        if item == 1: 
            platforms.append(N_Platform(plat_x, 10, COLOURS[0], PLATFORM_Y[idx][1])) 
        else: 
            if random.randint(0, 1): 
                platforms.append(N_Platform(plat_x, 10, COLOURS[0], PLATFORM_Y[idx][2])) 
                platforms.append(N_Platform(plat_x, 10, COLOURS[0], PLATFORM_Y[idx][0])) 
            else: 
                platforms.append(N_Platform(plat_x, 10, COLOURS[0], PLATFORM_Y[idx][item]))

run = True
clock = pygame.time.Clock()

score = 0
points = 0

clock_time = 80

#=============#
# SCORE BOARD #
#=============#

# without roof
# 07RRJ: 3558
# CAPITALIST: 3293
# ERROR: 3061

# with roof
# 07RRJ: 1988
# CAPITALIST: 
# ERROR: 

for runing in range(50):
    score += points // 1000
    points = 0
    
    if clock_time < 120:
        clock_time += 1
    for i in range(100):
        clock.tick(40)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
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

        # Apply gravity
        y_vel += gravity
        player_y += y_vel

        points += int(((((HEIGHT - player_y) // SCALE) ** 1.12) - 100) / 1.9)

        player_rect = pygame.Rect(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT)

        # --- Vertical collision resolution ---
        for platform in platforms:
            plat_rect = platform.rect()
            if player_rect.colliderect(plat_rect):
                if y_vel > 0 and player_rect.bottom - y_vel <= plat_rect.top:
                    player_y = plat_rect.top - PLAYER_HEIGHT
                    y_vel = 0
                    isJump = False
                elif y_vel < 0 and player_rect.top - y_vel >= plat_rect.bottom:
                    player_y = plat_rect.bottom
                    y_vel = 0

        # Horizontal collision (strong snap)
        player_rect = pygame.Rect(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT)
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
        if player_y + PLAYER_HEIGHT >= HEIGHT - 10:
            player_y = HEIGHT - PLAYER_HEIGHT - 10
            y_vel = 0
            isJump = False
        elif player_y <= 10:
            player_y = 10
            y_vel = 0
            y_vel += gravity

        # Drawing
        win.fill((50, 50, 50))
        pygame.draw.rect(win, COLOURS[0], pygame.Rect(0, HEIGHT - HEIGHT / 50, 500, 10))
        pygame.draw.rect(win, COLOURS[0], pygame.Rect(0, 0, HEIGHT, 10))
        win.blit(player_img, (player_x, player_y))
        for platform in platforms:
            platform.display(win)

        # Render and blit score text here
        text = text_font.render(f"{score + points / 1000:.2f}", True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.topright = (WIDTH - 10, 10)
        win.blit(text, text_rect)

        pygame.display.update()

print(f"tot: {score}")

pygame.quit()