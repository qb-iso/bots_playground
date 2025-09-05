import pygame
import random
import sys

# --- Settings ---
GRID_SIZE = 40
CELL_SIZE = 19
MENU_HEIGHT = 40
WINDOW_WIDTH = GRID_SIZE * CELL_SIZE
WINDOW_HEIGHT = GRID_SIZE * CELL_SIZE + MENU_HEIGHT
FPS = 8

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
MENU_COLOR = (180, 180, 250)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 255, 0)
RED = (255, 0, 0)

# --- Manhattan Dist ---
def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# --- Init ---
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)

# --- Helpers ---
def draw_text(text, pos, color=BLACK):
    screen.blit(font.render(text, True, color), pos)

def draw_button(rect, text, color=GRAY):
    pygame.draw.rect(screen, color, rect)
    draw_text(text, (rect.x + 8, rect.y + 6))

def draw_menu_bar():
    pygame.draw.rect(screen, MENU_COLOR, (0, 0, WINDOW_WIDTH, MENU_HEIGHT))

def draw_grid():
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (x, MENU_HEIGHT), (x, WINDOW_HEIGHT))
    for y in range(MENU_HEIGHT, WINDOW_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (0, y), (WINDOW_WIDTH, y))

def draw_snake(snake):
    for i, seg in enumerate(snake):
        color = DARK_GREEN if i == 0 else GREEN
        pygame.draw.rect(screen, color, (seg[0]*CELL_SIZE, seg[1]*CELL_SIZE + MENU_HEIGHT, CELL_SIZE, CELL_SIZE))

def place_food(snake):
    while True:
        fx = random.randint(0, GRID_SIZE - 1)
        fy = random.randint(0, GRID_SIZE - 1)
        if (fx, fy) not in snake:
            return (fx, fy)

# --- Screens (single event loop per frame, no doubling) ---

def game_loop():
    snake = [(GRID_SIZE//2, GRID_SIZE//2)]
    direction = (1, 0)
    food = place_food(snake)
    show_dropdown = False

    while True:
        clock.tick(FPS)

        # Precompute rects (we can test clicks against these rects)
        menu_btn = pygame.Rect(10, 5, 100, 30)
        exit_btn = pygame.Rect(WINDOW_WIDTH - 120, 5, 100, 30)
        dropdown_rect = pygame.Rect(10, MENU_HEIGHT, 200, 30)

        # --- Events ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and direction != (0, 1):
                    direction = (0, -1)
                elif event.key == pygame.K_s and direction != (0, -1):
                    direction = (0, 1)
                elif event.key == pygame.K_a and direction != (1, 0):
                    direction = (-1, 0)
                elif event.key == pygame.K_d and direction != (-1, 0):
                    direction = (1, 0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                # Menu click toggle
                if menu_btn.collidepoint(mx, my):
                    show_dropdown = not show_dropdown
                # Dropdown item
                elif show_dropdown and dropdown_rect.collidepoint(mx, my):
                    print("Nagini Activation clicked!")
                    show_dropdown = False
                # Exit button
                elif exit_btn.collidepoint(mx, my):
                    pygame.quit(); sys.exit()

        # --- Update game state (move snake) ---
        head_x, head_y = snake[0]
        dx, dy = direction
        new_head = ((head_x + dx) % GRID_SIZE, (head_y + dy) % GRID_SIZE)

        if new_head in snake:
            # Game over: return to menu (caller can handle)
            return len(snake)

        snake.insert(0, new_head)
        if new_head == food:
            food = place_food(snake)
        else:
            snake.pop()

        # --- Draw ---
        screen.fill(WHITE)
        draw_menu_bar()
        draw_button(menu_btn, "Menu ▾")
        if show_dropdown:
            pygame.draw.rect(screen, GRAY, dropdown_rect)
            draw_text("Nagini Activation", (dropdown_rect.x + 8, dropdown_rect.y + 6))
        draw_button(exit_btn, "EXIT")
        draw_grid()
        draw_snake(snake)
        pygame.draw.rect(screen, RED, (food[0]*CELL_SIZE, food[1]*CELL_SIZE + MENU_HEIGHT, CELL_SIZE, CELL_SIZE))
        
        pygame.display.update()

def train_screen():
    show_dropdown = False
    while True:
        clock.tick(FPS)

        menu_btn = pygame.Rect(10, 5, 100, 30)
        exit_btn = pygame.Rect(WINDOW_WIDTH//2 - 80, WINDOW_HEIGHT//2 + 60, 160, 50)
        dropdown_rect = pygame.Rect(10, MENU_HEIGHT, 200, 30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if menu_btn.collidepoint(mx, my):
                    show_dropdown = not show_dropdown
                elif show_dropdown and dropdown_rect.collidepoint(mx, my):
                    print("Nagini Activation clicked!")
                    show_dropdown = False
                elif exit_btn.collidepoint(mx, my):
                    pygame.quit(); sys.exit()

        screen.fill(WHITE)
        draw_menu_bar()
        draw_button(menu_btn, "Menu ▾")
        if show_dropdown:
            pygame.draw.rect(screen, GRAY, dropdown_rect)
            draw_text("Nagini Activation", (dropdown_rect.x + 8, dropdown_rect.y + 6))

        draw_text("hello world", (WINDOW_WIDTH//2 - 60, WINDOW_HEIGHT//2 - 10))
        draw_button(exit_btn, "EXIT")
        pygame.display.update()

def main_menu():
    show_dropdown = False
    while True:
        clock.tick(FPS)

        menu_btn = pygame.Rect(10, 5, 100, 30)
        start_btn = pygame.Rect(WINDOW_WIDTH//2 - 80, WINDOW_HEIGHT//2 - 60, 160, 50)
        exit_btn = pygame.Rect(WINDOW_WIDTH//2 - 80, WINDOW_HEIGHT//2 + 20, 160, 50)
        train_btn = pygame.Rect(WINDOW_WIDTH//2 - 80, WINDOW_HEIGHT//2 + 100, 160, 50)
        dropdown_rect = pygame.Rect(10, MENU_HEIGHT, 200, 30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if menu_btn.collidepoint(mx, my):
                    show_dropdown = not show_dropdown
                elif show_dropdown and dropdown_rect.collidepoint(mx, my):
                    print("Nagini Activation clicked!")
                    show_dropdown = False
                elif start_btn.collidepoint(mx, my):
                    score = game_loop()
                    print("Game Over! Score:", score)
                    # back to menu automatically
                elif exit_btn.collidepoint(mx, my):
                    pygame.quit(); sys.exit()
                elif train_btn.collidepoint(mx, my):
                    train_screen()

        screen.fill(WHITE)
        draw_menu_bar()
        draw_button(menu_btn, "Menu ▾")
        if show_dropdown:
            pygame.draw.rect(screen, GRAY, dropdown_rect)
            draw_text("Nagini Activation", (dropdown_rect.x + 8, dropdown_rect.y + 6))

        draw_button(start_btn, "START")
        draw_button(exit_btn, "EXIT")
        draw_button(train_btn, "TRAIN")
        pygame.display.update()

# --- Run ---
if __name__ == "__main__":
    main_menu()
