import pygame
import random
import sys

# Настройки экрана
WIDTH, HEIGHT = 900, 700
CELL_SIZE = 20
FPS = 60

# Цвета
COLOR_BG = (20, 25, 30)
COLOR_WALL = (60, 60, 80)
COLOR_GUS = (100, 255, 100)
COLOR_HEAD = (255, 255, 255)
COLOR_APPLE = (255, 50, 50)
COLOR_HAY = (255, 215, 0)
COLOR_TEXT = (200, 200, 200)

class CaterpillarGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Cyber Caterpillar: Room Climber")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24)
        self.reset_game()

    def reset_game(self):
        # Начальное состояние
        self.head = [WIDTH // 2, HEIGHT // 2]
        self.body = [list(self.head)]
        self.direction = pygame.Vector2(0, 0)
        self.max_length = 3
        self.apples_eaten = 0
        self.speed = 5
        self.score = 0
        
        # Спаунпоинт (Сено)
        self.spawn_pos = [100, 100]
        self.saved_length = 3
        
        self.spawn_apple()
        self.move_delay = 0

    def spawn_apple(self):
        # Спавним яблоко так, чтобы оно не попало в стену или игрока
        while True:
            self.apple_pos = [
                random.randrange(2, (WIDTH // CELL_SIZE) - 2) * CELL_SIZE,
                random.randrange(2, (HEIGHT // CELL_SIZE) - 2) * CELL_SIZE
            ]
            if self.apple_pos not in self.body:
                break

    def draw(self):
        self.screen.fill(COLOR_BG)
        
        # Рисуем границы (стены)
        pygame.draw.rect(self.screen, COLOR_WALL, (0, 0, WIDTH, HEIGHT), 20)
        
        # Рисуем сено (спаунпоинт)
        pygame.draw.rect(self.screen, COLOR_HAY, (*self.spawn_pos, CELL_SIZE, CELL_SIZE))
        
        # Рисуем яблоко
        pygame.draw.circle(self.screen, COLOR_APPLE, 
                           (self.apple_pos[0] + CELL_SIZE//2, self.apple_pos[1] + CELL_SIZE//2), 8)
        
        # Рисуем гусеницу
        for i, part in enumerate(self.body):
            color = COLOR_HEAD if i == 0 else COLOR_GUS
            pygame.draw.rect(self.screen, color, (part[0], part[1], CELL_SIZE - 2, CELL_SIZE - 2))

        # Интерфейс
        score_surf = self.font.render(f"Яблоки: {self.apples_eaten} | Длина: {len(self.body)}", True, COLOR_TEXT)
        self.screen.blit(score_surf, (30, 30))
        
        pygame.display.flip()

    def update(self):
        # Управление скоростью в зависимости от длины
        self.move_delay += 1
        current_limit = max(2, 10 - (len(self.body) // 5)) # Чем длиннее, тем тяжелее (медленнее)
        
        if self.move_delay >= current_limit:
            if self.direction.length() > 0:
                # Новая позиция головы
                new_head = [
                    self.head[0] + self.direction.x * CELL_SIZE,
                    self.head[1] + self.direction.y * CELL_SIZE
                ]
                
                # Проверка столкновения со стенами (лазанье)
                # Если упираемся в край — просто останавливаемся или скользим вдоль
                if new_head[0] < 20 or new_head[0] >= WIDTH - 20 or \
                   new_head[1] < 20 or new_head[1] >= HEIGHT - 20:
                    # Логика лазанья: разрешаем движение только вдоль стены
                    pass 
                
                self.head = new_head
                self.body.insert(0, list(self.head))

                # Проверка еды
                if self.head == self.apple_pos:
                    self.apples_eaten += 1
                    self.max_length += 1
                    self.spawn_apple()
                
                # Проверка сена (Сохранение)
                if self.head == self.spawn_pos:
                    self.saved_length = self.max_length
                    print("Прогресс сохранен!")

                # Удаление хвоста
                if len(self.body) > self.max_length:
                    self.body.pop()

                # Проверка смерти (столкновение с собой или выход за границы)
                if self.head in self.body[1:] or \
                   self.head[0] < 0 or self.head[0] >= WIDTH or \
                   self.head[1] < 0 or self.head[1] >= HEIGHT:
                    self.die()

            self.move_delay = 0

    def die(self):
        # Возврат к спаунпоинту
        self.head = list(self.spawn_pos)
        self.max_length = self.saved_length
        self.body = [list(self.head)]
        self.direction = pygame.Vector2(0, 0)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and self.direction.y == 0:
                        self.direction = pygame.Vector2(0, -1)
                    elif event.key == pygame.K_DOWN and self.direction.y == 0:
                        self.direction = pygame.Vector2(0, 1)
                    elif event.key == pygame.K_LEFT and self.direction.x == 0:
                        self.direction = pygame.Vector2(-1, 0)
                    elif event.key == pygame.K_RIGHT and self.direction.x == 0:
                        self.direction = pygame.Vector2(1, 0)

            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = CaterpillarGame()
    game.run()