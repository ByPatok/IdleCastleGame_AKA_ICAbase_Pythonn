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
castle_gold = 100
castle_gold_generation_rate_per_second = 2  
castle_level = 1
castle_upgrade_cost = 10

barracks = []
barracks_cost = 100
barracks_spawn_rate = 2
barracks_hp = [50] * len(barracks)
last_guard_spawn_time = time.time()

guards = []
guard_damage = 20
guard_last_attack_time = []
GUARD_SPAWN_RATE = 2

enemies = []
enemy_spawn_rate = 2
enemy_damage = 5
enemy_spawn_interval = 2
enemy_is_killed = False

enemy_xp_reward = 10
level = 1
xp = 0
xp_required = 100
xp_drop_enabled = True
XP_INCREMENT_PER_LEVEL = 100
xp_needed_for_next_level = level * XP_INCREMENT_PER_LEVEL

gold = 0

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
current_time = time.time()
last_guard_spawn_time = time.time()
last_enemy_spawn_time = time.time()
last_gold_generation_time = time.time()


# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                castle_hp = 100
                enemies = []
                gold = 0
                castle_level = 1


    current_time = time.time()
    elapsed_time = current_time - last_update_time

    if elapsed_time >= 1:
        gold_generated = int(elapsed_time * castle_gold_generation_rate_per_second)
        castle_gold += gold_generated
        last_gold_generation_time = current_time  # Update last_gold_generation_time
        last_update_time = current_time



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

    # Update game variables here

    # Def's
    def draw_info():
        text = font.render(f"Castle Level: {castle_level}", True, (0, 0, 0))
        screen.blit(text, (5, 10))
        text = font.render(f"Castle HP: {castle_hp}", True, (0, 0, 0))
        screen.blit(text, (5, 50))
        text = font.render(f"Gold: {gold}", True, (0, 0, 0))
        screen.blit(text, (5, 90))
        text = font.render(f"Upgrade Cost: {castle_upgrade_cost}", True, (0, 0, 0))
        screen.blit(text, (5, 130))
        text = font.render(f"Barrack Cost: {barracks_cost}", True, (0, 0, 0))
        screen.blit(text, (5, 170))
        text = font.render(f"Level: {level}", True, (0, 0, 0))
        screen.blit(text, (300, 10))
        text = font.render(f"XP: {xp} / {xp_needed_for_next_level}", True, (0, 0, 0))
        screen.blit(text, (300, 50))

    def draw_castle():
        pygame.draw.rect(screen, CASTLE_COLOR, (castle_x - castle_size // 2, castle_y - castle_size // 2, castle_size, castle_size))
        pygame.draw.rect(screen, (0, 0, 0), (castle_x - castle_size // 2, castle_y - castle_size // 2, castle_size, 5))
        screen.blit(castle_img, (castle_x - castle_size // 2, castle_y - castle_size // 2))

    def draw_guards():
        for guard in guards:
            guard_x, guard_y, guard_size = guard
            screen.blit(guard_img, (guard[0]- guard_size // 2, guard_y - guard_size // 2))

    def draw_barracks():
        for i, barrack in enumerate(barracks):
            screen.blit(barracks_img, (barrack[0] - castle_size // 2, barrack[1] - castle_size // 2))
            draw_health_bar(barrack[0], barrack[1] - 25, barracks_hp[i])

    def draw_health_bar(x, y, health):
        if health > 0:
            pygame.draw.rect(screen, (255, 0, 0), (x - 25, y, 50, 5))
            pygame.draw.rect(screen, (0, 128, 0), (x - 25, y, 50 * (health / 50), 5))

    def draw_enemies():
        for enemy in enemies:
            enemy[0], enemy[1], enemy_size, enemy_dmg = enemy
            screen.blit(enemy_img, (enemy[0]- enemy_size // 2, enemy[1] - enemy_size // 2))

    def calculate_xp_needed_for_next_level(current_level):
        
        return 100 * current_level

    def calculate_new_xp_threshold(current_level):
        
        return 100 * current_level

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

    # Draw everything
    screen.fill(BACKGROUND_COLOR)
    draw_info()
    draw_enemies()
    draw_guards()
    draw_barracks()
    draw_castle()
    draw_upgrade_castle_button()
    draw_create_barracks_button()

    pygame.display.update()
    clock.tick(FPS)