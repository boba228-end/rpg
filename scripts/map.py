import pygame
from scripts import utils
pygame.init()

class КАРТА:
    def __init__(self):
        self.карта = utils.load_image("taild/stiriworold.png",1)
        self.камера = [0,0]
        self.границы = utils.load_border()
    def render(self,экран):
        экран.blit(self.карта,(-self.камера[0],-self.камера[1]))

    def get_iner_sechons(self,bxpl):
        список = []
        for i in self.границы:
            bx = pygame.Rect(i[0],i[1],8,8)
            if bx.colliderect(bxpl):
                список.append(bx)
        return(список)