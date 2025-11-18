import pygame, sys, os, random, time
from dataclasses import dataclass

# --------------------------
# Setup
# --------------------------
def get_game_folder():
    return getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

pygame.init()
BASE_WIDTH, BASE_HEIGHT = 500, 500
win = pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
pygame.display.set_caption("Alexia run")

text_font = pygame.font.SysFont("Arial", 30, bold=True)
PLAYER_SIZE = 30

images_folder = os.path.join(get_game_folder(), "img")
player_img = pygame.image.load(os.path.join(images_folder, "player.png")).convert_alpha()
player_img = pygame.transform.scale(player_img, (PLAYER_SIZE, PLAYER_SIZE))

COLOURS = [(50, 170, 60), (60, 50, 170), (170, 60, 50)]

screen_bottom = BASE_HEIGHT - BASE_HEIGHT / 25
section = screen_bottom / 10
sec = [i * section + BASE_HEIGHT / 25 for i in range(10)]

PLATFORM_Y = [
    [sec[7], sec[8], sec[9]],
    [sec[4], sec[5], sec[6]],
    [sec[1], sec[2], sec[3]],
]

clock = pygame.time.Clock()

# --------------------------
# Classes
# --------------------------

@dataclass(slots=True)
class Button:
    text: str
    rect: pygame.Rect
    color: tuple

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        label = text_font.render(self.text, True, (255, 255, 255))
        label_rect = label.get_rect(center=self.rect.center)
        screen.blit(label, label_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

@dataclass(slots=True)
class N_Platform:
    x: float
    y: float
    colour: tuple
    rect: pygame.Rect
    def move(self, dx): 
        self.x -= dx
        self.rect.x = int(self.x)
    def draw(self, surf): 
        pygame.draw.rect(surf, self.colour, self.rect)

# --------------------------
# Generate next set of platforms dynamically
# --------------------------

def generate_platform_batch(start_index: int, count: int = 1):
    """Generate 'count' terrain chunks starting at index 'start_index'."""
    plats = []
    for i in range(start_index, start_index + count):
        rand = [random.randint(0, 2), random.randint(0, 2), random.randint(0, 2)]
        for idx, item in enumerate(rand):
            plat_x = 500 + i * 320 if idx in (0, 2) else 660 + i * 320
            if item == 1:
                y = PLATFORM_Y[idx][1]
                plats.append(N_Platform(plat_x, y, COLOURS[0], pygame.Rect(plat_x, y, 120, 5)))
            else:
                if random.randint(0, 1):
                    y1, y2 = PLATFORM_Y[idx][2], PLATFORM_Y[idx][0]
                    plats.append(N_Platform(plat_x, y1, COLOURS[0], pygame.Rect(plat_x, y1, 120, 5)))
                    plats.append(N_Platform(plat_x, y2, COLOURS[0], pygame.Rect(plat_x, y2, 120, 5)))
                else:
                    y = PLATFORM_Y[idx][item]
                    plats.append(N_Platform(plat_x, y, COLOURS[0], pygame.Rect(plat_x, y, 120, 5)))
    return plats

# --------------------------
# Main game loop with timer + dynamic terrain
# --------------------------
def the_game(run_condition):
    player_x = BASE_WIDTH // 10 - PLAYER_SIZE // 2
    player_y = 350
    y_vel = 0
    gravity = 1
    jump_power = 16
    isJump = False

    # Generate a small initial pool of terrain
    platforms = generate_platform_batch(0, 60)
    next_chunk_index = 60  # Next chunk to create

    score = 0
    start_time = time.time()
    move_x = 8
    floor_rect = pygame.Rect(0, BASE_HEIGHT - BASE_HEIGHT / 50, BASE_WIDTH, 10)
    ceiling_rect = pygame.Rect(0, 0, BASE_WIDTH, 10)

    # Track how far the player has moved horizontally
    player_move_threshold = 20  # When we should start generating platforms based on progress
    total_distance_travelled = 0  # Track how far the player has moved

    while run_condition(time.time() - start_time, score):
        clock.tick(40)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        keys = pygame.key.get_pressed()
        if not isJump and keys[pygame.K_UP]:
            isJump, y_vel = True, -jump_power
        elif isJump and keys[pygame.K_DOWN]:
            y_vel = jump_power

        y_vel += gravity
        player_y += y_vel
        player_rect = pygame.Rect(player_x, player_y, PLAYER_SIZE, PLAYER_SIZE)

        # Score system (unchanged)
        points = ((((BASE_HEIGHT - player_y) ** 1.12) - 100) / 1.9) / 1000
        score += points

        # Move + recycle platforms
        for p in platforms:
            p.move(move_x)

        # Calculate how far the player has moved (total horizontal distance)
        total_distance_travelled += move_x

        # Remove offscreen platforms and generate new ones when the player moves sufficiently
        while platforms and platforms[0].x < -200:
            platforms.pop(0)
        
        # Generate new chunks when the player has moved enough distance
        if total_distance_travelled >= player_move_threshold:
            platforms.extend(generate_platform_batch(next_chunk_index, 5))  # generate 5 new platforms
            next_chunk_index += 5  # Update the chunk index
            total_distance_travelled = 0  # Reset the distance traveled for next chunk generation

        # --- Collision detection ---
        for p in platforms:
            if player_rect.colliderect(p.rect):
                if y_vel > 0 and player_rect.bottom - y_vel <= p.rect.top:
                    player_y = p.rect.top - PLAYER_SIZE
                    y_vel = 0
                    isJump = False

        # --- Floor/ceiling bounds ---
        if player_y + PLAYER_SIZE >= BASE_HEIGHT - 10:
            player_y = BASE_HEIGHT - PLAYER_SIZE - 10
            y_vel = 0
            isJump = False
        elif player_y <= 10:
            player_y = 10
            y_vel = 0

        # --- Draw ---
        win.fill((50, 50, 50))
        pygame.draw.rect(win, COLOURS[0], floor_rect)
        pygame.draw.rect(win, COLOURS[0], ceiling_rect)
        win.blit(player_img, (player_x, player_y))
        for p in platforms:
            p.draw(win)

        # --- Score & Time (top-right corner) ---
        score_text = text_font.render(f"{points:.2f} + {score:.2f}", True, (255, 255, 255))
        win.blit(score_text, (BASE_WIDTH - 220, 20))
        elapsed = time.time() - start_time
        time_text = text_font.render(f"{elapsed:.1f}s", True, (255, 255, 255))
        win.blit(time_text, (BASE_WIDTH - 220, 50))

        pygame.display.update()

    # --- End Screen ---
    elapsed = time.time() - start_time
    win.fill((50, 50, 50))
    score_text = text_font.render(f"Your score: {score:.2f}", True, (255, 255, 255))
    time_text = text_font.render(f"It took: {elapsed:.1f}s", True, (255, 255, 255))
    win.blit(score_text, score_text.get_rect(center=(BASE_WIDTH//2, BASE_HEIGHT//2 - 30)))
    win.blit(time_text, time_text.get_rect(center=(BASE_WIDTH//2, BASE_HEIGHT//2 + 20)))
    pygame.display.flip()
    pygame.time.wait(4000)

# --------------------------
# Menu
# --------------------------
def draw_start_screen(buttons):
    win.fill((30, 30, 30))
    title = text_font.render("Alexia run", True, (255, 255, 255))
    win.blit(title, (BASE_WIDTH // 2 - title.get_width() // 2, 70))
    for btn in buttons:
        btn.draw(win)
    pygame.display.flip()


def main_menu():
    # Replace string evals with lambdas (same semantics)
    modes = [
        ("1 min", lambda t, s: t < 60),
        ("5 min", lambda t, s: t < 300),
        ("10 min", lambda t, s: t < 600),
        ("100 pt", lambda t, s: s <= 100),
        ("500 pt", lambda t, s: s <= 500),
        ("5k pt", lambda t, s: s <= 5000),
        ("infinite", lambda t, s: True)
    ]

    buttons = []
    for i, (label, _) in enumerate(modes):
        x = 50 + (i % 3) * 140
        y = 200 + (i // 3) * 100
        buttons.append(Button(label, pygame.Rect(x, y, 120, 50), COLOURS[i % 3]))

    while True:
        clock.tick(30)
        draw_start_screen(buttons)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for (label, cond), btn in zip(modes, buttons):
                    if btn.is_clicked(pos):
                        the_game(cond)

if __name__ == "__main__":
    main_menu()
