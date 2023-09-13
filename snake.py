import pygame
import random
import os

pygame.init()

# Define color constants
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
green = (0, 255, 0)

# Set up the game window
screen_width = 900
screen_height = 600
gamewindow = pygame.display.set_mode((screen_width, screen_height))

# Set the window title and update the display
pygame.display.set_caption("Snake Game")
pygame.display.update()

# Create a clock to control the frame rate
Clock = pygame.time.Clock()

# Create a font for displaying text
font = pygame.font.SysFont(None, 50)

# Function to display the score on the screen
def score_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gamewindow.blit(screen_text, [x, y])

# Load images for the apple and bonus apple
apple_img = pygame.image.load("apple.png")
apple_size = (30, 30)
apple_img = pygame.transform.scale(apple_img, apple_size)

bonus_apple_img = pygame.image.load("bonus_apple.png")
bonus_apple_img = pygame.transform.scale(bonus_apple_img, apple_size)

# Function to draw the snake on the screen
def plot_snake(gamewindow, head_color, body_color, snk_list, snake_size):
    if len(snk_list) > 0:
        # Draw the head (first segment) with head_color
        pygame.draw.rect(gamewindow, head_color, [snk_list[0][0], snk_list[0][1], snake_size, snake_size])

        # Draw the body (remaining segments) with body_color
        for i in range(1, len(snk_list)):
            pygame.draw.rect(gamewindow, body_color, [snk_list[i][0], snk_list[i][1], snake_size, snake_size])

# Main game loop
def gameloop():
    exit_game = False
    game_over = False
    snake_x = 10
    snake_y = 55
    snake_size = 25
    velocity_x = 0
    velocity_y = 0
    food_x = random.randint(0, screen_width)
    food_y = random.randint(0, screen_height)
    bonus_food_x = None
    bonus_food_y = None
    bonus_food_active = False
    score = 0
    regular_food_eaten = 0  # Track regular food items eaten
    fps = 20
    snk_list = []
    snk_length = 1

    # Check if highscore file exists, and create it if not
    if not os.path.exists("highscore.txt"):
        with open("highscore.txt", "w") as f:
            f.write("0")

    # Read the highscore from the file
    with open("highscore.txt", "r") as f:
        highscore = f.read()

    while not exit_game:
        if game_over:
            # Write the highscore to the file
            with open("highscore.txt", "w") as f:
                f.write(str(highscore))

            gamewindow.fill(black)
            score_screen("Game is over! Press Enter to continue", red, 100, 250)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        gameloop()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:   # controlling snake movement
                        velocity_x = 10
                        velocity_y = 0
                    if event.key == pygame.K_LEFT:
                        velocity_x = -10
                        velocity_y = 0
                    if event.key == pygame.K_UP:
                        velocity_y = -10
                        velocity_x = 0
                    if event.key == pygame.K_DOWN:
                        velocity_y = 10
                        velocity_x = 0

            snake_x = snake_x + velocity_x    # controlling snake movement
            snake_y = snake_y + velocity_y

            # Check if the snake has eaten regular food
            if food_x is not None and food_y is not None:
                if abs(snake_x - food_x) < 30 and abs(snake_y - food_y) < 30:
                    score += 10
                    regular_food_eaten += 1

                    if regular_food_eaten % 5 == 0:
                        # Hide regular food
                        food_x = None
                        food_y = None

                        # Update the position of bonus food
                        bonus_food_x = random.randint(0, screen_width)
                        bonus_food_y = random.randint(0, screen_height)
                        bonus_food_active = True  # Activate bonus food
                    else:
                        food_x = random.randint(0, screen_width)
                        food_y = random.randint(0, screen_height)

                    snk_length += 1



            # Check for collision with bonus food
            if bonus_food_active and abs(snake_x - bonus_food_x) < 20 and abs(snake_y - bonus_food_y) < 20:
                score += 30  # Triple the score for bonus food
                bonus_food_active = False  # Deactivate bonus food
                bonus_food_x = None
                bonus_food_y = None
                snk_length += 1

                # Regular food reappears after eating bonus food
                food_x = random.randint(0, screen_width)
                food_y = random.randint(0, screen_height)

            gamewindow.fill(white)

            if score > int(highscore):
                highscore = score

            score_screen("Score: " + str(score) + "       High Score: " + str(highscore), red, 5, 5)

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.insert(0, head)  # Insert the new head at the beginning

            # Control the snake's length by removing the tail
            if len(snk_list) > snk_length:
                del snk_list[-1]

            if head in snk_list[1:]:
                game_over = True

            if (
                    snake_x < 0
                    or snake_x > screen_width
                    or snake_y < 0
                    or snake_y > screen_height
            ):
                game_over = True

            plot_snake(gamewindow, green, black, snk_list, snake_size)

            if food_x is not None and food_y is not None:
                gamewindow.blit(apple_img, (food_x, food_y))
            if bonus_food_active:
                gamewindow.blit(bonus_apple_img, (bonus_food_x, bonus_food_y))

        pygame.display.update()
        Clock.tick(fps)

    pygame.quit()
    quit()

# Start the game loop
gameloop()
