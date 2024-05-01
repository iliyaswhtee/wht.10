# Import modules
import pygame
import random
import psycopg2

# Initialize Pygame
pygame.init()

# Database connection parameters
DB_NAME = "database_name"
DB_USER = "database_user"
DB_PASSWORD = "database_password"
DB_HOST = "database_host"
DB_PORT = "5432"

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)
cursor = conn.cursor()

# Game settings
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
SNAKE_SPEED = 10
LEVEL_UP_SCORE = 3  # Score needed to level up

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Function to register a new user or get user ID if already exists
def register_or_get_user(username):
    try:
        cursor.execute("INSERT INTO user (username) VALUES (%s) RETURNING id", (username,))
        user_id = cursor.fetchone()[0]
        conn.commit()
        print("User registered successfully with ID:", user_id)
        return user_id
    except psycopg2.IntegrityError:
        conn.rollback()
        cursor.execute("SELECT id FROM user WHERE username = %s", (username,))
        row = cursor.fetchone()
        if row:
            return row[0]
        else:
            print("Error: Unable to register user or fetch user information")
            return None

# Function to save game state (score and level) to the database
def save_game_state(user_id, score, level):
    try:
        cursor.execute("INSERT INTO user_score (user_id, score, level) VALUES (%s, %s, %s)", (user_id, score, level))
        conn.commit()
        print("Game state saved successfully")
    except psycopg2.Error as e:
        conn.rollback()
        print("Error:", e)

# Function to retrieve user scores from the database
def get_user_scores(user_id):
    cursor.execute("SELECT score, level FROM user_score WHERE user_id = %s ORDER BY level", (user_id,))
    rows = cursor.fetchall()
    if rows:
        print("User scores:")
        for row in rows:
            print("Level:", row[1], "- Score:", row[0])
    else:
        print("No scores found for the user")

# Initialize game variables
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Get username from the user
username = input("Enter your username: ")
user_id = register_or_get_user(username)

# Exit if user registration or retrieval fails
if not user_id:
    pygame.quit()
    quit()

# Snake position in the space 
snake = [(WIDTH // 2, HEIGHT // 2)]
food = (random.randint(0, WIDTH // GRID_SIZE - 1) *  GRID_SIZE, random.randint(0, HEIGHT // GRID_SIZE - 1) *  GRID_SIZE)
score = 0
level = 1  # Add level variable
direction = 'RIGHT'

# Main game loop
while True:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Save game state before quitting
            save_game_state(user_id, score, level)
            pygame.quit()
            quit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and direction != 'DOWN':
        direction = 'UP'
    if keys[pygame.K_DOWN] and direction != 'UP':
        direction = 'DOWN'
    if keys[pygame.K_LEFT] and direction != 'RIGHT':
        direction = 'LEFT'
    if keys[pygame.K_RIGHT] and direction != 'LEFT':
        direction = 'RIGHT'

    # Move the snake
    x, y = snake[0]
    if direction == 'UP':
        y -= GRID_SIZE
    if direction == 'DOWN':
        y += GRID_SIZE
    if direction == 'LEFT':
        x -= GRID_SIZE
    if direction == 'RIGHT':
        x += GRID_SIZE

    # Check for collision with walls or itself
    if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT or (x, y) in snake:
        # Save game state before quitting
        save_game_state(user_id, score, level)
        pygame.quit()
        quit()

    snake.insert(0, (x, y))

    # Check if snake eats the food
    if (x, y) == food:
        score += 1
        food = (random.randint(0, WIDTH // GRID_SIZE - 1) *  GRID_SIZE, random.randint(0, HEIGHT // GRID_SIZE - 1) *  GRID_SIZE)
        # Level up if score is high enough
        if score % LEVEL_UP_SCORE == 0:
            level += 1
    else:
        snake.pop()

    # Draw the snake
    for s in snake:
        pygame.draw.rect(screen, GREEN, (s[0], s[1], GRID_SIZE, GRID_SIZE))

    # Draw the food
    pygame.draw.rect(screen, RED, (food[0], food[1], GRID_SIZE, GRID_SIZE))

    # Display the score and level
    font = pygame.font.SysFont(None, 30)
    score_text = font.render("Score: " + str(score), True, (0, 0, 0))
    level_text = font.render("Level: " + str(level), True, (0, 0, 0))  # Add level display
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 40))  # Adjust position for level display

    pygame.display.update()
    clock.tick(SNAKE_SPEED + level)  # Increase speed with level