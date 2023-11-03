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
MAX_GUARDS_PER_BARRACK = 4

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

guards = []  # Store guards as [x, y, size, hp, damage, cooldown_timer]
barracks_positions = []
guard_dmg = 20
guard_cooldown = 1
guard_cooldown_timer = 0

enemies = []  # Store enemies as [x, y, size, hp, damage]
enemy_damage = 1
enemy_spawn_interval = 2
enemy_hp = 30

enemy_xp_reward = 10
level = 1
xp = 0
xp_required = 100
xp_drop_enabled = True
XP_INCREMENT_PER_LEVEL = 100
xp_needed_for_next_level = level * XP_INCREMENT_PER_LEVEL

step_size = 2 


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
    pygame.draw.rect(screen, (255, 0, 0), (castle_x - castle_size // 2, castle_y - castle_size // 2, castle_size, castle_size))
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

def draw_barracks():
    for barrack in barracks:
        x, y, size, remaining_guards = barrack  # Unpack x, y, size, and remaining_guards
        pygame.draw.rect(screen, BARRACKS_COLOR, (x - size // 2, y - size // 2, size, size))
        screen.blit(barracks_img, (x - size // 2, y - size // 2))

def draw_guards():
    for guard in guards:
        x, y, size, hp, damage, cooldown_timer = guard
        pygame.draw.rect(screen, (0, 255, 0), (x - size // 2, y - size // 2, size, size))
        screen.blit(guard_img, (x - size // 2, y - size // 2))

def create_barracks(castle_gold):
    x, y = random.randint(castle_x - 100, castle_x + 100), random.randint(castle_y - 100, castle_y + 100)
    if castle_x - 100 <= x <= castle_x + 100 and castle_y - 100 <= y <= castle_y + 100:
        for _ in range(4):  # Create 4 guards per barracks
            guards.append([x, y, castle_size, 100, guard_dmg, 0])  # Cooldown timer starts at 0
        castle_gold -= barracks_cost
    return castle_gold

def draw_enemies():
    for enemy in enemies:
        enemy_x, enemy_y, enemy_size, enemy_hp, enemy_dmg = enemy
        pygame.draw.rect(screen, ENEMY_COLOR, (enemy_x - enemy_size // 2, enemy_y - enemy_size // 2, enemy_size, enemy_size))
        screen.blit(enemy_img, (enemy_x - enemy_size // 2, enemy_y - enemy_size // 2))



# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                # Reset the game
                castle_hp = 100
                enemies = []
                castle_gold = 0
                castle_level = 1
                barracks = []
                barracks_positions = []

        if event.type == pygame.MOUSEBUTTONDOWN:
            if castle_upgrade_button.collidepoint(event.pos):
                if castle_gold >= castle_upgrade_cost:
                    castle_level += 1
                    castle_gold -= castle_upgrade_cost
                    castle_upgrade_cost = castle_level * 10
                    castle_gold_generation_rate_per_second = castle_level

            if create_barracks_button.collidepoint(event.pos):
                if castle_gold >= barracks_cost:
                    castle_gold = create_barracks(castle_gold)

    current_time = time.time()

    # Calculate the time elapsed since the last update
    time_elapsed = current_time - last_update_time

    # Generate gold based on the castle's level and rate
    gold_generated = castle_gold_generation_rate_per_second * time_elapsed

    # Increment the castle's gold
    castle_gold += gold_generated

    # Implement barracks spawning guards
    if (current_time - last_guard_spawn_time) >= guard_cooldown:
        for barrack in barracks:
            x, y, size, remaining_guards = barrack
            if remaining_guards > 0:
                for _ in range(min(4, remaining_guards)):  # Spawn up to 4 guards per barracks
                    guards.append([x, y, 100, guard_dmg, guard_cooldown])
                    remaining_guards -= 1  # Reduce the remaining guards count for the barracks
        last_guard_spawn_time = current_time

            # Count the number of guards spawned from this barrack
        guards_spawned = 0

            # Find available barrack positions
        available_positions = list(barracks_positions)

    for guard in guards:
        guard_x, guard_y, guard_size, guard_hp, guard_dmg, guard_cooldown_timer = guard

        # Check if the guard's cooldown timer is zero
        if guard_cooldown_timer <= 0:
            nearest_enemy = None
            min_distance = float('inf')

            for enemy in enemies:
                enemy_x, enemy_y, enemy_size, enemy_hp, enemy_dmg = enemy
                distance = math.sqrt((guard_x - enemy_x) ** 2 + (guard_y - enemy_y) ** 2)

                if distance < min_distance:
                    nearest_enemy = enemy
                    min_distance = distance

            if nearest_enemy is not None:
                enemy_x, enemy_y, enemy_size, enemy_hp, enemy_dmg = nearest_enemy

                # Calculate the direction vector
                dx = enemy_x - guard_x
                dy = enemy_y - guard_y

                # Calculate the unit vector
                distance = math.sqrt(dx ** 2 + dy ** 2)
                if distance > 0:
                    dx /= distance
                    dy /= distance

                # Increase the step size for faster movement
                step_size = 2

                # Move the guard in the direction of the nearest enemy
                guard_x += dx * step_size
                guard_y += dy * step_size

                # Update the guard's position in the current guard list
                guard[0] = guard_x
                guard[1] = guard_y

                # Update the guard's cooldown timer
                guard_cooldown_timer = guard_cooldown

        else:
            # Decrease the guard's cooldown timer
            guard_cooldown_timer -= time_elapsed

    # Update the guard's cooldown timer
    if guard_cooldown_timer > 0:
        guard_cooldown_timer -= time_elapsed
    # Implement enemy spawning
    if (current_time - last_enemy_spawn_time) >= enemy_spawn_interval:
        x, y = random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)
        enemies.append([x, y, 50, 100, enemy_damage])
        last_enemy_spawn_time = current_time

    # Update guards attacking enemies
    for enemy in enemies:
        enemy_x, enemy_y, enemy_size, enemy_hp, enemy_dmg = enemy
        distance = math.sqrt((castle_x - enemy_x) ** 2 + (castle_y - enemy_y) ** 2)

        if distance <= castle_size / 2:
            if castle_hp > 0:
                castle_hp -= enemy_dmg
                if castle_hp <= 0:
                    # Handle game over logic
                    pass
        else:
            # Calculate the direction vector
            dx = castle_x - enemy_x
            dy = castle_y - enemy_y

            # Calculate the unit vector
            distance = math.sqrt(dx ** 2 + dy ** 2)
            if distance > 0:
                dx /= distance
                dy /= distance

            # Move the enemy in the direction of the castle
            enemy_x += dx
            enemy_y += dy

            # Update the enemy's position
            enemy[0] = enemy_x
            enemy[1] = enemy_y

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
    draw_barracks()
    draw_guards()
    draw_enemies()

    ####
    pygame.display.update()
    clock.tick(FPS)
