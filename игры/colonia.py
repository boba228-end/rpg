import pygame
import sys
import math
import random

pygame.init()

# ---------------- НАСТРОЙКИ ----------------
TILE = 40
MAP_W, MAP_H = 20, 15
WIDTH, HEIGHT = MAP_W * TILE, MAP_H * TILE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Colonization Prototype")

clock = pygame.time.Clock()

# ---------------- ЦВЕТА ----------------
GREEN = (80, 160, 80)
BROWN = (120, 80, 40)
RED = (200, 60, 60)
GRAY = (120, 120, 120)
BLUE = (80, 80, 200)
BLACK = (0, 0, 0)
DARK_GREEN = (34, 139, 34)

# ---------------- РЕСУРСЫ ----------------
wood = 20  # стартовый ресурс

# ---------------- ОБЪЕКТЫ ----------------
class Building:
    def __init__(self, x, y, is_hq=False):
        self.x = x
        self.y = y
        self.is_hq = is_hq
        self.hp = 200 if is_hq else 100
        self.rect = pygame.Rect(x, y, TILE, TILE)

    def draw(self):
        color = BLUE if self.is_hq else BROWN
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)

class Tree:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, TILE//2, TILE//2)
        self.alive = True
        self.respawn_time = 8000  # дерево восстанавливается через 8 секунд
        self.timer = 0

    def update(self, dt):
        if not self.alive:
            self.timer += dt
            if self.timer >= self.respawn_time:
                self.alive = True
                self.timer = 0

    def draw(self):
        if self.alive:
            pygame.draw.rect(screen, DARK_GREEN, self.rect)

class Enemy:
    def __init__(self, x, y, target):
        self.x = x
        self.y = y
        self.speed = 1
        self.target = target
        self.hp = 30
        self.max_hp = 30
        self.rect = pygame.Rect(x, y, 30, 30)

    def update(self):
        dx = self.target.rect.centerx - self.x
        dy = self.target.rect.centery - self.y
        dist = math.hypot(dx, dy)
        if dist != 0:
            self.x += dx / dist * self.speed
            self.y += dy / dist * self.speed
        self.rect.topleft = (self.x, self.y)

        if self.rect.colliderect(self.target.rect):
            self.target.hp -= 0.2

    def draw(self):
        pygame.draw.rect(screen, RED, self.rect)
        # полоска HP
        bar_width = self.rect.width
        bar_height = 5
        health_ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, RED, (self.x, self.y - bar_height - 2, bar_width, bar_height))
        pygame.draw.rect(screen, GREEN, (self.x, self.y - bar_height - 2, bar_width * health_ratio, bar_height))

class Worker:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 2
        self.rect = pygame.Rect(x, y, TILE//2, TILE//2)
        self.target_tree = None

    def update(self, trees):
        global wood
        live_trees = [t for t in trees if t.alive]
        if not self.target_tree or not self.target_tree.alive:
            if live_trees:
                self.target_tree = min(live_trees, key=lambda t: math.hypot(t.x - self.x, t.y - self.y))
            else:
                self.target_tree = None

        if self.target_tree:
            dx = self.target_tree.x - self.x
            dy = self.target_tree.y - self.y
            dist = math.hypot(dx, dy)
            if dist != 0:
                self.x += dx / dist * self.speed
                self.y += dy / dist * self.speed
            self.rect.topleft = (self.x, self.y)

            if self.rect.colliderect(self.target_tree.rect) and self.target_tree.alive:
                wood += 1
                self.target_tree.alive = False
                self.target_tree.timer = 0
                self.target_tree = None

    def draw(self):
        pygame.draw.rect(screen, GRAY, self.rect)

class Tower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, TILE, TILE)
        self.range = 120
        self.damage = 10
        self.fire_rate = 1000
        self.timer = 0

    def update(self, enemies, dt):
        self.timer += dt
        if self.timer >= self.fire_rate:
            self.timer = 0
            target = None
            min_dist = float('inf')
            for e in enemies:
                dist = math.hypot(e.rect.centerx - self.rect.centerx,
                                  e.rect.centery - self.rect.centery)
                if dist < self.range and dist < min_dist:
                    target = e
                    min_dist = dist
            if target:
                target.hp -= self.damage

    def draw(self):
        pygame.draw.rect(screen, GRAY, self.rect)
        pygame.draw.circle(screen, BLACK, self.rect.center, self.range, 1)

# ---------------- ИГРА ----------------
buildings = []
trees = []
enemies = []
towers = []

hq = Building(WIDTH//2 - TILE//2, HEIGHT//2 - TILE//2, True)
buildings.append(hq)

builder_house = Building(WIDTH//2 - TILE//2, HEIGHT//2 + TILE, False)
buildings.append(builder_house)

worker = Worker(builder_house.x, builder_house.y)

# Деревья
for _ in range(15):
    x = random.randint(0, MAP_W-1) * TILE + TILE//4
    y = random.randint(0, MAP_H-1) * TILE + TILE//4
    trees.append(Tree(x, y))

# ---------------- ВОЛНЫ ----------------
wave_number = 1
wave_active = False   # первая волна ещё не активна
enemies_remaining = 0
spawn_interval = 2000
last_spawn = 0
initial_pause = 10000  # 10 секунд паузы перед первой волной

font = pygame.font.SysFont(None, 24)
game_timer = 0

# ---------------- ЦИКЛ ----------------
while True:
    dt = clock.tick(60)
    game_timer += dt

    screen.fill(GREEN)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # ЛКМ строим обычные здания
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = pygame.mouse.get_pos()
            x = (mx // TILE) * TILE
            y = (my // TILE) * TILE
            if wood >= 10:
                buildings.append(Building(x, y))
                wood -= 10
        # ПКМ строим башню
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            mx, my = pygame.mouse.get_pos()
            x = (mx // TILE) * TILE
            y = (my // TILE) * TILE
            if wood >= 15:
                towers.append(Tower(x, y))
                wood -= 15

    # Обновление деревьев
    for t in trees:
        t.update(dt)

    # Обновление рабочего
    worker.update(trees)

    # Запуск первой волны после initial_pause
    if not wave_active and game_timer > initial_pause and enemies_remaining == 0:
        wave_active = True
        wave_number = 1
        enemies_remaining = 5
        last_spawn = game_timer
        print(f"Началась первая волна {wave_number}!")

    # ВОЛНА врагов
    if wave_active and enemies_remaining > 0:
        if game_timer - last_spawn > spawn_interval:
            last_spawn = game_timer
            side = random.choice(["top", "bottom", "left", "right"])
            if side == "top":
                enemies.append(Enemy(random.randint(0, WIDTH), -40, hq))
            elif side == "bottom":
                enemies.append(Enemy(random.randint(0, WIDTH), HEIGHT + 40, hq))
            elif side == "left":
                enemies.append(Enemy(-40, random.randint(0, HEIGHT), hq))
            else:
                enemies.append(Enemy(WIDTH + 40, random.randint(0, HEIGHT), hq))
            enemies_remaining -= 1

    # Проверка конца волны
    if wave_active and enemies_remaining == 0 and len(enemies) == 0:
        wave_active = False
        print(f"Волна {wave_number} окончена!")

    # Перезапуск следующей волны после паузы между волнами
    if not wave_active and game_timer - last_spawn > 10000 and game_timer > initial_pause:
        wave_number += 1
        enemies_remaining = 5 + wave_number*2
        wave_active = True
        last_spawn = game_timer
        print(f"Началась волна {wave_number}!")

    # Обновление врагов
    for e in enemies[:]:
        e.update()
        if e.hp <= 0:
            enemies.remove(e)

    # Обновление башен
    for tower in towers:
        tower.update(enemies, dt)

    # Проверка Game Over
    if hq.hp <= 0:
        print("GAME OVER! Вы проиграли!")
        pygame.quit()
        sys.exit()

    # Рисуем объекты
    for t in trees:
        t.draw()
    for b in buildings:
        b.draw()
    for e in enemies:
        e.draw()
    for tower in towers:
        tower.draw()
    worker.draw()

    # UI
    screen.blit(font.render(f"Wood: {wood}", True, BLACK), (10, 10))
    screen.blit(font.render(f"HQ HP: {int(hq.hp)}", True, BLACK), (10, 30))
    if not wave_active:
        if game_timer < initial_pause:
            screen.blit(font.render("Начальная пауза для развития", True, BLACK), (10, 50))
        else:
            screen.blit(font.render("Пауза между волнами", True, BLACK), (10, 50))
    else:
        screen.blit(font.render(f"Волна {wave_number}", True, BLACK), (10, 50))

    pygame.display.flip()
