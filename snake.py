import pygame
import time
import random

# Initialize Pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

# Screen dimensions
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Snake settings
snake_block = 10
snake_speed = 15

# Clock
clock = pygame.time.Clock()

# Font
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Function to display the score
def show_score(score):
    value = score_font.render(f"Your Score: {score}", True, WHITE)
    screen.blit(value, [0, 0])

# Function to draw the snake
def draw_snake(snake_block, snake_list):
    for block in snake_list:
        pygame.draw.rect(screen, GREEN, [block[0], block[1], snake_block, snake_block])

# Function to display a message
def message(msg, color, pos):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, pos)

# Function to display the start screen
def start_screen():
    screen.fill(BLUE)
    message("Welcome to Snake Game!", WHITE, [WIDTH / 6, HEIGHT / 3])
    message("Press S to Start or Q to Quit", WHITE, [WIDTH / 6, HEIGHT / 2])
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    waiting = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

# Main game loop
def game_loop():
    game_over = False
    game_close = False

    # Starting position for the snake
    x = WIDTH / 2
    y = HEIGHT / 2

    # Initial movement
    x_change = 0
    y_change = 0

    # Snake body
    snake_list = []
    length_of_snake = 1

    # Generate food
    food_x = round(random.randrange(0, WIDTH - snake_block) / 10.0) * 10.0
    food_y = round(random.randrange(0, HEIGHT - snake_block) / 10.0) * 10.0

    while not game_over:

        # Game over screen
        while game_close:
            screen.fill(BLACK)
            message("You Lost! Press Q-Quit or C-Play Again", RED, [WIDTH / 6, HEIGHT / 3])
            show_score(length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -snake_block
                    y_change = 0
                elif event.key == pygame.K_RIGHT:
                    x_change = snake_block
                    y_change = 0
                elif event.key == pygame.K_UP:
                    y_change = -snake_block
                    x_change = 0
                elif event.key == pygame.K_DOWN:
                    y_change = snake_block
                    x_change = 0

        # Update snake position
        if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0:
            game_close = True
        x += x_change
        y += y_change

        screen.fill(BLUE)

        # Draw food
        pygame.draw.rect(screen, RED, [food_x, food_y, snake_block, snake_block])

        # Update snake
        snake_head = [x, y]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        # Check for collisions with itself
        for block in snake_list[:-1]:
            if block == snake_head:
                game_close = True

        draw_snake(snake_block, snake_list)
        show_score(length_of_snake - 1)

        pygame.display.update()

        # Check if the snake ate food
        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, WIDTH - snake_block) / 10.0) * 10.0
            food_y = round(random.randrange(0, HEIGHT - snake_block) / 10.0) * 10.0
            length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

# Start the game with the start screen
start_screen()
game_loop()
