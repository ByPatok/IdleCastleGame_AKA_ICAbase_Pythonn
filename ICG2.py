import pygame
import sys
import random
import time
import math

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
pygame.display.set_caption("Idle Castle Game v2")

# Load and resize images
castle_img = pygame.transform.scale(pygame.image.load("castle.png"), (50, 50))
barracks_img = pygame.transform.scale(pygame.image.load("barracks.png"), (50, 50))
enemy_img = pygame.transform.scale(pygame.image.load("zombie.png"), (50, 50))
guard_img = pygame.transform.scale(pygame.image.load("guard.png"), (50, 50))

# Initialize game variables
castle_x = WIDTH // 2
castle_y = HEIGHT // 2
castle_size = 50
castle_hp = 100
castle_gold_generation_rate_per_second = 2
castle_level = 1
castle_upgrade_cost = 10
castle_gold = 0 

barracks = []
barracks_cost = 100
barracks_spawn_rate = 2
barracks_hp = [50] * len(barracks)

guards = []
guard_damage = 20
guard_last_attack_time = [0] * len(guards)
GUARD_SPAWN_RATE = 2

enemies = []
enemy_spawn_rate = 2
enemy_damage = 5
enemy_spawn_interval = 2
enemy_is_killed = False
enemy_xp_reward = 10
enemy_speed = 1  

level = 1
xp = 0
xp_required = 100
xp_drop_enabled = True
XP_INCREMENT_PER_LEVEL = 100
xp_needed_for_next_level = level * XP_INCREMENT_PER_LEVEL

ENEMY_ATTACK_COOLDOWN = 1.0 
GUARD_ATTACK_COOLDOWN = 1.0


# Load the font
font = pygame.font.Font(None, 36)

# Game clock
clock = pygame.time.Clock()

# Buttons
castle_upgrade_button = pygame.Rect(10, 390, 150, 40)
create_barracks_button = pygame.Rect(10, 440, 150, 40)

# Time tracking
last_update_time = time.time()
last_guard_spawn_time = time.time()
last_enemy_spawn_time = time.time()

# Def's

def draw_health_bar(x, y, health):
    if health > 0:
        pygame.draw.rect(screen, (255, 0, 0), (x - 25, y, 50, 5))
        pygame.draw.rect(screen, (0, 128, 0), (x - 25, y, 50 * (health / 50), 5))

def draw_castle():
    pygame.draw.rect(screen, CASTLE_COLOR, (castle_x - castle_size // 2, castle_y - castle_size // 2, castle_size, castle_size))
    pygame.draw.rect(screen, (0, 0, 0), (castle_x - castle_size // 2, castle_y - castle_size // 2, castle_size, 5))
    screen.blit(castle_img, (castle_x - castle_size // 2, castle_y - castle_size // 2))

def draw_info():
    text = font.render(f"Castle Level: {castle_level}", True, (0, 0, 0))
    screen.blit(text, (5, 10))
    text = font.render(f"Castle HP: {castle_hp}", True, (0, 0, 0))
    screen.blit(text, (5, 50))
    text = font.render(f"Gold: {castle_gold}", True, (0, 0, 0))
    screen.blit(text, (5, 90))
    text = font.render(f"Upgrade Cost: {castle_upgrade_cost}", True, (0, 0, 0))
    screen.blit(text, (5, 130))
    text = font.render(f"Barrack Cost: {barracks_cost}", True, (0, 0, 0))
    screen.blit(text, (5, 170))
    text = font.render(f"Level: {level}", True, (0, 0, 0))
    screen.blit(text, (300, 10))
    text = font.render(f"XP: {xp} / {xp_required}", True, (0, 0, 0))
    screen.blit(text, (300, 50))

def draw_create_barracks_button():
    create_barracks_button.topleft = (10, HEIGHT - 50)
    pygame.draw.rect(screen, (0, 0, 0), create_barracks_button)
    pygame.draw.rect(screen, (200, 200, 200), create_barracks_button.inflate(-5, -5))
    text = font.render("Create Barracks", True, (0, 0, 0))
    screen.blit(text, create_barracks_button.move(10, 0))

def draw_upgrade_castle_button():
    castle_upgrade_button.topleft = (10, HEIGHT - 100)
    pygame.draw.rect(screen, (0, 0, 0), castle_upgrade_button)
    pygame.draw.rect(screen, (255, 255, 255), castle_upgrade_button.inflate(-5, -5))
    text = font.render("Upgrade Castle", True, (0, 0, 0))
    screen.blit(text, castle_upgrade_button.move(0, 0))

def move_towards_target(x1, y1, x2, y2, speed):
    
    angle = math.atan2(y2 - y1, x2 - x1)
    x1 += speed * math.cos(angle)
    y1 += speed * math.sin(angle)
    return x1, y1

def attack(target, damage):
    
    target[2] -= damage
    if target[2] <= 0:
        
        if target in enemies:
            enemies.remove(target)
        elif target in guards:
            guards.remove(target)


# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                # Reset the game
                castle_hp = 100
                castle_gold = 0
                enemies = []
                gold = 0
                castle_level = 1

        if event.type == pygame.MOUSEBUTTONDOWN:
            if castle_upgrade_button.collidepoint(event.pos):
                if gold >= castle_upgrade_cost:
                    castle_level += 1
                    gold -= castle_upgrade_cost
                    castle_upgrade_cost = castle_level * 10
                    castle_gold_generation_rate_per_second = castle_level

            if create_barracks_button.collidepoint(event.pos):
                if gold >= barracks_cost:
                    x, y = random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)
                    barracks.append([x, y, castle_size])
                    gold -= barracks_cost

    current_time = time.time()

    # Calculate distances from enemies to the castle and attack if near
    for enemy in enemies:
        enemy_x, enemy_y, _, _ = enemy
        distance = math.sqrt((castle_x - enemy_x) ** 2 + (castle_y - enemy_y) ** 2)

        if distance < castle_size / 2:
            if current_time - enemy_last_attack_time >= ENEMY_ATTACK_COOLDOWN:
                castle_hp -= enemy_damage
                enemy_last_attack_time = current_time

    # Calculate distances from guards to enemies and attack if near
    for guard in guards:
        guard_x, guard_y, _, _ = guard
        closest_enemy = None
        min_distance = float("inf")

        for enemy in enemies:
            enemy_x, enemy_y, _, _ = enemy
            distance = math.sqrt((guard_x - enemy_x) ** 2 + (guard_y - enemy_y) ** 2)

            if distance < min_distance:
                min_distance = distance
                closest_enemy = enemy

        if closest_enemy and min_distance < castle_size * 2:
            if current_time - guard_last_attack_time[guards.index(guard)] >= GUARD_ATTACK_COOLDOWN:
                attack(closest_enemy, guard_damage)
                guard_last_attack_time[guards.index(guard)] = current_time

    # Update enemy positions to move towards the castle
    for enemy in enemies:
        enemy[0], enemy[1] = move_towards_target(enemy[0], enemy[1], castle_x, castle_y, enemy_speed)




    # Draw everything
    screen.fill(BACKGROUND_COLOR)
    
    # Draw game elements
    for barrack in barracks:
        x, y, size = barrack
        pygame.draw.rect(screen, BARRACKS_COLOR, (x - size // 2, y - size // 2, size, size))
    
    for guard in guards:
        x, y, size = guard
        screen.blit(guard_img, (x - size // 2, y - size // 2))
    
    for enemy in enemies:
        x, y, size, health = enemy
        screen.blit(enemy_img, (x - size // 2, y - size // 2))
        draw_health_bar(x, y - size // 2 - 10, health)
    
    draw_castle()
    draw_info()
    draw_upgrade_castle_button()
    draw_create_barracks_button()

    pygame.display.update()
    last_update_time = current_time
    clock.tick(FPS)
