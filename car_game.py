import pygame
from pygame.locals import *
import random
import sys

pygame.init()

# Create the window
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Car Game')

# Define colors
GRAY = (100, 100, 100)
GREEN = (76, 208, 56)
RED = (200, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 232, 0)

# Define road and marker sizes
ROAD_WIDTH = 300
MARKER_WIDTH = 10
MARKER_HEIGHT = 50

# Define lane coordinates
LANE_WIDTH = ROAD_WIDTH // 3
LANES = [WIDTH // 2 - ROAD_WIDTH // 2 + i * LANE_WIDTH for i in range(3)]

# Define road and edge markers
ROAD = pygame.Rect(WIDTH // 2 - ROAD_WIDTH // 2, 0, ROAD_WIDTH, HEIGHT)
LEFT_EDGE_MARKER = pygame.Rect(LANES[0] - MARKER_WIDTH, 0, MARKER_WIDTH, HEIGHT)
RIGHT_EDGE_MARKER = pygame.Rect(LANES[2], 0, MARKER_WIDTH, HEIGHT)

# Define player's car coordinates
player_x = LANE_WIDTH
player_y = HEIGHT - MARKER_HEIGHT - 20

# Initialize the clock and set the frame rate
clock = pygame.time.Clock()
FPS = 60

# Game settings
gameover = False
speed = 2
score = 0

class Vehicle(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        image = pygame.transform.scale(image, (60, 100))
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

class PlayerVehicle(Vehicle):
    def __init__(self, x, y):
        image = pygame.image.load('python-car-game-main/images/car.png')
        super().__init__(image, x, y)

# Sprite groups
player_group = pygame.sprite.Group()
vehicle_group = pygame.sprite.Group()

# Create the player's car
player = PlayerVehicle(player_x, player_y)
player_group.add(player)

# Load vehicle images
vehicle_images = [pygame.image.load('python-car-game-main/images/pickup_truck.png'),
                  pygame.image.load('python-car-game-main/images/semi_trailer.png'),
                  pygame.image.load('python-car-game-main/images/taxi.png'),
                  pygame.image.load('python-car-game-main/images/van.png')]

# Load the crash image
crash = pygame.image.load('python-car-game-main/images/crash.png')
crash_rect = crash.get_rect()

# Game loop
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_LEFT and player.rect.centerx > LANE_WIDTH:
                player.rect.x -= LANE_WIDTH
            elif event.key == K_RIGHT and player.rect.centerx < LANE_WIDTH * 3:
                player.rect.x += LANE_WIDTH

    screen.fill(GREEN)
    pygame.draw.rect(screen, GRAY, ROAD)
    pygame.draw.rect(screen, YELLOW, LEFT_EDGE_MARKER)
    pygame.draw.rect(screen, YELLOW, RIGHT_EDGE_MARKER)

    # Draw lane markers
    for y in range(-MARKER_HEIGHT * 2, HEIGHT, MARKER_HEIGHT * 2):
        for x in LANES:
            pygame.draw.rect(screen, WHITE, (x - MARKER_WIDTH // 2, y + (speed * 2) % (MARKER_HEIGHT * 2), MARKER_WIDTH, MARKER_HEIGHT))

    player_group.draw(screen)

    # Add vehicles
    if len(vehicle_group) < 2:
        add_vehicle = True
        for vehicle in vehicle_group:
            if vehicle.rect.top < vehicle.rect.height * 1.5:
                add_vehicle = False

        if add_vehicle:
            lane = random.choice(LANES)
            image = random.choice(vehicle_images)
            vehicle = Vehicle(image, lane, -60)
            vehicle_group.add(vehicle)

    # Move vehicles
    for vehicle in vehicle_group:
        vehicle.rect.y += speed
        if vehicle.rect.top >= HEIGHT:
            vehicle.kill()
            score += 1
            if score > 0 and score % 5 == 0:
                speed += 1

    vehicle_group.draw(screen)

    # Check for collisions
    if pygame.sprite.spritecollide(player, vehicle_group, False):
        gameover = True
        crash_rect.center = [player.rect.centerx, player.rect.top]

    if gameover:
        screen.blit(crash, crash_rect)
        pygame.draw.rect(screen, RED, (0, 50, WIDTH, 100))
        font = pygame.font.Font(None, 36)
        text = font.render('Game over. Play again? (Press Y or N)', True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, 100))
        screen.blit(text, text_rect)

    pygame.display.update()

    while gameover:
        for event in pygame.event.get():
            if event.type == QUIT:
                gameover = False
                running = False
            if event.type == KEYDOWN:
                if event.key == K_y:
                    gameover = False
                    speed = 2
                    score = 0
                    vehicle_group.empty()
                    player.rect.center = (LANES[0], player_y)
                elif event.key == K_n:
                    gameover = False
                    running = False

pygame.quit()
sys.exit()
