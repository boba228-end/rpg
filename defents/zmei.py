import pygame
from scripts import utils
pygame.init()

WIDTH, HEIGHT = 499, 497
screen = pygame.display.set_mode((WIDTH, HEIGHT))
map = utils.load_image("defents/map.png")
while True:
