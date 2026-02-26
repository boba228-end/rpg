import pygame
pygame.init()

название_квест = 'тест'
font = pygame.font.Font(None,23)
def render(экран):
    pygame.draw.rect(экран,"gray",(900,0,200,150))
class Spirit_Kvest:
    def __init__(self,kol_vo):
        self.kol = kol_vo
        self.kol_spirit_killed = 0
    def render(self,экран):
        font.render(str(self.kol_spirit_killed)+"/"+str(self.kol))