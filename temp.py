import pygame, sys, os, random
from dataclasses import dataclass

def get_game_folder():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

game_folder = get_game_folder()
images_folder = os.path.join(game_folder, "img")

pygame.init()

# Detect display and set fullscreen
display_info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = display_info.current_w, display_info.current_h
BASE_WIDTH, BASE_HEIGHT = 500, 500

# Scaling factors
scale_x = SCREEN_WIDTH / BASE_WIDTH
scale_y = SCREEN_HEIGHT / BASE_HEIGHT
scale_avg = (scale_x + scale_y) / 2

# Set fullscreen window
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("alexia run")

# Font scaled
font_size = int(30 * scale_avg)
text_font = pygame.font.SysFont("Arial", font_size, bold=True)

# Player setup (scaled)
PLAYER_HEIGHT = int(30 * scale_y)
PLAYER_WIDTH = PLAYER_HEIGHT
player_img = pygame.image.load(os.path.join(images_folder, "player.png")).convert_alpha()
player_img = pygame.transform.scale(player_img, (PLAYER_WIDTH, PLAYER_HEIGHT))

# Player initial position and movement variables
player_x = int((BASE_WIDTH // 10 - PLAYER_WIDTH // 2) * scale_x)
player_y = int(400 * scale_y)
vel = 5 * scale_x
y_vel = 0
gravity = 1 * scale_y
jump_power = 16 * scale_y
isJump = False

COLOURS = [
    (50, 170, 60),  # GREEN
    (60, 50, 170),  # BLUE
    (170, 60, 50)   # RED
]

screen_bottom = SCREEN_HEIGHT - SCREEN_HEIGHT / 25
section = screen_bottom / 10
sec = [i * section + SCREEN_HEIGHT / 25 for i in range(10)]

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
        height = int(5 * scale_y)
        width = int(120 * scale_x)
        return pygame.Rect(self.x, self.y, width, height)

    def display(self, screen):
        pygame.draw.rect(screen, self.colour, self.rect())

# Create random platforms
platforms = []
for i in range(2000):
    rand = [random.randint(0, 2), random.randint(0, 2), random.randint(0, 2)]
    for idx, item in enumerate(rand):
        plat_x = int((500 + i * 320) * scale_x) if idx in (0, 2) else int((660 + i * 320) * scale_x)
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

# Main loop
for runing in range(50):
    score += points // 1000
    points = 0
    # if clock_time < 120:
    #     clock_time += 1

    for i in range(100):
        clock.tick(40)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        move_x = clock_time / 10 * scale_x

        for platform in platforms:
            platform.x -= move_x

        if not isJump and keys[pygame.K_UP]:
            isJump = True
            y_vel = -jump_power
        elif isJump and keys[pygame.K_DOWN]:
            y_vel = jump_power

        y_vel += gravity
        player_y += y_vel
        points += int(((((SCREEN_HEIGHT - player_y) / scale_avg) ** 1.12) - 100) / 1.9)

        player_rect = pygame.Rect(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT)

        # Collision detection (vertical)
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

        # Collision (horizontal)
        for platform in platforms:
            plat_rect = platform.rect()
            if player_rect.colliderect(plat_rect):
                if move_x > 0 and player_rect.right > plat_rect.left and player_rect.left < plat_rect.left:
                    for p in platforms:
                        p.x += vel
                    break
                elif move_x < 0 and player_rect.left < plat_rect.right and player_rect.right > plat_rect.right:
                    for p in platforms:
                        p.x -= vel
                    break

        # Floor boundaries
        if player_y + PLAYER_HEIGHT >= SCREEN_HEIGHT - 10:
            player_y = SCREEN_HEIGHT - PLAYER_HEIGHT - 10
            y_vel = 0
            isJump = False
        elif player_y <= 10:
            player_y = 10
            y_vel = 0
            y_vel += gravity

        # Drawing
        win.fill((50, 50, 50))
        floor_rect = pygame.Rect(0, SCREEN_HEIGHT - SCREEN_HEIGHT / 100, SCREEN_WIDTH, 10)
        ceiling_rect = pygame.Rect(0, 0, SCREEN_WIDTH, 10)
        pygame.draw.rect(win, COLOURS[0], floor_rect)
        pygame.draw.rect(win, COLOURS[0], ceiling_rect)
        win.blit(player_img, (player_x, player_y))
        for platform in platforms:
            platform.display(win)

        # Score
        text = text_font.render(f"{score + points / 1000:.2f}", True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.topright = (SCREEN_WIDTH - 20, 20)
        win.blit(text, text_rect)

        pygame.display.update()

pygame.quit()
print(f"Total score: {score}")
