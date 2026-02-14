import pygame
import csv
import os
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







def load_border_from_CSV(путь):
    файл = open(путь)
    ритор = csv.reader(файл)  
    rezald = []
    ctroka = 0
    for row in ритор:
        ctolb = 0
        for i in row:
            if i == "24461":
                rezald.append((ctolb*8,ctroka*8))
            ctolb += 1
        ctroka += 1
    return set (rezald)
    #return set ()