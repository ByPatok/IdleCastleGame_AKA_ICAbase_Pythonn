import pygame
import sys
import random
import time
import math

# Initialize Pygame
pygame.init()

enemy_xp_reward = 10
level = 1
xp = 0
xp_required = 100
xp_drop_enabled = True
XP_INCREMENT_PER_LEVEL = 100
xp_needed_for_next_level = level * XP_INCREMENT_PER_LEVEL

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
enemy_img = pygame.transform.scale(pygame.image.load("zombie.png"), (50, 50))
guard_img = pygame.transform.scale(pygame.image.load("guard.png"), (50, 50)) 

# Castle properties
castle_x = WIDTH // 2
castle_y = HEIGHT // 2
castle_size = 50
castle_level = 1
castle_upgrade_cost = 10
castle_gold_generation_rate_per_second = 2
castle_hp = 100

# Barracks properties
barracks = []
barracks_cost = 100
barracks_spawn_rate = 2
barracks_hp = [50] * len(barracks)
last_guard_spawn_time = time.time()

guard_damage = 20
guards = []
guard_last_attack_time = []
GUARD_SPAWN_RATE = 2


# Enemy properties
enemies = []
enemy_spawn_rate = 2
enemy_damage = 5
if enemies:  
    enemies[0] = (enemies[0][0], enemies[0][1], enemies[0][2], 30)
enemy_spawn_interval = 2
enemy_is_killed = False

# Gold properties
gold = 0

# Load the font
font = pygame.font.Font(None, 36)

# Game clock
clock = pygame.time.Clock()

# Buttons
castle_upgrade_button = pygame.Rect(10, 390, 150, 40)
create_barracks_button = pygame.Rect(10, 440, 150, 40)


dx, dy = 0, 0


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

barracks_positions = []

create_barracks_button = pygame.Rect(10, 440, 150, 40)
castle_upgrade_button = pygame.Rect(10, 490, 150, 40)

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

def spawn_enemy():
    x = random.randint(50, WIDTH - 50)
    y = random.randint(50, HEIGHT - 50)
    enemy = [x, y, castle_size, enemy_damage, time.time()] 
    enemies.append(enemy)
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


def spawn_guard(barracks, barrack_index):
    guard_x = barrack_x + offset_x
    guard_y = barrack_y + offset_y
    guard_size = 10
    guards.append([guard_x, guard_y, guard_size])
    guard_last_attack_time.append(current_time)
    barrack_x, barrack_y, barrack_size = barracks[barrack_index]  

    offset_x = random.randint(-barrack_size // 2, barrack_size // 2)
    offset_y = random.randint(-barrack_size // 2, barrack_size // 2)

    guard_x = barrack_x + offset_x
    guard_y = barrack_y + offset_y
    guard_size = 10

    guards.append([guard_x, guard_y, guard_size])
    barracks_hp[barrack_index] -= 10  

    if barracks_hp[barrack_index] <= 0:
        barracks.pop(barrack_index) 




def move_guards_towards_enemy(guard, enemy):
    guard_x, guard_y, guard_size = guard
    enemy[0], enemy[1], enemy_size, enemy_dmg = enemy

    dx = enemy[0]- guard_x
    dy = enemy[1] - guard_y
    distance = (dx ** 2 + dy ** 2) ** 0.5

    if distance > 0:
        speed = 1  
        direction_x = dx / distance
        direction_y = dy / distance

        new_x = guard[0]+ speed * direction_x
        new_y = guard_y + speed * direction_y

        return [new_x, new_y, guard_size]
    return guard



last_barracks_spawn_time = 0

def create_barracks():
    global gold
    if gold >= barracks_creation_cost:
        barracks.append([random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50), castle_size])
        barracks_hp.append(50)  
        gold -= barracks_creation_cost
        barracks_creation_cost += 50  
        spawn_guard(barracks, -1) 


barracks_creation_cost = 100 
def draw_barracks_creation_cost():
    text = font.render(f"Barracks Cost: {barracks_creation_cost} Gold", True, (0, 0, 0))
    screen.blit(text, (10, 170))

def spawn_barracks():
    x = random.randint(0, WIDTH - castle_size)
    y = random.randint(0, HEIGHT - castle_size)
    barracks.append([x, y, castle_size])
    barracks_hp.append(50)

def update_castle_health():
    global castle_hp
    for enemy in enemies:
        enemy[0], enemy[1], enemy_size, enemy_dmg = enemy
        dx = castle_x - enemy_x
        dy = castle_y - enemy[1]
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance < castle_size + enemy_size:
            castle_hp -= enemy_dmg

            if castle_hp <= 0:
                castle_hp = 0
                print("Castle destroyed!")

    i = 0
    while i < len(guards):
        j = 0
        while j < len(enemies):
            guard = guards[i]
            enemy = enemies[j]
            guard_x, guard_y, guard_size = guard
            enemy[0], enemy[1], enemy_size, enemy_dmg = enemy
            dx = guard[0]- enemy_x
            dy = guard_y - enemy[1]
            distance = math.sqrt(dx ** 2 + dy ** 2)

            if distance < guard_size + enemy_size:
               
                guards[i] = [guard_x, guard_y, guard_size - enemy_dmg]  
                if guards[i][2] <= 0:
                    guards.pop(i)
                    i -= 1
                
                enemies[j] = [enemy_x, enemy[1], enemy_size, enemy_dmg - guard_damage]  
                if enemies[j][3] <= 0:
                    enemies.pop(j)
                j += 1
            else:
                j += 1
        i += 1


GUARD_ATTACK_COOLDOWN = 1.0 
ENEMY_ATTACK_COOLDOWN = 1.5  
guard_last_attack_time = [0] * len(guards)
enemy_last_attack_time = [time.time() for _ in enemies]

                

def game_over_screen():
    screen.fill(BACKGROUND_COLOR)
    game_over_text = font.render("Game Over", True, (255, 0, 0))
    restart_text = font.render("Press 'R' to Restart", True, (0, 0, 0))
    screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
    screen.blit(restart_text, (WIDTH // 2 - 100, HEIGHT // 2 + 10))
    pygame.display.update()

def reset_game():
    global castle_hp, enemies, gold, castle_level
    castle_hp = 100  
    enemies = []  
    gold = 0  
    castle_level = 1  

def check_enemy_collisions():
    for enemy in enemies:
        enemy[0], enemy[1], enemy_size, enemy_dmg = enemy

if enemies:  
    dx = castle_x - enemies[0][0]
    dy = castle_y - enemies[0][1]


distance = math.sqrt(dx ** 2 + dy ** 2)

if castle_hp <= 0:
    castle_hp = 0
    game_over_screen()

# Main game loop
last_update_time = time.time()
current_time = time.time()
time_elapsed = current_time - last_update_time
if time_elapsed >= 1:
    gold += castle_gold_generation_rate_per_second
    last_update_time = current_time
last_guard_spawn_time = time.time()
last_enemy_spawn_time = time.time()
barracks_hp = [] 


mouse_pos = (0, 0)
while True:
    update_castle_health()
    if castle_hp <= 0:
        game_over_screen()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_game()
        current_time = time.time()
        guards_to_remove = [] 
        for i, guard in enumerate(guards):
            if current_time - guard_last_attack_time[i] >= GUARD_ATTACK_COOLDOWN:
                 for j, enemy in enumerate(enemies):
                    guard_x, guard_y, guard_size = guard
                    enemy_x, enemy[1], enemy_size, enemy_dmg = enemy
                    dx = guard_x - enemy_x
                    dy = guard_y - enemy[1]
                    distance = math.sqrt(dx ** 2 + dy ** 2)
                    guard_last_attack_time[i] = current_time
                    if distance < guard_size + enemy_size:
                        
                        guards[i] = [guard_x, guard_y, guard_size - enemy_dmg]  
                        if guards[i][2] <= 0:
                            guards_to_remove.append(i)
                        
                        enemies[j] = [enemy_x, enemy[1], enemy_size, enemy_dmg - guard_damage]  
                        if enemies[j][3] <= 0:
                            enemies.pop(j)
                        guard_last_attack_time[i] = current_time
        for i in guards_to_remove:
            if i < len(guards):
                guards.pop(i)
                guard_last_attack_time.pop(i)
        enemies_to_remove = []  
        current_time = time.time()
        enemies_to_remove = []  
        for i, enemy in enumerate(enemies):
            if current_time - enemy_last_attack_time[i] >= ENEMY_ATTACK_COOLDOWN:
                enemy_x, enemy[1], _, _ = enemy  
                for j, guard in enumerate(guards):
                    guard_x, guard_y, guard_size = guard
                    if (
                        guard_x - guard_size // 2 < enemy[0] < guard_x + guard_size // 2
                        and guard_y - guard_size // 2 < enemy[1] < guard_y + guard_size // 2
                    ):
                        
                        enemy[3] = max(0, enemy[3] - guard_damage)
                        if enemy[3] <= 0:
                            enemies_to_remove.append(i)
                        enemy_last_attack_time[i] = current_time    
        for i in reversed(enemies_to_remove):
            if i < len(enemies):
                enemies.pop(i)
                enemy_last_attack_time.pop(i)
        for i in enemies_to_remove:
            if i < len(enemies):
                enemies.pop(i)

        for i in range(len(guards) - 1, -1, -1):
            for j, enemy in enumerate(enemies):
                guard = guards[i]
                guard_x, guard_y, guard_size = guard
                enemy_x, enemy[1], enemy_size, enemy_dmg = enemy
                dx = enemy_x - guard_x
                dy = enemy[1] - guard_y
                distance = math.sqrt(dx ** 2 + dy ** 2)

                if distance < guard_size + enemy_size:
                    
                    guards[i] = [guard_x, guard_y, guard_size - enemy_dmg]  
                    if guards[i][2] <= 0:
                        guards.pop(i)
                        break

        enemies = [enemy for enemy in enemies if enemy[3] > 0]

        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if castle_upgrade_button.collidepoint(event.pos):
                if gold >= castle_upgrade_cost:
                    castle_level += 1
                    gold -= castle_upgrade_cost
                    castle_upgrade_cost = castle_level * 10
                    castle_gold_generation_rate_per_second = castle_level
                    print(f"Castle Level: {castle_level}, Gold Gen Rate: {castle_gold_generation_rate_per_second}")
            if create_barracks_button.collidepoint(event.pos):
                if gold >= barracks_cost:
                    x, y = random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)
                    barracks.append([x, y, castle_size])
                    barracks_hp.append(50)  
                    gold -= barracks_cost
                    barracks_positions.append((x, y))
                if gold >= barracks_cost:
                    spawn_barracks()
                    gold -= barracks_cost
            if create_barracks_button.collidepoint(event.pos):
                if gold >= barracks_cost:
                    x, y = random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)
                    barracks.append([x, y, castle_size])
                    gold -= barracks_cost
                    barracks_positions.append((x, y))

        if event.type == pygame.MOUSEBUTTONDOWN and xp_button.collidepoint(event.pos):
            xp_drop_enabled = not xp_drop_enabled

    text = font.render(f"Level: {level}", True, (0, 0, 0))
    screen.blit(text, (5, 10))
    text = font.render(f"XP: {xp}/{xp_required}", True, (0, 0, 0))
    screen.blit(text, (5, 50))

    xp_button = pygame.Rect(700, 10, 90, 30)
    pygame.draw.rect(screen, (0, 0, 0), xp_button)
    text = font.render("XP Drop: ON" if xp_drop_enabled else "XP Drop: OFF", True, (255, 255, 255))
    screen.blit(text, (700, 15))

    for enemy in enemies:
        if enemy[3] <= 0:  
            xp += enemy_xp_reward
        if xp >= xp_needed_for_next_level:
            level += 1
            xp = 0
            xp_needed_for_next_level = calculate_xp_needed_for_next_level(level)


    if enemy_is_killed:
        xp += enemy_xp_reward
        if xp >= xp_required:
            level += 1
            xp = 0
            xp_required = calculate_xp_needed_for_next_level(level)
        enemy_is_killed = False

    if xp >= xp_required:
        level += 1
        xp -= xp_required
        xp_required = calculate_new_xp_threshold(level)


        if event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos
        draw_create_barracks_button()
    current_time = time.time()
    time_elapsed = current_time - last_update_time
    if time_elapsed >= 1:
        gold += barracks_spawn_rate + castle_gold_generation_rate_per_second
        last_update_time = current_time

    if current_time - last_guard_spawn_time >= GUARD_SPAWN_RATE:
        for barrack in barracks:
            if random.random() < 0.2:
                spawn_guard(barracks, len(barracks) - 1)  
        last_guard_spawn_time = current_time

    if current_time - last_enemy_spawn_time >= enemy_spawn_interval:
        spawn_enemy()
        last_enemy_spawn_time = current_time

    if current_time - last_barracks_spawn_time >= barracks_spawn_rate:
        spawn_barracks()
    last_barracks_spawn_time = current_time

    for guard in guards:
        current_time = time.time()
        for i, guard in enumerate(guards):
            if current_time - guard_last_attack_time[i] >= GUARD_ATTACK_COOLDOWN:
                for j, enemy in enumerate(enemies):
                    guard_x, guard_y, guard_size = guard
                    enemy_x, enemy[1], enemy_size, enemy_dmg = enemy
                    dx = guard_x - enemy_x
                    dy = guard_y - enemy[1]
                    distance = math.sqrt(dx ** 2 + dy ** 2)

                    if distance < guard_size + enemy_size:
                        # Reduce guard HP and remove them if their HP drops to zero
                        guards[i] = [guard_x, guard_y, guard_size - enemy_dmg]  # Reduce guard HP
                        if guards[i][2] <= 0:
                            guards.pop(i)
                            guard_last_attack_time.pop(i)
                        # Reduce enemy HP and remove them if their HP drops to zero
                        enemies[j] = [enemy_x, enemy[1], enemy_size, enemy_dmg - guard_damage]  # Reduce enemy HP
                        if enemies[j][3] <= 0:
                            enemies.pop(j)
                        guard_last_attack_time[i] = current_time
        
        for enemy in enemies:
            guard = move_guards_towards_enemy(guard, enemy)


    for enemy in enemies:
        enemy_x, enemy_y, enemy_size, enemy_damage = enemy
        for guard in guards:
            guard_x, guard_y, guard_size = guard
            if (
                guard[0]- guard_size // 2 < enemy[0]< guard[0]+ guard_size // 2
                and guard_y - guard_size // 2 < enemy[1] < guard_y + guard_size // 2
            ):
                enemy[3] = max(0, enemy[3] - guard_damage)

                if enemy[3] <= 0:
                    enemies.remove(enemy)
                    enemy_is_killed = True

    for enemy in enemies:
        if enemy[3] <= 0:  
            xp += enemy_xp_reward
    if xp >= xp_needed_for_next_level:
        level += 1
        xp = 0
        xp_needed_for_next_level = calculate_xp_needed_for_next_level(level)


    for barrack in barracks:
        barrack_x, barrack_y, barrack_size = barrack
        for enemy in enemies:
            enemy_x, enemy_y, enemy_size, enemy_damage = enemy
            if barrack_x - barrack_size // 2 < enemy[0]< barrack_x + barrack_size // 2 and barrack_y - barrack_size // 2 < enemy[1] < barrack_y + barrack_size // 2:
                gold += enemy[3]
                enemies.remove(enemy)
                break

    for enemy in enemies:
        enemy[0], enemy[1], enemy_size, enemy_dmg = enemy
        if barrack_x - barrack_size // 2 < enemy[0]< barrack_x + barrack_size // 2 and barrack_y - barrack_size // 2 < enemy[1] < barrack_y + barrack_size // 2:
            gold += enemy_dmg
            enemies.remove(enemy)
            break

    for guard in guards:
        guard_x, guard_y, guard_size = guard
        for enemy in enemies:
            enemy_x, enemy_y, enemy_size, enemy_damage = enemy
            if guard[0]- guard_size // 2 < enemy[0]< guard[0]+ guard_size // 2 and guard_y - guard_size // 2 < enemy[1] < guard_y + guard_size // 2:
                enemies.remove(enemy)
                break
        if enemies:
            nearest_enemy = min(enemies, key=lambda enemy: ((guard[0]- enemy[0]) ** 2 + (guard_y - enemy[1]) ** 2) ** 0.5)
            angle = math.atan2(nearest_enemy[1] - guard_y, nearest_enemy[0] - guard_x)
            speed = 3   
            guard[0]+= speed * math.cos(angle)
            guard_y += speed * math.sin(angle)
            guard[0] = guard_x
            guard[1] = guard_y

            dx = enemy[0]- guard_x
            dy = enemy[1] - guard_y
            distance = (dx ** 2 + dy ** 2) ** 0.5
            if distance < guard_size + enemy_size:

                enemies = [enemy for enemy in enemies if 0 <= enemy[0] <= WIDTH and 0 <= enemy[1] <= HEIGHT]

    check_enemy_collisions()

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
