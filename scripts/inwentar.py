import pygame
pygame.init()

склад = { } 
def add_inwentar(название,колво):
    if название in склад :
        склад[название] += колво
    else:
        склад[название] = колво


def render(экран):
    pygame.draw.rect(экран, (100,100,100),(200,150,400,300))


def utate():
    pass



