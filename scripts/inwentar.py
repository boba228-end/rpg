import pygame
pygame.init()

склад = { } 
from scripts import utils
pygame.init()

склад = { } 
def load():
    global fon,grass,font
    fon = utils.load_image("graphics/fireboll/Image20260214132900.png",1.32)
    grass = utils.load_image("graphics/grass/grass_2.png",1)
    font = pygame.font.Font(None,40)
def add_inwentar(название,колво):
    if название in склад :
        склад[название] += колво
    else:
        склад[название] = колво


def render(экран):
    экран.blit(fon,(100,100))
    экран.blit(grass,(180,150))
    экран.blit(font.render(str(склад.get("трава",0)),True,(255,255,255)),(165,135))
def utate():
    pass



