import pygame 
import random
from scripts import utils
pygame.init()

class Button:
    def __init__(self,x,y,w,h,collor,aktive_collor,text,tcollor,taktive_collor,tsize):
        self.bbx = pygame.Rect(x,y,w,h)
        self.collor = collor
        self.aktive_collor = aktive_collor
        self.text = text
        self.tcollor= tcollor
        self.taktive_color = taktive_collor
        self.font = pygame.font.Font(None,tsize)
        self.aktive = False
        self.slot = None
    def render(self,экран):
        if self.aktive == False:
            pygame.draw.rect(экран,(self.collor),(self.bbx),border_radius=7)
            tmg = self.font.render(self.text,False,self.tcollor)
            экран.blit(tmg,(self.bbx.x+self.bbx.width/2-tmg.get_width()/2,self.bbx.y+self.bbx.height/2-tmg.get_height()/2))
        if self.aktive == True:
            pygame.draw.rect(экран,(self.aktive_collor),(self.bbx),border_radius=7)
            tmg = self.font.render(self.text,False,self.taktive_color)
            экран.blit(tmg,(self.bbx.x+self.bbx.width/2-tmg.get_width()/2,self.bbx.y+self.bbx.height/2-tmg.get_height()/2))
    def update(self,klik):
        self.ip_mouse = pygame.mouse.get_pos()
        if self.bbx.collidepoint(self.ip_mouse):
            if klik == True and self.slot != None:
                self.slot()
            self.aktive = True
        else:
            self.aktive = False
class Image_button:
    def __init__(self,x,y,w,h,collor,aktive_collor,путь_картинка,border_width = 0,color_border = "black"):
        self.bbx = pygame.Rect(x,y,w,h)
        self.collor = collor
        self.aktive_collor = aktive_collor
        self.картинка = utils.load_image(путь_картинка,1)
        k = self.картинка.get_height()/h
        self.new_картинка = utils.load_image(путь_картинка,1/k)
        self.aktive = False
        self.slot = None
        self.collor_border = color_border
        self.border_width = border_width

    def update(self,klik):
        self.ip_mouse = pygame.mouse.get_pos()
        if self.bbx.collidepoint(self.ip_mouse):
            if klik == True and self.slot != None:
                self.slot()
            self.aktive = True
        else:
            self.aktive = False
    def render(self,экран):
        if self.aktive == False:
            pygame.draw.rect(экран,self.collor_border,(self.bbx.left-self.border_width,self.bbx.top-self.border_width,self.bbx.width+self.border_width*2,self.bbx.height+self.border_width*2))
            pygame.draw.rect(экран,(self.collor),(self.bbx),)
        if self.aktive == True:
            pygame.draw.rect(экран,self.collor_border,(self.bbx.left-self.border_width,self.bbx.top-self.border_width,self.bbx.width+self.border_width*2,self.bbx.height+self.border_width*2))
            pygame.draw.rect(экран,(self.aktive_collor),(self.bbx),)
        экран.blit(self.new_картинка,(self.bbx.centerx-self.new_картинка.get_width()/2,self.bbx.top),)
class Vidor_Button(Button):
    def render(self,экран):
        if self.aktive == False:
            pygame.draw.rect(экран,(self.collor),(self.bbx),border_radius=7)
            tmg = self.font.render(self.text,False,self.tcollor)
            экран.blit(tmg,(self.bbx.x,self.bbx.y+self.bbx.height/2-tmg.get_height()/2))
        if self.aktive == True:
            pygame.draw.rect(экран,(self.aktive_collor),(self.bbx),border_radius=7)
            tmg = self.font.render(self.text,False,self.taktive_color)
            экран.blit(tmg,(self.bbx.x,self.bbx.y+self.bbx.height/2-tmg.get_height()/2))