import pygame, sys, os, random, time
from dataclasses import dataclass

def get_game_folder():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

game_folder = get_game_folder()
images_folder = os.path.join(game_folder, "img")

pygame.init()

# Base (logical) resolution - your original game size
BASE_WIDTH, BASE_HEIGHT = 500, 500

# Set fullscreen mode with SCALED flag: auto-scales to any screen resolution
win = pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
pygame.display.set_caption("alexia run")

# Font and player size at base resolution (no manual scale)
text_font = pygame.font.SysFont("Arial", 30, bold=True)
PLAYER_SIZE = 30
player_img = pygame.image.load(os.path.join(images_folder, "player.png")).convert_alpha()
player_img = pygame.transform.scale(player_img, (PLAYER_SIZE, PLAYER_SIZE))

# Player initial position and movement variables (base resolution coordinates)
player_x = BASE_WIDTH // 10 - PLAYER_SIZE // 2
player_y = 400
vel = 5
y_vel = 0
gravity = 1
jump_power = 16
isJump = False

COLOURS = [
    (50, 170, 60),
    (60, 50, 170),
    (170, 60, 50)
]

screen_bottom = BASE_HEIGHT - BASE_HEIGHT / 25
section = screen_bottom / 10
sec = [i * section + BASE_HEIGHT / 25 for i in range(10)]

PLATFORM_Y = [
    [sec[7], sec[8], sec[9]],
    [sec[4], sec[5], sec[6]],
    [sec[1], sec[2], sec[3]]
]

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

# Generate platforms as before with base resolution coordinates
platforms = []
for i in range(2000):
    rand = [random.randint(0, 2), random.randint(0, 2), random.randint(0, 2)]
    for idx, item in enumerate(rand):
        plat_x = 500 + i * 320 if idx in (0, 2) else 660 + i * 320
        if item == 1:
            platforms.append(N_Platform(plat_x, 10, COLOURS[0], PLATFORM_Y[idx][1]))
        else:
            if random.randint(0, 1):
                platforms.append(N_Platform(plat_x, 10, COLOURS[0], PLATFORM_Y[idx][2]))
                platforms.append(N_Platform(plat_x, 10, COLOURS[0], PLATFORM_Y[idx][0]))
            else:
                platforms.append(N_Platform(plat_x, 10, COLOURS[0], PLATFORM_Y[idx][item]))

clock = pygame.time.Clock()
score = 0
points = 0
clock_time = 80
run = True

#=============#
# SCORE BOARD #
#=============#

# 07RRJ: 2006.57
# CAPITALIST: 
# ERROR: 

program_start_time = time.time()
run_time = program_start_time + 100
while run_time > program_start_time:
    run_time -= 1
    clock.tick(40)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    win.fill((50, 50, 50))
    score_text = text_font.render(f"start in: {run_time - program_start_time}", True, (255, 255, 255))
    score_rect = score_text.get_rect()
    score_rect.topright = (BASE_WIDTH / 2, BASE_HEIGHT / 2)
    win.blit(score_text, score_rect)
    pygame.display.update()

# def the_game():
for i in range(5000):
    clock.tick(40)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    move_x = clock_time / 10

    for platform in platforms:
        platform.x -= move_x

    if not isJump and keys[pygame.K_UP]:
        isJump = True
        y_vel = -jump_power
    elif isJump and keys[pygame.K_DOWN]:
        y_vel = jump_power

    y_vel += gravity

    # Simple vertical movement with collision (can add stepping logic if needed)
    player_y += y_vel
    player_rect = pygame.Rect(player_x, player_y, PLAYER_SIZE, PLAYER_SIZE)

    points += int((((BASE_HEIGHT - player_y) ** 1.12) - 100) / 1.9)

    for platform in platforms:
        plat_rect = platform.rect()
        if player_rect.colliderect(plat_rect):
            if y_vel > 0 and player_rect.bottom - y_vel <= plat_rect.top:
                player_y = plat_rect.top - PLAYER_SIZE
                y_vel = 0
                isJump = False
            elif y_vel < 0 and player_rect.top - y_vel >= plat_rect.bottom:
                player_y = plat_rect.bottom
                y_vel = 0

    # Floor boundary
    if player_y + PLAYER_SIZE >= BASE_HEIGHT - 10:
        player_y = BASE_HEIGHT - PLAYER_SIZE - 10
        y_vel = 0
        isJump = False
    elif player_y <= 10:
        player_y = 10
        y_vel = 0
        y_vel += gravity

    # Draw
    win.fill((50, 50, 50))
    floor_rect = pygame.Rect(0, BASE_HEIGHT - BASE_HEIGHT / 50, BASE_WIDTH, 10)
    ceiling_rect = pygame.Rect(0, 0, BASE_WIDTH, 10)
    pygame.draw.rect(win, COLOURS[0], floor_rect)
    pygame.draw.rect(win, COLOURS[0], ceiling_rect)
    win.blit(player_img, (player_x, player_y))
    for platform in platforms:
        platform.display(win)

    score_text = text_font.render(f"{score + points / 1000:.2f}", True, (255, 255, 255))
    score_rect = score_text.get_rect()
    score_rect.topright = (BASE_WIDTH - 20, 20)
    win.blit(score_text, score_rect)

    pygame.display.update()

for i in range(200):
    clock.tick(40)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    win.fill((50, 50, 50))
    score_text = text_font.render(f"your score: {score + points / 1000:.2f}", True, (255, 255, 255))
    score_rect = score_text.get_rect()
    score_rect.topright = (BASE_WIDTH - 20, 20)
    win.blit(score_text, score_rect)
    pygame.display.update()

pygame.quit()
print(score)