import pygame
from scripts import utils
pygame.init()

class Anime:
    def __init__(self,картинки,пириуд):
        self.картинки = картинки
        self.пириуд = пириуд
        self.индикс = 0
        self.таймер = пириуд
    def render(self,экран,камера,x,y):
         экран.blit(self.картинки[self.индикс],(x-камера[0],y-камера[1]))
    def uptate(self):
        self.таймер -= 1
        if self.таймер == 0:
            self.индикс += 1
            self.таймер = self.пириуд
            if self.индикс >= len(self.картинки):
                self.индикс = 0

class Lazy_Anime(Anime):
     def __init__(self, путь_картинки, пириуд,scale=1):
         картинки = utils.load_images(путь_картинки,scale)
         Anime.__init__(self,картинки, пириуд)