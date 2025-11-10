import pygame, sys, os, random, time
from dataclasses import dataclass

pygame.init()

BASE_WIDTH, BASE_HEIGHT = 500, 500
win = pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
pygame.display.set_caption("Alexia Run")

text_font = pygame.font.SysFont("Arial", 30, bold=True)
clock = pygame.time.Clock()

COLOURS = [(50, 170, 60), (60, 50, 170), (170, 60, 50)]

@dataclass
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

def draw_start_screen(buttons):
    win.fill((30, 30, 30))
    title = text_font.render("Select Game Mode", True, (255, 255, 255))
    win.blit(title, (BASE_WIDTH // 2 - title.get_width() // 2, 70))
    for btn in buttons:
        btn.draw(win)
    pygame.display.flip()

def the_game(mode):
    start_time = pygame.time.get_ticks()
    countdown = 3
    run = True
    while run:
        clock.tick(40)
        win.fill((50, 50, 50))
        elapsed = (pygame.time.get_ticks() - start_time) / 1000
        if elapsed < countdown:
            text = text_font.render(f"Starting in: {countdown - int(elapsed)}", True, (255, 255, 255))
            win.blit(text, (BASE_WIDTH // 2 - text.get_width() // 2, BASE_HEIGHT // 2))
        else:
            # Example gameplay placeholder
            text = text_font.render(f"Game started! Mode: {mode}", True, (255, 255, 255))
            win.blit(text, (BASE_WIDTH // 2 - text.get_width() // 2, BASE_HEIGHT // 2))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    pygame.quit()
    sys.exit()

# Create six buttons in two rows of three
buttons = []
for i in range(9):
    x = 80 + (i % 3) * 140
    y = 200 + (i // 3) * 100
    buttons.append(Button(f"Mode {i+1}", pygame.Rect(x, y, 120, 50), COLOURS[i % 3]))

# ====== MENU LOOP ======
selected_mode = None
while not selected_mode:
    clock.tick(30)
    draw_start_screen(buttons)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for i, btn in enumerate(buttons):
                if btn.is_clicked(pos):
                    selected_mode = i + 1
the_game(selected_mode)