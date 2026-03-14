import pygame
import random

# Инициализация
pygame.init()
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Симулятор Босса: Дракон против Нуба")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)
small_font = pygame.font.SysFont("Arial", 18)

# Цвета
GOLD = (255, 215, 0)
DRAGON_RED = (200, 30, 30)
FIRE_ORANGE = (255, 100, 0)
KNIGHT_SILVER = (192, 192, 192)
CAVE_BG = (30, 20, 10)

class Dragon:
    def __init__(self):
        self.rect = pygame.Rect(100, 400, 150, 100)
        self.hp = 1000
        self.max_hp = 1000
        self.vel_y = 0
        self.is_breathing_fire = False
        self.fire_rect = pygame.Rect(0, 0, 200, 80)

    def update(self):
        keys = pygame.key.get_pressed()
        # Движение
        if keys[pygame.K_LEFT] and self.rect.left > 0: self.rect.x -= 5
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH: self.rect.x += 5
        
        # Прыжок (полет)
        if keys[pygame.K_SPACE]:
            self.vel_y = -8
        
        # Гравитация
        self.vel_y += 0.5
        self.rect.y += self.vel_y
        if self.rect.bottom > HEIGHT - 50:
            self.rect.bottom = HEIGHT - 50
            self.vel_y = 0

        # Огненное дыхание (Атака)
        if keys[pygame.K_x]:
            self.is_breathing_fire = True
            self.fire_rect.midleft = self.rect.midright
        else:
            self.is_breathing_fire = False

    def draw(self):
        # Рисуем тело дракона
        pygame.draw.ellipse(screen, DRAGON_RED, self.rect)
        pygame.draw.polygon(screen, (150, 0, 0), [self.rect.midtop, (self.rect.centerx-20, self.rect.top-40), (self.rect.centerx+20, self.rect.top-40)]) # Крыло
        
        if self.is_breathing_fire:
            pygame.draw.ellipse(screen, FIRE_ORANGE, self.fire_rect)

class Knight:
    def __init__(self):
        self.rect = pygame.Rect(800, 500, 40, 60)
        self.hp = 100
        self.max_hp = 100
        self.speed = 2
        self.state = "thinking"
        self.timer = 0
        self.phrase = ""
        self.phrases = [
            "Где тут кнопка атаки?",
            "Ого, какой большой пельмень!",
            "Мама говорила, будет легко...",
            "А щит точно защищает от огня?",
            "Я просто нажму все кнопки сразу!",
            "Ай! Оно жжется!"
        ]

    def ai_logic(self, dragon):
        self.timer -= 1
        if self.timer <= 0:
            self.state = random.choice(["approach", "retreat", "jump", "idle"])
            self.timer = random.randint(40, 100)
            if random.random() < 0.3:
                self.phrase = random.choice(self.phrases)

        if self.state == "approach":
            if self.rect.x < dragon.rect.x: self.rect.x += self.speed
            else: self.rect.x -= self.speed
        elif self.state == "retreat":
            if self.rect.x < dragon.rect.x: self.rect.x -= self.speed
            else: self.rect.x += self.speed

        # Рыцарь получает урон от огня
        if dragon.is_breathing_fire and self.rect.colliderect(dragon.fire_rect):
            self.hp -= 0.5
            self.phrase = "ААА! ГОРЮ!"

        # Рыцарь "бьет" дракона (если коснулся)
        if self.rect.colliderect(dragon.rect):
            dragon.hp -= 1

    def draw(self):
        pygame.draw.rect(screen, KNIGHT_SILVER, self.rect)
        if self.phrase and self.timer > 0:
            txt = small_font.render(self.phrase, True, (255, 255, 255))
            screen.blit(txt, (self.rect.x - 20, self.rect.y - 30))

def draw_interface(dragon, knight):
    # HP Дракона
    pygame.draw.rect(screen, (50, 0, 0), (20, 20, 300, 25))
    pygame.draw.rect(screen, (255, 0, 0), (20, 20, 300 * (dragon.hp/dragon.max_hp), 25))
    screen.blit(font.render("ДРАКОН (ТЫ)", True, (255, 255, 255)), (20, 50))

    # HP Рыцаря
    pygame.draw.rect(screen, (50, 50, 50), (WIDTH - 320, 20, 300, 25))
    pygame.draw.rect(screen, (200, 200, 200), (WIDTH - 320, 20, 300 * (knight.hp/knight.max_hp), 25))
    screen.blit(font.render("НУБ-РЫЦАРЬ", True, (255, 255, 255)), (WIDTH - 180, 50))

# Игра
dragon = Dragon()
knight = Knight()

running = True
while running:
    screen.fill(CAVE_BG)
    
    # Рисуем "золото" на полу
    for i in range(0, WIDTH, 40):
        pygame.draw.circle(screen, GOLD, (i + random.randint(0,10), HEIGHT - 45), 15)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обновление
    dragon.update()
    knight.ai_logic(dragon)

    # Отрисовка
    dragon.draw()
    knight.draw()
    draw_interface(dragon, knight)

    # Условия победы/поражения
    if knight.hp <= 0:
        msg = font.render("РЫЦАРЬ УШЕЛ НА РЕСПАУН! ТЫ ПОБЕДИЛ!", True, GOLD)
        screen.blit(msg, (WIDTH//2 - 200, HEIGHT//2))
        pygame.display.flip()
        pygame.time.delay(3000)
        running = False
    
    if dragon.hp <= 0:
        msg = font.render("НУБ СЛУЧАЙНО ТЕБЯ ЗАВАЛИЛ... ПОЗОР!", True, (255, 0, 0))
        screen.blit(msg, (WIDTH//2 - 200, HEIGHT//2))
        pygame.display.flip()
        pygame.time.delay(3000)
        running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()