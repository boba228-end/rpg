import pygame 
import dialog
from scripts import settings
from scripts import antites
from scripts import map
from scripts import grass
from scripts import inwentar
from scripts import particlas
from scripts import widget
from scripts import batl


pygame.init()
экран = pygame.display.set_mode((settings.WIDTH,settings.HEIGHT))
inwentar.load()
batl.load_fon()
glass_1 = pygame.Surface((settings.WIDTH,settings.HEIGHT),pygame.SRCALPHA)
glass_dark = pygame.Surface((settings.WIDTH,settings.HEIGHT),pygame.SRCALPHA)
часы = pygame.time.Clock()
карта = map.КАРТА()
ent = antites.Entity(100,100,5,80,50,карта)
pl = antites.Playr(10,10,10,карта)
NPCs_dio = []
oleg = antites.Spirit_diologNPC(100,100,карта,"оleg")
NPCs_dio.append(oleg)
травы = grass.kerate_grass()
иветнтарь = False
враги = antites.kreate_anmy(карта)
print(враги)
partikals = []
steat = "game"
clik = False
inwentaria = False
def slot_con():
      global steat
      steat = "game"
def inkris_exp(kol_vo = 1):
     pl.exp += kol_vo
     if pl.exp == 100:
          dialog.change_meta("oleg","good")
          
widget = widget.Button(settings.WIDTH/2-100,300,200,50,"black","yellow","continue","white","black",55)
widget.slot = slot_con
while True:
     print(len(враги))
     pygame.display.set_caption(str(pygame.mouse.get_pos()))
     if steat == "game":
          pl.ener += 0.02
          
          if pl.ener >= 100:
                pl.ener = 100
          экран.fill((0,0,0))
          
          XM = pygame.mouse.get_pos()[0]
          yM = pygame.mouse.get_pos()[1]
          pl.x += (XM+карта.камера[0] - pl.x) /5
          pl.y += (yM+карта.камера[1] - pl.y) /5
          часы.tick(settings.FPS)
          ent.update()
          ent.render(экран)
          карта.render(экран)
          карта.камера[0] += (pl.x-экран.get_width()/2-карта.камера[0])
          карта.камера[1] += (pl.y-экран.get_height()/2-карта.камера[1])
          if карта.камера[0] < 0:
               карта.камера[0] = 0
          if карта.камера[1] < 0:
               карта.камера[1] = 0
          if карта.камера[1] > карта.карта.get_height() - settings.HEIGHT :
               карта.камера[1] =  карта.карта.get_height() - settings.HEIGHT
          if карта.камера[0] > карта.карта.get_width() - settings.WIDTH :
               карта.камера[0] =  карта.карта.get_width() - settings.WIDTH
          for i in partikals:
               i.render(экран,карта.камера)
               i.uptate(partikals)
          pl.update()
          pl.render(экран,карта.камера)
          for i in враги:
               i.render(экран,карта.камера)
               i.update(враги) 
          for i in NPCs_dio:
                i.render(экран,карта.камера)
                i.uptate()
          for i in травы:
               i.render(экран,карта.камера)
          pl.render_hp(экран) 
          clik = False
          if inwentaria == True:
                inwentar.render(экран)
          if иветнтарь == True:
               inwentar.render(экран)
               inwentar.utate()
          for ev in pygame.event.get():
                    if ev.type == pygame.MOUSEBUTTONDOWN:
                         clik = True
                    if ev.type == pygame.QUIT:
                         exit(0)
                    if ev.type == pygame.KEYDOWN:
                         if ev.key == pygame.K_SPACE:
                              pl.attak(травы,partikals,враги,экран)
                         if ev.key == pygame.K_a:
                              pl.runl = True
                         if ev.key == pygame.K_e:
                              inwentaria = not(inwentaria)
                         if ev.key == pygame.K_d:
                              pl.runr = True
                         if ev.key == pygame.K_w:
                              pl.runu = True
                         if ev.key == pygame.K_g:
                               inkris_exp(100)
                         if ev.key == pygame.K_s:
                              pl.rund = True
                         if ev.key == pygame.K_TAB:
                              иветнтарь = not иветнтарь
                         if ev.key == pygame.K_ESCAPE:
                              steat = "pause"
                              glass_1.blit(экран,(0,0))
                    if ev.type == pygame.KEYUP:
                         if ev.key == pygame.K_a:
                              pl.runl = False
                         if ev.key == pygame.K_d:
                              pl.runr = False
                         if ev.key == pygame.K_w:
                              pl.runu = False         
                         if ev.key == pygame.K_s:
                              pl.rund = False
          
          pygame.display.update()
     if steat == "pause":
          glass_dark.fill((0,0,0,200))
          экран.blit(glass_1,(0,0))
          экран.blit(glass_dark,(0,0))
          #smoth = pygame.transform.smoothscale(экран,(settings.WIDTH/2,settings.HEIGHT/2),экран)
          #экран.blit(smoth,(0,0))
          widget.render(экран)     
          widget.update(clik)  
          clik = False
          for ev in pygame.event.get():
               if ev.type == pygame.MOUSEBUTTONDOWN:
                         clik = True
               if ev.type == pygame.QUIT:
                         exit(0)
               if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_ESCAPE:
                              steat = "game"
          pygame.display.update()