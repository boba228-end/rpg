import pygame
from scripts import ia
otvet = None
in_suxariki = False
max_sim = 71

def render(экран):

    for i in range(0,len(otvet),max_sim):
        sub_otvet = otvet[i:i+max_sim]
        tetx_image = font_2.render(sub_otvet,True,(50,50,50))
        экран.blit(tetx_image,(50,y))
        y += 55