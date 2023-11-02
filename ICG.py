import pygame
import sys
import random
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (135, 206, 235)
CASTLE_COLOR = (255, 0, 0)
BARRACKS_COLOR = (0, 128, 0)
ENEMY_COLOR = (0, 0, 255)
FPS = 30

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Idle Castle Game")

# Load and resize images
castle_img = pygame.transform.scale(pygame.image.load("castle.png"), (50, 50))
barracks_img = pygame.transform.scale(pygame.image.load("barracks.png"), (50, 50))
enemy_img = pygame.transform.scale(pygame.image.load("duck.png"), (50, 50))

# Castle properties
castle_x = WIDTH // 2
castle_y = HEIGHT // 2
castle_size = 50
castle_level = 1
castle_upgrade_cost = 10
castle_gold_generation_rate = 1  # Initial gold generation rate
castle_hp = 100

# Barracks properties
barracks = []
barracks_hp = []  
barracks_cost = 100
barracks_spawn_rate = 2  # Spawn a guard every 2 seconds
last_guard_spawn_time = time.time()
guard_damage = 10

# Enemy properties
enemies = []
enemy_spawn_rate = 2  # Spawn an enemy every 2 seconds
last_enemy_spawn_time = time.time()
enemy_damage = 10

# Gold properties
gold = 0

# Load the font
font = pygame.font.Font(None, 36)

# Game clock
clock = pygame.time.Clock()

# Buttons
castle_upgrade_button = pygame.Rect(10, 390, 150, 40)
upgrade_castle_button = pygame.Rect(10, 390, 150, 40)
create_barracks_button = pygame.Rect(10, 440, 150, 40)

def draw_castle():
    pygame.draw.rect(screen, CASTLE_COLOR, (castle_x - castle_size // 2, castle_y - castle_size // 2, castle_size, castle_size))
    pygame.draw.rect(screen, (0, 0, 0), (castle_x - castle_size // 2, castle_y - castle_size // 2, castle_size, 5))
    screen.blit(castle_img, (castle_x - castle_size // 2, castle_y - castle_size // 2))
    health_bar_width = castle_size
    health_bar_height = 5
    health_bar_x = castle_x - castle_size // 2
    health_bar_y = castle_y - castle_size // 2 - health_bar_height
    pygame.draw.rect(screen, (0, 255, 0), (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
    remaining_hp = max(0, castle_hp)
    pygame.draw.rect(screen, (255, 0, 0), (health_bar_x + remaining_hp, health_bar_y, health_bar_width - remaining_hp, health_bar_height))

def spawn_barracks():
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    barracks.append([x, y, castle_size])
    barracks_hp.append(50)  # Initialize barracks health

def draw_enemies():
    for enemy in enemies:
        screen.blit(enemy_img, (enemy[0] - castle_size // 2, enemy[1] - castle_size // 2))

def draw_info():
    text = font.render(f"Castle Level: {castle_level}", True, (0, 0, 0))
    screen.blit(text, (10, 10))
    text = font.render(f"Gold: {gold}", True, (0, 0, 0))
    screen.blit(text, (10, 50))
    text = font.render(f"Upgrade Cost: {castle_upgrade_cost}", True, (0, 0, 0))
    screen.blit(text, (10, 90))
    text = font.render(f"Castle HP: {castle_hp}", True, (0, 0, 0))
    screen.blit(text, (10, 130))

def draw_barracks_info():
    text = font.render(f"Barracks Cost: {barracks_cost}", True, (0, 0, 0))
    screen.blit(text, (10, 170))
    text = font.render(f"Barracks Spawn Rate: {barracks_spawn_rate} guards/min", True, (0, 0, 0))
    screen.blit(text, (10, 210))

def draw_barracks():
    for i in range(len(barracks)):
        x, y, size = barracks[i]
        hp = barracks_hp[i]
        pygame.draw.rect(screen, BARRACKS_COLOR, (x - size // 2, y - size // 2, size, size))
        pygame.draw.rect(screen, (0, 0, 0), (x - size // 2, y - size // 2, size, 5))
        pygame.draw.rect(screen, (0, 255, 0), (x - size // 2, y - size // 2, size * (hp / 50), 5))

def spawn_barracks():
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    barracks.append([x, y, castle_size])
    barracks_hp.append(50)  # Initialize barracks health

def draw_create_barracks_button():
    pygame.draw.rect(screen, (0, 0, 0), create_barracks_button)
    pygame.draw.rect(screen, (255, 255, 255), create_barracks_button.inflate(-5, -5))
    text = font.render("Create Barracks", True, (0, 0, 0))
    screen.blit(text, create_barracks_button.move(10, 0))

def draw_upgrade_castle_button():
    pygame.draw.rect(screen, (0, 0, 0), upgrade_castle_button)
    pygame.draw.rect(screen, (255, 255, 255), upgrade_castle_button.inflate(-5, -5))
    text = font.render("Upgrade Castle", True, (0, 0, 0))
    screen.blit(text, upgrade_castle_button.move(10, 0))

def spawn_enemy():
    side = random.choice(["top", "bottom", "left", "right"])
    if side == "top":
        x = random.randint(0, WIDTH)
        y = -castle_size // 2
    elif side == "bottom":
        x = random.randint(0, WIDTH)
        y = HEIGHT + castle_size // 2
    elif side == "left":
        x = -castle_size // 2
        y = random.randint(0, HEIGHT)
    else:
        x = WIDTH + castle_size // 2
        y = random.randint(0, HEIGHT)
    enemies.append([x, y, castle_size, enemy_damage])

def spawn_guard():
    side = random.choice(["top", "bottom", "left", "right"])
    if side == "top":
        x = random.randint(0, WIDTH)
        y = -castle_size // 2
    elif side == "bottom":
        x = random.randint(0, WIDTH)
        y = HEIGHT + castle_size // 2
    elif side == "left":
        x = -castle_size // 2
        y = random.randint(0, HEIGHT)
    else:
        x = WIDTH + castle_size // 2
        y = random.randint(0, HEIGHT)
    barracks.append([x, y, castle_size])
    barracks_hp.append(50)  # Initialize barracks health


# Main game loop
last_update_time = time.time()
last_enemy_spawn_time = time.time()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if castle_upgrade_button.collidepoint(event.pos):
                if gold >= castle_upgrade_cost:
                    gold -= castle_upgrade_cost
                    castle_level += 1
                    castle_upgrade_cost = castle_level * 10
                    castle_gold_generation_rate = castle_level  # Update gold generation rate

            if create_barracks_button.collidepoint(event.pos):
                if gold >= barracks_cost:
                    gold -= barracks_cost
            if current_time - last_barracks_spawn_time >= barracks_spawn_rate:
                spawn_barracks()
                last_barracks_spawn_time = current_time

    spawn_guard()
    for i in range(len(barracks)):
        # Check if the barracks is destroyed
        if barracks_hp[i] <= 0:
            barracks.pop(i)
            barracks_hp.pop(i)
            break

    current_time = time.time()
    time_elapsed = current_time - last_update_time

    if time_elapsed >= 1:
        gold += castle_gold_generation_rate  # Update gold generation based on the castle's level
        last_update_time = current_time

    if current_time - last_enemy_spawn_time >= enemy_spawn_rate:
        spawn_enemy()
        last_enemy_spawn_time = current_time

    for enemy in enemies:
        enemy_x, enemy_y, enemy_size, enemy_dmg = enemy
        if castle_x - castle_size // 2 < enemy_x < castle_x + castle_size // 2 and castle_y - castle_size // 2 < enemy_y < castle_y + castle_size // 2:
            castle_hp -= enemy_dmg
            enemies.remove(enemy)

    for barrack in barracks:
        barrack_x, barrack_y, barrack_size = barrack
        for enemy in enemies:
            enemy_x, enemy_y, enemy_size, enemy_dmg = enemy
            if barrack_x - barrack_size // 2 < enemy_x < barrack_x + barrack_size // 2 and barrack_y - barrack_size // 2 < enemy_y < barrack_y + barrack_size // 2:
                gold += enemy_dmg
                enemies.remove(enemy)
                break

    enemies = [enemy for enemy in enemies if 0 <= enemy[0] <= WIDTH and 0 <= enemy[1] <= HEIGHT]

    screen.fill(BACKGROUND_COLOR)
    draw_create_barracks_button()
    draw_barracks_info()
    draw_info()
    draw_enemies()
    draw_barracks()
    draw_castle()
    draw_upgrade_castle_button()

    pygame.display.update()
    clock.tick(FPS)