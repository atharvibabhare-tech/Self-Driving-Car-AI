import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen settings
WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Self Driving Car Simulation")

# Colors
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Clock
clock = pygame.time.Clock()

# Font
font = pygame.font.SysFont(None, 36)

# Lane positions
lanes = [250, 375, 500]

# Player car
car_x = 375
car_y = 500
car_width = 50
car_height = 80

# Traffic cars
traffic = []

for i in range(3):

    traffic.append({
        "x": random.choice(lanes),
        "y": random.randint(-600, -100),
        "speed": random.randint(6, 10)
    })

# Score
score = 0

# AI Mode
ai_mode = False

# Game loop
running = True

while running:

    # Background
    screen.fill(GRAY)

    # Road
    pygame.draw.rect(screen, BLACK, (175, 0, 450, 600))

    # Lane lines
    pygame.draw.line(screen, WHITE, (325, 0), (325, 600), 5)
    pygame.draw.line(screen, WHITE, (475, 0), (475, 600), 5)

    # Player car
    player = pygame.draw.rect(
        screen,
        RED,
        (car_x, car_y, car_width, car_height)
    )

    # =========================
    # AI SENSORS
    # =========================

    if ai_mode:

        # Front sensor
        pygame.draw.line(
            screen,
            GREEN,
            (car_x + 25, car_y),
            (car_x + 25, car_y - 150),
            3
        )

        # Left sensor
        pygame.draw.line(
            screen,
            GREEN,
            (car_x, car_y + 20),
            (car_x - 100, car_y - 80),
            3
        )

        # Right sensor
        pygame.draw.line(
            screen,
            GREEN,
            (car_x + 50, car_y + 20),
            (car_x + 150, car_y - 80),
            3
        )

    # =========================
    # DRAW TRAFFIC
    # =========================

    for car in traffic:

        obstacle = pygame.draw.rect(
            screen,
            BLUE,
            (car["x"], car["y"], 50, 80)
        )

        # Move traffic
        car["y"] += car["speed"]

        # Reset traffic
        if car["y"] > HEIGHT:

            car["y"] = random.randint(-300, -100)
            car["x"] = random.choice(lanes)

            score += 1

        # Collision detection
        if player.colliderect(obstacle):

            game_over = font.render(
                "GAME OVER",
                True,
                WHITE
            )

            screen.blit(game_over, (280, 250))

            pygame.display.update()

            pygame.time.delay(2000)

            running = False

    # =========================
    # EVENTS
    # =========================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # Toggle AI mode
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_a:
                ai_mode = not ai_mode

    # Keyboard input
    keys = pygame.key.get_pressed()

    # =========================
    # HUMAN MODE
    # =========================

    if not ai_mode:

        if keys[pygame.K_LEFT]:

            if car_x > 250:
                car_x -= 125

        if keys[pygame.K_RIGHT]:

            if car_x < 500:
                car_x += 125

    # =========================
    # AI MODE
    # =========================

    else:

        for car in traffic:

            # Detect nearby traffic
            if car["y"] > 250:

                # Same lane
                if car_x == car["x"]:

                    # Move intelligently
                    if car_x == 250:
                        car_x = 375

                    elif car_x == 375:
                        car_x = 500

                    else:
                        car_x = 250

    # Score display
    score_text = font.render(
        f"Score: {score}",
        True,
        WHITE
    )

    screen.blit(score_text, (20, 20))

    # Mode display
    if ai_mode:
        mode = "MODE: AI"
        mode_color = GREEN
    else:
        mode = "MODE: HUMAN"
        mode_color = WHITE

    mode_text = font.render(
        mode,
        True,
        mode_color
    )

    screen.blit(mode_text, (20, 60))

    # Instructions
    instruction = font.render(
        "Press A to Toggle AI",
        True,
        WHITE
    )

    screen.blit(instruction, (20, 100))

    # Update screen
    pygame.display.update()

    # FPS
    clock.tick(60)

pygame.quit()
sys.exit()