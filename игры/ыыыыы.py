import pygame
import random
import math

# --- Инициализация ---
pygame.init()
WIDTH, HEIGHT = 1000, 800
WORLD_W, WORLD_H = 2200, 2000 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cyber Market: Tactical Darkness")
clock = pygame.time.Clock()

# --- Стили ---
font_ui = pygame.font.SysFont("Agency FB", 30, bold=True)
font_tag = pygame.font.SysFont("Consolas", 14, bold=True)
font_menu = pygame.font.SysFont("Impact", 80)

COLOR_BG = (2, 2, 5) 
COLOR_PLAYER = (0, 255, 255)
COLOR_MONEY = (0, 255, 120)
COLOR_GUARD = (255, 50, 50) 
WHITE = (255, 255, 255)

DEPARTMENTS = {
    "МОЛОЧНЫЙ": {"color": (150, 180, 255), "items": {"Йогурт": (230, 230, 255), "Кефир": (255, 255, 255), "Масло": (255, 255, 180)}},
    "ВЫПЕЧКА": {"color": (180, 120, 50), "items": {"Хлеб": (180, 130, 70), "Пончик": (255, 100, 200), "Кекс": (150, 75, 0)}},
    "НАПИТКИ": {"color": (0, 120, 255), "items": {"Вода": (0, 150, 255), "Сок": (255, 150, 0), "Кола": (100, 0, 0)}},
    "СНЕКИ": {"color": (200, 50, 50), "items": {"Чипсы": (255, 50, 50), "Сухарики": (130, 100, 50), "Чай": (40, 100, 40)}}
}

# --- Класс Охранника ---
class Guard:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.angle = random.randint(0, 360)
        self.speed = 2.5
        self.t_change = 0
        self.view_dist = 400
        self.view_spread = 60

    def update(self):
        self.t_change -= 1
        if self.t_change <= 0:
            self.angle += random.randint(-45, 45)
            self.t_change = random.randint(60, 180)
        
        move = pygame.Vector2(1, 0).rotate(self.angle) * self.speed
        new_pos = self.pos + move
        if 100 < new_pos.x < WORLD_W - 100 and 100 < new_pos.y < WORLD_H - 100:
            self.pos = new_pos
        else:
            self.angle += 180

    def check_detection(self, p_pos):
        dist = self.pos.distance_to(p_pos)
        if dist < self.view_dist:
            vec_to_player = p_pos - self.pos
            angle_to_p = math.degrees(math.atan2(vec_to_player.y, vec_to_player.x))
            diff = (angle_to_p - self.angle + 180) % 360 - 180
            if abs(diff) < self.view_spread / 2:
                return True
        return False

# --- Системы ---
MAP_SCALE = 8
GRID_SIZE = 60
grid_cols, grid_rows = WORLD_W // GRID_SIZE + 1, WORLD_H // GRID_SIZE + 1
explored_grid = [[0 for _ in range(grid_cols)] for _ in range(grid_rows)]

# --- Состояние ---
player_pos = pygame.Vector2(300, 300)
player_rect = pygame.Rect(0, 0, 32, 32)
current_angle = 0.0
target_angle = 0.0
rotation_speed = 0.12 

money, level = 0, 1
show_phone = False
phone_y = HEIGHT
phone_tab = "LIST" 
notes_text = "Купить продукты\nИзбегать охранников..."
is_paused = False
msg, msg_t = "", 0

todo_list, inventory, shelves, products = [], [], [], []
guards = []
checkout_rect = pygame.Rect(WORLD_W - 450, WORLD_H - 450, 300, 220)

def draw_tactical_light(surface, origin, angle, radius, spread, color):
    points = [origin]
    steps = 30
    start_angle = angle - spread / 2
    for i in range(steps + 1):
        rad = math.radians(start_angle + (spread / steps) * i)
        p = (origin[0] + math.cos(rad) * radius, origin[1] + math.sin(rad) * radius)
        points.append(p)
    pygame.draw.polygon(surface, color, points)

def draw_menu_btn(text, y):
    mx, my = pygame.mouse.get_pos()
    rect = pygame.Rect(WIDTH//2 - 140, y, 280, 60)
    hover = rect.collidepoint(mx, my)
    color = (0, 180, 180) if hover else (0, 60, 60)
    pygame.draw.rect(screen, color, rect, border_radius=12)
    pygame.draw.rect(screen, (0, 255, 255), rect, 2, border_radius=12)
    txt = font_ui.render(text, True, WHITE)
    screen.blit(txt, (rect.centerx - txt.get_width()//2, rect.centery - txt.get_height()//2))
    return rect

def init_level():
    global money, inventory, player_pos, explored_grid, todo_list, shelves, products, guards
    inventory, player_pos = [], pygame.Vector2(300, 300)
    explored_grid = [[0 for _ in range(grid_cols)] for _ in range(grid_rows)]
    shelves.clear(); products.clear(); guards.clear()
    
    for _ in range(level):
        guards.append(Guard(random.randint(800, WORLD_W-200), random.randint(800, WORLD_H-200)))

    dept_names = list(DEPARTMENTS.keys())
    for r in range(5):
        current_dept = dept_names[r % len(dept_names)]
        for c in range(5):
            sx, sy = 550 + c * 420, 450 + r * 380
            is_hor = (r + c) % 2 == 0
            rect = pygame.Rect(sx, sy, 300, 50) if is_hor else pygame.Rect(sx, sy, 50, 300)
            shelves.append({"rect": rect, "dept": current_dept, "color": DEPARTMENTS[current_dept]["color"]})
            items_in_dept = DEPARTMENTS[current_dept]["items"]
            for i in range(4):
                name = random.choice(list(items_in_dept.keys()))
                p_x = rect.x + i*70 + 20 if is_hor else rect.x + 55
                p_y = rect.y - 45 if is_hor else rect.y + i*70 + 20
                products.append({"name": name, "price": random.randint(20, 70), "color": items_in_dept[name], "rect": pygame.Rect(p_x, p_y, 35, 42), "done": False})
    
    level_items = random.sample(products, 5)
    money = sum(p["price"] for p in level_items) + 20
    todo_list = [p["name"] for p in level_items]

init_level()
running = True
while running:
    dt = 0.3 if show_phone else 1.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if is_paused:
                if draw_menu_btn("CONTINUE", 350).collidepoint(event.pos): is_paused = False
                if draw_menu_btn("RESTART", 430).collidepoint(event.pos): level = 1; init_level(); is_paused = False
            elif show_phone:
                p_r = pygame.Rect(WIDTH - 310, phone_y, 280, 520)
                if pygame.Rect(p_r.x+10, p_r.y+20, 85, 35).collidepoint(event.pos): phone_tab = "LIST"
                if pygame.Rect(p_r.x+95, p_r.y+20, 85, 35).collidepoint(event.pos): phone_tab = "MAP"
                if pygame.Rect(p_r.x+180, p_r.y+20, 85, 35).collidepoint(event.pos): phone_tab = "NOTES"

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: is_paused = not is_paused
            if not is_paused:
                if event.key == pygame.K_TAB: show_phone = not show_phone
                if event.key == pygame.K_e:
                    for p in products:
                        if player_rect.inflate(50, 50).colliderect(p["rect"]) and not p["done"] and money >= p["price"]:
                            money -= p["price"]; p["done"] = True; inventory.append(p["name"])
                            msg, msg_t = f"ВЗЯТО: {p['name']}", 70
                    if player_rect.colliderect(checkout_rect) and all(it in inventory for it in todo_list): 
                        level += 1; init_level(); msg, msg_t = f"LVL {level}!", 100

    if not is_paused:
        keys = pygame.key.get_pressed()
        vx, vy = (keys[pygame.K_d]-keys[pygame.K_a]), (keys[pygame.K_s]-keys[pygame.K_w])
        move = pygame.Vector2(vx, vy)
        if move.length() > 0:
            target_angle = math.degrees(math.atan2(vy, vx))
            new_pos = player_pos + move.normalize() * (8 * dt)
            if 0 <= new_pos.x <= WORLD_W-32 and 0 <= new_pos.y <= WORLD_H-32:
                if not any(pygame.Rect(new_pos.x, new_pos.y, 32, 32).colliderect(s["rect"]) for s in shelves):
                    player_pos = new_pos
        
        angle_diff = (target_angle - current_angle + 180) % 360 - 180
        current_angle += angle_diff * rotation_speed
        player_rect.topleft = player_pos
        
        for g in guards:
            g.update()
            if g.check_detection(player_pos + pygame.Vector2(16, 16)):
                msg, msg_t = "ОБНАРУЖЕН!", 100
                init_level()

        gx, gy = int(player_pos.x // GRID_SIZE), int(player_pos.y // GRID_SIZE)
        for y in range(max(0, gy-3), min(grid_rows, gy+4)):
            for x in range(max(0, gx-3), min(grid_cols, gx+4)): 
                if 0 <= y < grid_rows and 0 <= x < grid_cols: explored_grid[y][x] = 1

    cx, cy = max(0, min(player_pos.x - WIDTH//2, WORLD_W - WIDTH)), max(0, min(player_pos.y - HEIGHT//2, WORLD_H - HEIGHT))
    screen.fill(COLOR_BG)
    
    # --- Отрисовка Мира ---
    pygame.draw.rect(screen, (40, 10, 10), checkout_rect.move(-cx, -cy), border_radius=15)
    for s in shelves:
        r = s["rect"].move(-cx, -cy)
        pygame.draw.rect(screen, (20, 22, 30), r, border_radius=5)
    for p in products:
        if not p["done"]:
            dr = p["rect"].move(-cx, -cy)
            pygame.draw.rect(screen, p["color"], dr, border_radius=4)

    pygame.draw.rect(screen, COLOR_PLAYER, player_rect.move(-cx, -cy), border_radius=6)
    for g in guards:
        pygame.draw.rect(screen, COLOR_GUARD, pygame.Rect(g.pos.x - cx - 10, g.pos.y - cy - 10, 20, 20), border_radius=4)

    # --- СИСТЕМА СВЕТА ---
    fog = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    fog.fill((5, 5, 10, 245)) 
    light_mask = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    p_scr = (player_pos.x - cx + 16, player_pos.y - cy + 16)
    
    # Фонарь игрока (вырезается из тумана)
    draw_tactical_light(light_mask, p_scr, current_angle, 550, 75, (255, 255, 255, 180))
    pygame.draw.circle(light_mask, (255, 255, 255, 120), p_scr, 80)
    fog.blit(light_mask, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
    screen.blit(fog, (0, 0))
    
    # КРАСНЫЕ ФОНАРИ ОХРАННИКОВ (рисуются поверх тумана для яркости)
    for g in guards:
        g_scr = (int(g.pos.x - cx), int(g.pos.y - cy))
        # Создаем временную поверхность для прозрачного луча
        light_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        draw_tactical_light(light_surf, g_scr, g.angle, g.view_dist, g.view_spread, (255, 0, 0, 100))
        screen.blit(light_surf, (0, 0))

    # --- ТЕЛЕФОН ---
    target_py = 180 if show_phone else HEIGHT
    phone_y += (target_py - phone_y) * 0.15
    p_rect = pygame.Rect(WIDTH - 310, phone_y, 280, 520)
    pygame.draw.rect(screen, (15, 15, 25), p_rect, border_radius=35)
    pygame.draw.rect(screen, (0, 255, 255), p_rect, 1, border_radius=35)
    
    if show_phone:
        for i, (n, t) in enumerate([("СПИСОК", "LIST"), ("КАРТА", "MAP"), ("ЗАМЕТКИ", "NOTES")]):
            r = pygame.Rect(p_rect.x+10 + i*85, p_rect.y+20, 80, 35)
            pygame.draw.rect(screen, (0, 80, 80) if phone_tab == t else (30,30,40), r, border_radius=8)
            screen.blit(font_tag.render(n, True, WHITE), (r.x+10, r.y+10))
        cont_r = pygame.Rect(p_rect.x+15, p_rect.y+70, 250, 420)
        pygame.draw.rect(screen, (2, 2, 5), cont_r, border_radius=10)
        
        if phone_tab == "LIST":
            for i, item in enumerate(todo_list):
                clr = (60,60,60) if item in inventory else WHITE
                screen.blit(font_tag.render(f"• {item}", True, clr), (cont_r.x+20, cont_r.y+30+i*35))
        elif phone_tab == "MAP":
            m_s = pygame.Surface((250, 420)); m_s.fill((5, 5, 8))
            ox, oy = player_pos.x / MAP_SCALE - 125, player_pos.y / MAP_SCALE - 210
            for y in range(grid_rows):
                for x in range(grid_cols):
                    if explored_grid[y][x]:
                        pygame.draw.rect(m_s, (20, 25, 35), (x*GRID_SIZE/MAP_SCALE-ox, y*GRID_SIZE/MAP_SCALE-oy, (GRID_SIZE/MAP_SCALE)+1, (GRID_SIZE/MAP_SCALE)+1))
            for s in shelves:
                sx, sy = max(0, min(int(s["rect"].centerx // GRID_SIZE), grid_cols - 1)), max(0, min(int(s["rect"].centery // GRID_SIZE), grid_rows - 1))
                if explored_grid[sy][sx]:
                    pygame.draw.rect(m_s, s["color"], (s["rect"].x/MAP_SCALE-ox, s["rect"].y/MAP_SCALE-oy, s["rect"].width/MAP_SCALE, s["rect"].height/MAP_SCALE))
            for g in guards:
                pygame.draw.circle(m_s, COLOR_GUARD, (int(g.pos.x/MAP_SCALE-ox), int(g.pos.y/MAP_SCALE-oy)), 3)
            pygame.draw.circle(m_s, COLOR_PLAYER, (125, 210), 4)
            screen.blit(m_s, (cont_r.x, cont_r.y))
        elif phone_tab == "NOTES":
            screen.blit(font_tag.render(notes_text, True, WHITE), (cont_r.x+10, cont_r.y+40))

    pygame.draw.rect(screen, (5, 5, 10), (0, 0, WIDTH, 65))
    screen.blit(font_ui.render(f"CASH: ${money} | LVL: {level}", True, COLOR_MONEY), (25, 15))
    if msg_t > 0: msg_t -= 1; screen.blit(font_ui.render(msg, True, (0, 255, 255)), (WIDTH//2 - 100, 15))

    if is_paused:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA); overlay.fill((0, 0, 0, 220)); screen.blit(overlay, (0, 0))
        title = font_menu.render("PAUSED", True, (0, 255, 255))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 180))
        draw_menu_btn("CONTINUE", 350); draw_menu_btn("RESTART", 430)

    pygame.display.flip()
    clock.tick(60)
pygame.quit()