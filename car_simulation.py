import pygame
import sys
import random

# =========================
# INITIALIZE PYGAME
# =========================

pygame.init()

# =========================
# SCREEN SETTINGS
# =========================

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Self Driving Car Simulation")

# =========================
# COLORS
# =========================

BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# =========================
# CLOCK
# =========================

clock = pygame.time.Clock()

# =========================
# FONT
# =========================

font = pygame.font.SysFont(None, 36)

# =========================
# LOAD IMAGES
# =========================

player_img = pygame.image.load("assets/cc2.webp")
player_img = pygame.transform.scale(player_img, (50, 80))

traffic_img = pygame.image.load("assets/cc1.jpg")
traffic_img = pygame.transform.scale(traffic_img, (50, 80))

# =========================
# LANE POSITIONS
# =========================

lanes = [250, 375, 500]

# =========================
# PLAYER CAR
# =========================

car_x = 375
car_y = 500
car_width = 50
car_height = 80

# =========================
# TRAFFIC CARS
# =========================

traffic = []

for i in range(3):

    traffic.append({
        "x": random.choice(lanes),
        "y": random.randint(-600, -100),
        "speed": random.randint(6, 10)
    })

# =========================
# SCORE
# =========================

score = 0

# =========================
# AI MODE
# =========================

ai_mode = False

# =========================
# TRAFFIC LIGHT SYSTEM
# =========================

traffic_light = "GREEN"
light_timer = 0

# =========================
# GAME LOOP
# =========================

running = True

while running:

    # Background
    screen.fill(GRAY)

    # Road
    pygame.draw.rect(screen, BLACK, (175, 0, 450, 600))

    # Lane lines
    pygame.draw.line(screen, WHITE, (325, 0), (325, 600), 5)
    pygame.draw.line(screen, WHITE, (475, 0), (475, 600), 5)

    # =========================
    # TRAFFIC LIGHTS
    # =========================

    light_timer += 1

    if light_timer < 300:
        traffic_light = "GREEN"

    elif light_timer < 450:
        traffic_light = "YELLOW"

    elif light_timer < 700:
        traffic_light = "RED"

    else:
        light_timer = 0

    # Traffic light box
    pygame.draw.rect(screen, BLACK, (650, 50, 80, 200))

    # Red light
    pygame.draw.circle(screen, RED, (690, 90), 25)

    # Yellow light
    pygame.draw.circle(screen, YELLOW, (690, 150), 25)

    # Green light
    pygame.draw.circle(screen, GREEN, (690, 210), 25)

    # Light text
    light_text = font.render(
        traffic_light,
        True,
        WHITE
    )

    screen.blit(light_text, (630, 270))

    # =========================
    # PLAYER CAR
    # =========================

    player = screen.blit(
        player_img,
        (car_x, car_y)
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

        obstacle = screen.blit(
            traffic_img,
            (car["x"], car["y"])
        )

        # Move traffic only if not red light
        if traffic_light != "RED":
            car["y"] += car["speed"]

        # Reset traffic
        if car["y"] > HEIGHT:

            car["y"] = random.randint(-300, -100)
            car["x"] = random.choice(lanes)

            score += 1

        # Collision detection
        obstacle_rect = pygame.Rect(
            car["x"],
            car["y"],
            50,
            80
        )

        player_rect = pygame.Rect(
            car_x,
            car_y,
            50,
            80
        )

        if player_rect.colliderect(obstacle_rect):

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

    # =========================
    # KEYBOARD INPUT
    # =========================

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

                    # Intelligent lane switching
                    if car_x == 250:
                        car_x = 375

                    elif car_x == 375:
                        car_x = 500

                    else:
                        car_x = 250

    # =========================
    # SCORE DISPLAY
    # =========================

    score_text = font.render(
        f"Score: {score}",
        True,
        WHITE
    )

    screen.blit(score_text, (20, 20))

    # =========================
    # MODE DISPLAY
    # =========================

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

    # =========================
    # UPDATE SCREEN
    # =========================

    pygame.display.update()

    # FPS
    clock.tick(60)

# =========================
# QUIT GAME
# =========================

pygame.quit()
sys.exit()