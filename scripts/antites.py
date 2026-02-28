import pygame 
import random
from scripts import anime
from scripts import utils
from scripts import particlas
from scripts import batl
from scripts import inwentar
import csv

pygame.init()
font = pygame.font.Font(None,40)

def debag(every,экран):
    текст = font.render(str(every),True,(255,255,0))
    экран.blit(текст,(10,10))

class Entity:
    def __init__(self,x,y,speed,width,height,map):
        self.x = x
        self.y =y 
        self.speed = speed
        self.width = width
        self.height = height
        self.runr = False
        self.runl = False
        self.runu = False
        self.rund = False
        self.map = map

    def update(self):
        sp = self.speed
        if (self.runu == True or self.rund == True) and (self.runr == True or self.runl == True):
             sp /= 1.41
        self.movex(sp)
        self.movey(sp)


    def movex(self,sp):
        if self.runr == True:
            self.x += sp
        if self.runl == True:
            self.x -=  sp
        tiles = self.map.get_iner_sechons(self.get_bx())
        for i in tiles:
            if self.runr == True:
                self.x = i.x-self.width
            if self.runl == True:
                self.x = i.x+i.width



    def movey(self,sp):
        if self.runu == True:
            self.y -= sp
        if self.rund == True:
            self.y += sp
        tiles = self.map.get_iner_sechons(self.get_bx())
        for i in tiles:
            if self.rund == True:
                self.y = i.y-self.height
            if self.runu == True:
                self.y = i.y+i.height

    def render(self,экран):
            pygame.draw.rect(экран,(65,54,86),(self.x,self.y,self.width,self.height))
    

    def get_bx(self):
        bx = pygame.Rect(self.x,self.y,self.width,self.height)
        return(bx)


class Playr(Entity):
     def __init__(self,x,y,speed,map):
        self.karent_anime = "down"
        self.exp = 0
        self.таймер = 0
        self.HP = 100
        self.MAXhp = 100
        self.ener = 100
        self.MAXener = 100
        self.armor = 1
        self.animes =  {
            "down":anime.Lazy_Anime("graphics/player/down",15),
            "up":anime.Lazy_Anime("graphics/player/up",15),
            "right":anime.Lazy_Anime("graphics/player/right",15),
            "left":anime.Lazy_Anime("graphics/player/left",15),
            "down_idle":anime.Lazy_Anime("graphics/player/down_idle",15),
            "up_idle":anime.Lazy_Anime("graphics/player/up_idle",15),
            "right_idle":anime.Lazy_Anime("graphics/player/right_idle",15),
            "left_idle":anime.Lazy_Anime("graphics/player/left_idle",15),
            "down_attack":anime.Lazy_Anime("graphics/player/down_attack",15),
            "up_attack":anime.Lazy_Anime("graphics/player/up_attack",15),
            "right_attack":anime.Lazy_Anime("graphics/player/right_attack",15),
            "left_attack":anime.Lazy_Anime("graphics/player/left_attack",15),
            "batl_anime":anime.Lazy_Anime("graphics/player/right_idle",15,3),
            "batl_attak":anime.Lazy_Anime("graphics/player/right_attack",15,3)
        }
        self.weapons = {
            "sword":utils.load_images("graphics/weapons/sword",1)
        }
        self.оружие_в_руке = "sword"
        self.width = self.animes[self.karent_anime].картинки[0].get_width()
        self.height = self.animes[self.karent_anime].картинки[0].get_height()
        self.attaking = False
        self.attaks = {
            ""
        }
        super().__init__(x,y,speed,self.width,self.height,map)



     def render(self,экран,камера):
        if self.attaking == True: 
            if self.karent_anime == "left_attack":
                self.animes[self.karent_anime].render(экран,камера,self.x,self.y)
                экран.blit(self.weapons[self.оружие_в_руке][2],(self.x-30-камера[0],self.y+self.height/2+5-камера[1]))


            if self.karent_anime == "up_attack":
                экран.blit(self.weapons[self.оружие_в_руке][4],(self.x+40-30-камера[0],self.y-70+self.height/2+5-камера[1]))
                self.animes[self.karent_anime].render(экран,камера,self.x,self.y)
                

            if self.karent_anime == "down_attack":
                экран.blit(self.weapons[self.оружие_в_руке][0],(self.x+40-37-камера[0],self.y-70+95+self.height/2+5-камера[1]))
                self.animes[self.karent_anime].render(экран,камера,self.x,self.y)


            if self.karent_anime == "right_attack":
                self.animes[self.karent_anime].render(экран,камера,self.x,self.y)
                экран.blit(self.weapons[self.оружие_в_руке][3],(self.x+83-30-камера[0],self.y-70+70+self.height/2+5-камера[1]))
        else:
            self.animes[self.karent_anime].render(экран,камера,self.x,self.y)

     def atakk_aria(self,):
         if "left" in self.karent_anime :
             return(pygame.Rect(self.x-50,self.y-7,62,self.height+14))
         if "right" in self.karent_anime :
             return(pygame.Rect(self.x+self.width-10,self.y-7,62,self.height+14))
         if "up" in self.karent_anime :
             return(pygame.Rect(self.x-7,self.y-52,self.height+14,62))
         if"down" in  self.karent_anime :
             return(pygame.Rect(self.x-7,self.y+self.height-10,self.height+14,62))
     def update(self):
         if self.attaking == True:
             self.таймер += 1
         if self.таймер == 30:
             self.attaking = False
             self.таймер = 0
             if self.karent_anime == "up_attack":
                self.karent_anime = "up_idle" 
             if self.karent_anime == "down_attack":
                self.karent_anime = "down_idle" 
             if self.karent_anime == "right_attack":
                self.karent_anime = "right_idle" 
             if self.karent_anime == "left_attack":
                self.karent_anime = "left_idle" 
         self.animes[self.karent_anime].uptate()
         super().update()
         if self.runr == True:
            self.karent_anime = "right"
         if self.runl == True:
            self.karent_anime = "left"
         if self.runu == True:
            self.karent_anime = "up"
         if self.rund == True:
            self.karent_anime = "down"
         if any((self.rund,self.runl,self.runr,self.runu)) == False: #не двигается
            if self.karent_anime == "up":
                self.karent_anime = "up_idle" 
            if self.karent_anime == "down":
                self.karent_anime = "down_idle" 
            if self.karent_anime == "right":
                self.karent_anime = "right_idle" 
            if self.karent_anime == "left":
                self.karent_anime = "left_idle" 
         if self.attaking == True:
             if self.karent_anime == "up":
                self.karent_anime = "up_attack" 
             if self.karent_anime == "down":
                self.karent_anime = "down_attack" 
             if self.karent_anime == "right":
                self.karent_anime = "right_attack" 
             if self.karent_anime == "left":
                self.karent_anime = "left_attack" 

             if self.karent_anime == "up_idle":
                self.karent_anime = "up_attack" 
             if self.karent_anime == "down_idle":
                self.karent_anime = "down_attack" 
             if self.karent_anime == "right_idle":
                self.karent_anime = "right_attack" 
             if self.karent_anime == "left_idle":
                self.karent_anime = "left_attack" 
     def render_hp(self,экран):
         pygame.draw.rect(экран,(255,0,0),(10,10,200,25),border_radius=5)
         pygame.draw.rect(экран,(0,255,0),(10,10,200*self.HP/100,25),border_top_left_radius=5,border_bottom_left_radius=5)

         pygame.draw.rect(экран,(255,0,0),(10,40,200,25),border_radius=5)
         pygame.draw.rect(экран,(0,0,255),(10,40,200*self.ener/100,25),border_top_left_radius=5,border_bottom_left_radius=5)
     def attak(self,травы,партикалс:list,враги,экран):
         self.attaking = True
         bxpl = self.atakk_aria()
         for i in враги:
            bxvr = i.get_bx()
            if bxpl.colliderect(bxvr):
                batl.run(экран,self,i)
         for i in травы.copy():
           
           if i.bxgrass.colliderect(bxpl):
               травы.remove(i)
               партиклы = random.randint(5,12)
               inwentar.add_inwentar("трава",1)
               for y in range(партиклы):
                   par = particlas.Partikl(i.x-random.randint(10,25),i.y-random.randint(10,25),random.randint(1,6))
                   партикалс.append(par)
class Anamy(Entity):
    def __init__(self, x, y, speed, width, height, map):
        super().__init__(x, y, speed, width, height, map)
        self.таймер = 0
        self.HP = 101
        self.MAXhp = 100
        self.ener = 99
        self.MAXener = 100
        self.armor = 1
     
    def render(self,экран,камера):
        self.animes[self.karent_anime].render(экран,камера,self.x,self.y)
    def update(self):
        self.animes[self.karent_anime].uptate()
        super().update()
class Spirit(Anamy):
    def __init__(self, x, y, map):
        self.animes = {
        "idle":anime.Lazy_Anime("graphics/monsters/spirit/idle",15),
        "move":anime.Lazy_Anime("graphics/monsters/spirit/move",15),
        "attack":anime.Lazy_Anime("graphics/monsters/spirit/attack",15),
        "batl":anime.Lazy_Anime("graphics/monsters/spirit/idle",15,3),
        "herd_batl":anime.Lazy_Anime("graphics/monsters/spirit/move",15,3)
        }
        self.karent_anime = "idle"
        self.width = self.animes[self.karent_anime].картинки[0].get_width()
        self.height = self.animes[self.karent_anime].картинки[0].get_height()
        self.ai_таймер = random.randint(60*5,60*10)
        self.направление = random.randint(1,4)
        self.deadh_taimer = 0
        self.tip = "Spirit"
        super().__init__(x, y, 2, self.width, self.height, map)
    def update(self,враги):
         super().update()  
         self.ai_таймер -= 1
         if self.HP <= 0:
             self.deadh_taimer += 1
         if self.deadh_taimer == 180:
             враги.remove(self)
         if self.ai_таймер <= 0:
             self.ai_таймер = random.randint(60*5,60*10)
             if self.rund == False and self.runl == False and self.runr == False and self.runu == False:
                self.направление = random.randint(1,4)
                if self.направление == 1:
                    self.rund = True
                if self.направление == 2:
                    self.runl = True
                if self.направление == 3:
                    self.runu = True
                if self.направление == 4:
                    self.runr = True
                self.karent_anime = "move"
             else:
              self.rund = False
              self.runl = False
              self.runr = False
              self.runu = False
              self.karent_anime = "idle"
def kreate_anmy(map):
    Anamy = []
    f = open("map/animes.csv")
    riter = csv.reader(f)
    for cтрока,x in enumerate(riter):
           for столбец,y in enumerate(x):
               if y == "390":
                   враг = Spirit(32*столбец,32*cтрока,map)
                   Anamy.append(враг)

    f.close()
    return(Anamy)
class Spirit_diologNPC(Spirit):
    def __init__(self, x, y, map,name):
        super().__init__(x, y, map)
        self.name = name
        self.name_image = font.render(str(self.name),True,"Black")
        self.dil_ar_bx = pygame.Rect(x-25,y-25,100,100)

    def uptate(self):
        self.animes[self.karent_anime].uptate()

    def render(self, экран, камера):
         super().render(экран, камера)
         pygame.draw.rect(экран,(255,0,0),(self.dil_ar_bx),100)

    def cehk_for_dialog(self,playr):
        cehk = False
        if self.dil_ar_bx.colliderect(playr.get_bx()):
            cehk = True
        else:
            cehk = False
        return(cehk)
