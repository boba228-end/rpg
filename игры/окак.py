import pygame
import math
import random

pygame.init()

# Настройки экрана
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tower Defense")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
TRANSPARENT_BLUE = (0, 0, 255, 50)

clock = pygame.time.Clock()
FPS = 60

# ------------------- ГЕНЕРАЦИЯ СЛОЖНОГО ПУТИ -------------------
def segments_intersect(a, b, c, d):
    def ccw(p1, p2, p3):
        return (p3[1] - p1[1]) * (p2[0] - p1[0]) > (p2[1] - p1[1]) * (p3[0] - p1[0])
    return ccw(a, c, d) != ccw(b, c, d) and ccw(a, b, c) != ccw(a, b, d)

def generate_random_path():
    GRID = 40
    cols = screen_width // GRID
    rows = screen_height // GRID

    start_row = random.randint(2, rows - 3)
    col, row = 1, start_row
    visited = set()
    visited.add((col, row))
    path_cells = [(col, row)]

    steps = random.randint(8, 14)
    for _ in range(steps):
        directions = []

        if col + 1 < cols - 2 and (col + 1, row) not in visited:
            directions.append((1, 0))
        if row - 1 > 1 and (col, row - 1) not in visited:
            directions.append((0, -1))
        if row + 1 < rows - 2 and (col, row + 1) not in visited:
            directions.append((0, 1))

        if not directions:
            break

        # тянем путь к центру
        center_row = rows // 2
        weighted_dirs = []
        for dx, dy in directions:
            if abs((row + dy) - center_row) < abs(row - center_row):
                weighted_dirs.extend([(dx, dy)] * 4)
            else:
                weighted_dirs.append((dx, dy))
        dx, dy = random.choice(weighted_dirs)

        col += dx
        row += dy
        visited.add((col, row))
        path_cells.append((col, row))

    # база справа
    base_col = cols - 2
    base_row = row
    path_cells.append((base_col, base_row))

    # перевод в пиксели
    path = [(c * GRID, r * GRID) for c, r in path_cells]
    return path

# ------------------- КЛАСС ВРАГА -------------------
class Enemy:
    def __init__(self, path, health=50, speed=1.2):
        self.path = path
        self.path_index = 0
        self.x, self.y = path[self.path_index]
        self.width = 40
        self.height = 40
        self.base_speed = speed
        self.speed = speed
        self.health = health
        self.alive = True

    def update(self):
        if self.path_index < len(self.path) - 1:
            target_x, target_y = self.path[self.path_index + 1]
            dx = target_x - self.x
            dy = target_y - self.y
            dist = math.sqrt(dx ** 2 + dy ** 2)
            if dist > self.speed:
                self.x += self.speed * (dx / dist)
                self.y += self.speed * (dy / dist)
            else:
                self.path_index += 1
        self.speed = self.base_speed
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.alive = False
            return True
        return False

    def draw(self, screen):
        if self.alive:
            pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))
        else:
            pygame.draw.circle(screen, (255, 165, 0), (int(self.x + self.width // 2), int(self.y + self.height // 2)), 20)

    def draw_health_bar(self, screen):
        pygame.draw.rect(screen, BLACK, (self.x - 15, self.y - 10, 30, 5))
        pygame.draw.rect(screen, RED, (self.x - 15, self.y - 10, 30 * max(self.health,0) / 50, 5))

# ------------------- КЛАСС СНАРЯДА -------------------
class Projectile:
    def __init__(self, x, y, target_x, target_y, damage):
        self.x = x
        self.y = y
        self.target_x = target_x
        self.target_y = target_y
        self.damage = damage
        self.speed = 5
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        dist = math.sqrt(dx ** 2 + dy ** 2)
        if dist > self.speed:
            self.x += self.speed * (dx / dist)
            self.y += self.speed * (dy / dist)

    def draw(self, screen):
        pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), 5)

# ------------------- КЛАСС БАШНИ -------------------
class Tower:
    def __init__(self, x, y, tower_type="default"):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.type = tower_type
        self.level = 1
        self.last_attack_time = 0
        self.projectiles = []

        if tower_type == "default":
            self.color = BLUE
            self.damage = 10
            self.attack_speed = 600
            self.range = 120

        elif tower_type == "sniper":
            self.color = RED
            self.damage = 25
            self.attack_speed = 1200
            self.range = 220

        elif tower_type == "slow":
            self.color = (150, 0, 150)
            self.damage = 5
            self.attack_speed = 700
            self.range = 140

    def update(self, enemies, current_time):
        global coins
        if current_time - self.last_attack_time > self.attack_speed:
            for enemy in enemies:
                if math.hypot(enemy.x - self.x, enemy.y - self.y) <= self.range:
                    projectile = Projectile(
                        self.x + self.width // 2,
                        self.y + self.height // 2,
                        enemy.x,
                        enemy.y,
                        self.damage
                    )
                    projectile.slow = (self.type == "slow")
                    self.projectiles.append(projectile)
                    self.last_attack_time = current_time
                    break

        for projectile in self.projectiles[:]:
            projectile.update()
            for enemy in enemies[:]:
                if math.hypot(projectile.x - enemy.x, projectile.y - enemy.y) < 12:
                    if projectile.slow:
                        enemy.speed *= 0.7
                    if enemy.take_damage(projectile.damage):
                        enemies.remove(enemy)
                        coins += 2
                    self.projectiles.remove(projectile)
                    break

    def draw(self, screen):
        pygame.draw.rect(screen, self.color,
                         (self.x, self.y, self.width, self.height))
        pygame.draw.circle(
            screen,
            self.color,
            (self.x + self.width // 2, self.y + self.height // 2),
            self.range,
            2
        )
        for projectile in self.projectiles:
            projectile.draw(screen)
# ------------------- КЛАСС БАЗЫ -------------------
class Base:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 60
        self.height = 60
        self.health = 5

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont(None, 24)
        text = font.render(f"HP: {self.health}", True, BLACK)
        screen.blit(text, (self.x + 5, self.y + 5))

# ------------------- ГЛАВНАЯ ФУНКЦИЯ -------------------
def main():
    global coins
    coins = 6
    running = True
    towers = []

    level = 1
    wave_enemies = 5
    enemies_spawned = 0
    enemy_health = 50
    enemy_speed = 1.2
    enemy_spawn_interval = 1000
    last_spawn_time = 0

    path = generate_random_path()
    base_x, base_y = path[-1]
    base = Base(base_x - 30, base_y - 30)
    enemies = []
    selected_tower_type = "default"
    while running:
        screen.fill(WHITE)
        current_time = pygame.time.get_ticks()

        # Рисуем путь
        for i in range(len(path) - 1):
            pygame.draw.line(screen, GRAY, path[i], path[i + 1], 40)

        # События
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selected_tower_type = "default"
                elif event.key == pygame.K_2:
                    selected_tower_type = "sniper"
                elif event.key == pygame.K_3:
                    selected_tower_type = "slow"
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if event.button == 1:  # левая кнопка — поставить башню
                    can_place = True
                    for i in range(len(path) - 1):
                        x1, y1 = path[i]
                        x2, y2 = path[i + 1]
                        dx = x2 - x1
                        dy = y2 - y1
                        t = max(0, min(1, ((x - x1) * dx + (y - y1) * dy) / (dx*dx + dy*dy))) if dx*dx+dy*dy !=0 else 0
                        nearest_x = x1 + t * dx
                        nearest_y = y1 + t * dy
                        if math.hypot(x - nearest_x, y - nearest_y) < 40:
                            can_place = False
                            break
                    if can_place:
                        if coins >= 3:
                            if event.button == 1:
                                towers.append(Tower(x - 25, y - 25, "default"))
                            elif event.button == 2:
                                towers.append(Tower(x - 25, y - 25, "sniper"))
                            elif event.button == 3:
                                towers.append(Tower(x - 25, y - 25, "slow"))
                            coins -= 3
                        else:
                            print("Недостаточно монет!")
                    else:
                        print("Нельзя ставить башню на пути врага!")
                elif event.button == 3:  # правая кнопка — улучшить башню
                    for tower in towers:
                        if tower.x <= x <= tower.x + tower.width and tower.y <= y <= tower.y + tower.height:
                            tower.upgrade()
                            break

        # Спавн врагов
        if enemies_spawned < wave_enemies:
            if current_time - last_spawn_time > enemy_spawn_interval:
                enemies.append(Enemy(path, enemy_health, enemy_speed))
                enemies_spawned += 1
                last_spawn_time = current_time
        elif not enemies:
            coins += 5 + level * 2
            towers.clear()
            level += 1
            wave_enemies = int(wave_enemies * 1.2)
            enemy_health = int(enemy_health * 1.15)
            enemy_speed = round(enemy_speed * 1.05, 2)
            enemies_spawned = 0
            path = generate_random_path()
            base_x, base_y = path[-1]
            base = Base(base_x - 30, base_y - 30)

        # Обновление врагов
        for enemy in enemies[:]:
            enemy.update()
            enemy.draw(screen)
            enemy.draw_health_bar(screen)
            if enemy.path_index >= len(enemy.path) - 1:
                base.take_damage(1)
                enemies.remove(enemy)

        # Обновление башен
        for tower in towers:
            tower.update(enemies, current_time)
        for tower in towers:
            tower.draw(screen)

        # База
        base.draw(screen)

        # Монеты и уровень
        font = pygame.font.SysFont(None, 32)
        text = font.render(f"Монеты: {coins} | Уровень: {level}", True, BLACK)
        screen.blit(text, (10, 10))

        # Конец игры
        if base.health <= 0:
            font = pygame.font.SysFont(None, 48)
            text = font.render("Игра окончена! База разрушена!", True, RED)
            screen.blit(text, (150, 250))
            pygame.display.flip()
            pygame.time.delay(3000)
            running = False

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()

