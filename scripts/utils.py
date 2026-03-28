import pygame
import csv
import os
import pytmx
pygame.init()

def load_image(путь, моштаб):
    картинка = pygame.image.load(путь).convert_alpha()
    w = картинка.get_width()
    h = картинка.get_height()
    w2 = int(w * моштаб)
    h2 = int(h * моштаб)
    new_картинка = pygame.transform.scale(картинка, (w2, h2))
    return(new_картинка)
def load_images(путь,много):
    картинки = []
    ам = os.listdir(путь)
    for i in ам:
        абоба = load_image(путь +"/"+ i,много)
        картинки.append(абоба)
    return(картинки)


def cut_image(путь, можтаб, size):
    tiles = []
    картинка = load_image(путь, можтаб)
    for x in range(0, картинка.get_width(), size):
        for y in range(0, картинка.get_height(), size):
            tile = картинка.subsurface((x, y, size, size))
            tiles.append(tile)
    return(tiles)


def load_border():
    border = []
    world = pytmx.load_pygame("taild/stiriworold.tmx")
    for x,y,gid in world.get_layer_by_name("границы"):
        if gid != 0:
            border.append((x*32,y*32))
    return set (border)