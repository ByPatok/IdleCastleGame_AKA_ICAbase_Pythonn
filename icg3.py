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

# Load and resize images
castle_img = pygame.transform.scale(pygame.image.load("castle.png"), (50, 50))
barracks_img = pygame.transform.scale(pygame.image.load("barracks.png"), (50, 50))
enemy_img = pygame.transform.scale(pygame.image.load("zombie.png"), (50, 50))
guard_img = pygame.transform.scale(pygame.image.load("guard.png"), (50, 50))
# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Idle Castle Game")

# Initialize game variables
castle_x, castle_y = WIDTH // 2, HEIGHT // 2
castle_size = 50
castle_hp = 100
castle_level = 1
castle_upgrade_cost = 10
castle_gold = 0
castle_gold_generation_rate_per_second = 2

barracks = []  # Store barracks as [x, y, size]
barracks_cost = 100
barracks_spawn_rate = 2

guards = []  # Store guards as [x, y, size, hp, damage]
guard_damage = 20
guard_cooldown = 2  # Add a cooldown for guard attacks

enemies = []  # Store enemies as [x, y, size, hp, damage]
enemy_damage = 5
enemy_spawn_interval = 2

enemy_xp_reward = 10
level = 1
xp = 0
xp_required = 100
xp_drop_enabled = True
XP_INCREMENT_PER_LEVEL = 100
xp_needed_for_next_level = level * XP_INCREMENT_PER_LEVEL

dx, dy = 0, 0

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

#def's
def draw_castle():
    pygame.draw.rect(screen, CASTLE_COLOR, (castle_x - castle_size // 2, castle_y - castle_size // 2, castle_size, castle_size))
    pygame.draw.rect(screen, (0, 0, 0), (castle_x - castle_size // 2, castle_y - castle_size // 2, castle_size, 5))
    screen.blit(castle_img), (castle_x - castle_size // 2, castle_y - castle_size // 2)

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


# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                # Reset the game
                castle_hp = 100
                enemies = []
                castle_gold = 0
                castle_level = 1
                # Reset other variables as needed

        if event.type == pygame.MOUSEBUTTONDOWN:
            if castle_upgrade_button.collidepoint(event.pos):
                if castle_gold >= castle_upgrade_cost:
                    castle_level += 1
                    castle_gold -= castle_upgrade_cost
                    castle_upgrade_cost = castle_level * 10
                    castle_gold_generation_rate_per_second = castle_level

            if create_barracks_button.collidepoint(event.pos):
                if castle_gold >= barracks_cost:
                    x, y = random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)
                    barracks.append([x, y, castle_size])
                    castle_gold -= barracks_cost

    current_time = time.time()

    # Calculate the time elapsed since the last update
    time_elapsed = current_time - last_update_time

    # Generate gold based on the castle's level and rate
    gold_generated = castle_gold_generation_rate_per_second * time_elapsed

    # Increment the castle's gold
    castle_gold += gold_generated

    # Update game variables here

    # Implement barracks spawning guards
    if (current_time - last_guard_spawn_time) >= guard_cooldown:
        for barrack in barracks:
            x, y, size = barrack
            guards.append([x, y, size, 100, guard_damage])
        last_guard_spawn_time = current_time

    # Implement enemy spawning
    if (current_time - last_enemy_spawn_time) >= enemy_spawn_interval:
        x, y = random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)
        enemies.append([x, y, 50, 100, enemy_damage])
        last_enemy_spawn_time = current_time

    # Update guards attacking enemies
    for guard in guards:
        for enemy in enemies:
            guard_x, guard_y, guard_size, guard_hp, guard_dmg = guard
            enemy_x, enemy_y, enemy_size, enemy_hp, enemy_dmg = enemy
            distance = math.sqrt((guard_x - enemy_x) ** 2 + (guard_y - enemy_y) ** 2)
            if distance <= guard_size / 2:
                if enemy_hp > 0:
                    enemy_hp -= guard_dmg
                    if enemy_hp <= 0:
                        enemies.remove(enemy)
                        xp += enemy_xp_reward

    # Update enemies attacking the castle
    for enemy in enemies:
        enemy_x, enemy_y, enemy_size, enemy_hp, enemy_dmg = enemy
        distance = math.sqrt((castle_x - enemy_x) ** 2 + (castle_y - enemy_y) ** 2)
        if distance <= castle_size / 2:
            if castle_hp > 0:
                castle_hp -= enemy_dmg
                if castle_hp <= 0:
                    # Handle game over logic
                    pass

    # Handle leveling up
    if xp >= xp_needed_for_next_level:
        xp -= xp_needed_for_next_level
        level += 1
        xp_needed_for_next_level = level * XP_INCREMENT_PER_LEVEL

    # Continue with the rest of your game logic

    # Draw everything
    screen.fill(BACKGROUND_COLOR)

    # Implement functions to draw castle, guards, barracks, enemies, info, buttons, etc.
    draw_castle()
    draw_info()
    draw_upgrade_castle_button()
    draw_create_barracks_button()

    ####
    pygame.display.update()
    clock.tick(FPS)
