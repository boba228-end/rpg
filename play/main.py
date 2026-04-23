import pygame
import random
import sys
import math
import os
import asyncio


def get_path(filename):
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    path_here = os.path.join(base_path, filename)
    if os.path.exists(path_here):
        return path_here
    
    path_up = os.path.join(os.path.dirname(base_path), filename)
    if os.path.exists(path_up):
        return path_up
    return path_here

async def main():
    pygame.init()

    WIDTH, HEIGHT = 321, 453
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Fruit Merge Pro")
    clock = pygame.time.Clock()

    def load_img(path, w, h):
        try:
            full_path = get_path(path)
            img = pygame.image.load(full_path).convert_alpha()
            return pygame.transform.scale(img, (w, h))
        except:
            surf = pygame.Surface((w, h))
            surf.fill((random.randint(150, 255), 50, 50))
            return surf

    FRUIT_DATA = {
        0: (35, 50), 1: (57, 65), 2: (55, 82),
        3: (48, 80), 4: (60, 69), 5: (80, 80)  
    }

    map_img = load_img("map.png", WIDTH, HEIGHT)

    imgs = [
        load_img("strawdery.png", 35, 50),
        load_img("apple.png", 57, 65),
        load_img("grape.png", 55, 82),
        load_img("pai.png", 48, 80),
        load_img("cherry.png", 60, 69),
        load_img("watermelon.png", 80, 80)
    ]

    dropped_fruits = []

    def draw_dashed_line(surf, color, start_pos, end_pos):
        dist = math.hypot(end_pos[0] - start_pos[0], end_pos[1] - start_pos[1])
        if dist < 1: return
        dx, dy = (end_pos[0] - start_pos[0]) / dist, (end_pos[1] - start_pos[1]) / dist
        for i in range(0, int(dist), 15):
            s = (start_pos[0] + dx * i, start_pos[1] + dy * i)
            e = (start_pos[0] + dx * min(i + 10, dist), start_pos[1] + dy * min(i + 10, dist))
            pygame.draw.line(surf, color, s, e, 2)

    current_type = random.randint(0, 1)
    s_x, s_y = 0, 50
    is_falling = False
    v_y = 0
    gravity = 0.6

    def spawn_new():
        nonlocal current_type, is_falling, v_y, s_y
        current_type = random.randint(0, 1)
        is_falling = False
        v_y = 0
        s_y = 50

    while True:
        screen.blit(map_img, (0, 0))
        mouse_x = pygame.mouse.get_pos()[0]
        curr_w, curr_h = FRUIT_DATA[current_type]

        if not is_falling:
            s_x = max(0, min(mouse_x - curr_w / 2, WIDTH - curr_w))
            draw_dashed_line(screen, (100, 100, 100), (s_x + curr_w/2, s_y + curr_h), (s_x + curr_w/2, HEIGHT))
            screen.blit(imgs[current_type], (s_x, s_y))
        else:
            v_y += gravity
            s_y += v_y
            curr_rect = pygame.Rect(s_x, s_y, curr_w, curr_h)
            landed = False
            for f in dropped_fruits:
                if curr_rect.colliderect(pygame.Rect(f['x'], f['y'], f['w'], f['h'])):
                    if s_y + curr_h <= f['y'] + 15:
                        landed = True
                        break
            if landed or s_y >= HEIGHT - curr_h:
                if s_y >= HEIGHT - curr_h: s_y = HEIGHT - curr_h
                dropped_fruits.append({'type': current_type, 'x': s_x, 'y': s_y, 'w': curr_w, 'h': curr_h, 'vel_y': v_y})
                spawn_new()
            else:
                screen.blit(imgs[current_type], (s_x, s_y))

        for _ in range(2): 
            for i, f1 in enumerate(dropped_fruits):
                if f1['y'] < HEIGHT - f1['h']:
                    f1['vel_y'] += gravity * 0.5
                    f1['y'] += f1['vel_y']
                else:
                    f1['y'] = HEIGHT - f1['h']
                    f1['vel_y'] = 0
                for j, f2 in enumerate(dropped_fruits):
                    if i == j: continue
                    r1, r2 = pygame.Rect(f1['x'], f1['y'], f1['w'], f1['h']), pygame.Rect(f2['x'], f2['y'], f2['w'], f2['h'])
                    if r1.colliderect(r2):
                        m1x, m1y = f1['x'] + f1['w']/2, f1['y'] + f1['h']/2
                        m2x, m2y = f2['x'] + f2['w']/2, f2['y'] + f2['h']/2
                        dx, dy = m1x - m2x, m1y - m2y
                        dist_x, dist_y = abs(dx), abs(dy)
                        min_dist_x, min_dist_y = (f1['w'] + f2['w']) / 2, (f1['h'] + f2['h']) / 2
                        overlap_x, overlap_y = min_dist_x - dist_x, min_dist_y - dist_y
                        if overlap_x < overlap_y:
                            if overlap_x > 0.5:
                                shift = overlap_x * 0.15 
                                if dx > 0: f1['x'] += shift; f2['x'] -= shift
                                else: f1['x'] -= shift; f2['x'] += shift
                        else:
                            if overlap_y > 0.5:
                                shift = overlap_y * 0.15
                                if dy > 0: f1['y'] += shift; f2['y'] -= shift
                                else: f1['y'] -= shift; f2['y'] += shift; f1['vel_y'] *= 0.2
                f1['x'] = max(0, min(f1['x'], WIDTH - f1['w']))

        to_remove = set()
        new_fruits = []
        for i in range(len(dropped_fruits)):
            if i in to_remove: continue
            for j in range(i + 1, len(dropped_fruits)):
                if j in to_remove: continue
                f1, f2 = dropped_fruits[i], dropped_fruits[j]
                if f1['type'] == f2['type'] and f1['type'] < 5:
                    r1, r2 = pygame.Rect(f1['x'], f1['y'], f1['w'], f1['h']), pygame.Rect(f2['x'], f2['y'], f2['w'], f2['h'])
                    if r1.inflate(4, 4).colliderect(r2):
                        to_remove.add(i); to_remove.add(j)
                        new_t = f1['type'] + 1
                        nw, nh = FRUIT_DATA[new_t]
                        new_fruits.append({'type': new_t, 'x': (f1['x'] + f2['x'])/2, 'y': min(f1['y'], f2['y']), 'w': nw, 'h': nh, 'vel_y': 0})
        
        if to_remove:
            dropped_fruits = [f for idx, f in enumerate(dropped_fruits) if idx not in to_remove]
            dropped_fruits.extend(new_fruits)

        for f in dropped_fruits:
            screen.blit(imgs[f['type']], (f['x'], f['y']))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not is_falling:
                is_falling = True

        pygame.display.update()
        
        await asyncio.sleep(0) 
        clock.tick(60)

asyncio.run(main())