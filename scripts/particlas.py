import pygame
pygame.init()
from scripts import anime

class Partikl:
    def __init__(self,x,y,tip):
        self.x = x
        self.y = y 
        self.таймер = 100
        self.animecia = anime.Lazy_Anime(f"graphics/particles/leaf{tip}",5)   
    def render(self,экран,камера):
        self.animecia.render(экран,камера,self.x,self.y)
    def uptate(self,партиклы):
        self.animecia.uptate()
        self.таймер -= 1
        if self.таймер == 0:
            партиклы.remove(self)
            
        
        