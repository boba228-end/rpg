import pygame 
from scripts import utils
import csv
pygame.init()

class Grass:
    def __init__(self,Id,x,y):
        self.x = x
        self.y = y
        if Id == "1":
           self.image = utils.load_image("graphics/grass/grass_1.png",1) 
        if Id == "2":
           self.image = utils.load_image("graphics/grass/grass_2.png",1) 
        if Id == "3":
           self.image = utils.load_image("graphics/grass/grass_3.png",1)
        self.bxgrass = pygame.Rect(self.x,self.y,self.image.get_width(),self.image.get_height())

    def render(self,экран,камера):
       экран.blit(self.image,(self.x-камера[0],self.y-камера[1]))

    def uptate(self):
       pass

def kerate_grass():
    grass = []
    f = open("map\grass.csv")
    riter = csv.reader(f)
    for cтрока,x in enumerate(riter):
           for столбец,y in enumerate(x):
               if y != "-1":
                   твава = Grass(y,32*столбец,32*cтрока)
                   grass.append(твава)

    f.close()
    return(grass)