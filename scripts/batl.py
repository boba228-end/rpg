xpp = 0
import pygame
from scripts import utils
from scripts import settings
from scripts import anime
from scripts import widget
import random
pygame.init()
select = None
clik = False
ВРАГ = None
ctoit = "vыbor"
ctoit_2_0 = "vыborь"
run_batle = True

def clik_magik():
    global select
    select = magik_buttun
def clik_sword():
    global select
    select = sword_button
def clik_run():
    global select
    select = run_buttun
def clik_fire():
    global ctoit_2_0,ctoit
    if ctoit == "vыbor" and PLAYR.ener >= 30:
        PLAYR.ener -= 30
        ctoit = "fire"
        ctoit_2_0 = "go"
def load_fon():
    global фон,земля,sword_button,magik_buttun,run_buttun,sword_button_sword,sword_button_fire,защита,font,efekt_fire,deadf,fire_sword,fireball_anime
    фон = utils.load_image("graphics/font/ja7ti1z834f91.jpg",0.6)
    земля = utils.load_image("graphics/font/i.png",4)
    защита = utils.load_image("graphics/grass/shield (1).png",1)
    efekt_fire = utils.load_image("graphics/grass/fire.png",2)
    deadf = utils.load_image("graphics/grass/down.png",2)
    fire_sword = utils.load_image("graphics/grass/Fired Sword.png",0.4)
    fireball_anime = anime.Lazy_Anime("graphics/fireboll",1,1)

    font = pygame.font.Font(None,55)
    f = 5
    #главные кнопки
    magik_buttun = widget.Image_button(10,settings.HEIGHT-земля.get_height()+f+земля.get_height()/3,300,земля.get_height()/3-2*f,(58,58,58),(70,70,70),"graphics/grass/3d-fire.png",f,"green")
    magik_buttun.slot = clik_magik 
    run_buttun = widget.Image_button(10,settings.HEIGHT-земля.get_height()+f+земля.get_height()/3*2,300,земля.get_height()/3-2*f,(58,58,58),(70,70,70),"graphics/grass/run.png",f,(255,255,255))
    run_buttun.slot = clik_run
    sword_button = widget.Image_button(10,settings.HEIGHT-земля.get_height()+f,300,земля.get_height()/3-2*f,(58,58,58),(70,70,70),"graphics/grass/sword.png",f,(255,140,0))
    sword_button.slot = clik_sword
    #не главные кнопки
    sword_button_fire = widget.Image_button(345,660,200,земля.get_height()/3-2*f,(58,58,58),(70,70,70),"graphics/grass/sword (2).png",f,"orange")
    sword_button_fire.slot = clik_fire
    sword_button_sword = widget.Image_button(345,580,200,земля.get_height()/3-2*f,(58,58,58),(70,70,70),"graphics/font/slash.png",f,"orange")
def render(экран,playr,враг):
    global ctoit
    global clik
    global xpp
    global x_fire
    XM = pygame.mouse.get_pos()[0]
    yM = pygame.mouse.get_pos()[1]
    pygame.display.set_caption(str([XM,yM]))
    #sword_button_sword.bbx.x = XM
    #sword_button_sword.bbx.y = yM
    анимация_игрок = playr.animes[pl_anime]
    анимация_враг = враг.animes[vr_anime]
    анимация_враг.render(экран,(0,0),925,360)
    анимация_игрок.render(экран,(0,0),xpp,360)
    анимация_враг.uptate()
    экран.blit(защита,(10,70))
    экран.blit(защита,(экран.get_width()-10-защита.get_width(),70))
    armor1 = font.render(str(playr.armor),True,"black")
    armor2 = font.render(str(враг.armor),True,"black")
    sword_button.render(экран)
    sword_button.update(clik)
    экран.blit(armor2,(экран.get_width()-10-защита.get_width()+защита.get_width()/2-armor1.get_width()/2+1,70+защита.get_height()/2-armor1.get_height()/2+5))
    экран.blit(armor1,(10+защита.get_width()/2-armor1.get_width()/2+1,70+защита.get_height()/2-armor1.get_height()/2+5))
    magik_buttun.render(экран)
    magik_buttun.update(clik)
    run_buttun.render(экран)
    run_buttun.update(clik)
    if ctoit == "s_fireball":
        fireball_anime.render(экран,(0,0),x_fire,y_fire)
        x_fire -= 5
        if x_fire <= 185:
            playr.HP -= 25 * (1 - playr.armor/10)
            ctoit = "vыbor"
            playr.ener += random.randint(5,10)
            ВРАГ.ener += random.randint(5,10)
    #atttack_buton

    if select == sword_button:
        sword_button_sword.render(экран)
        sword_button_sword.update(clik)
        sword_button_fire.render(экран)
        sword_button_fire.update(clik)
    #xп
    pygame.draw.rect(экран,(255,0,0),(10,10,300,30),border_radius=5)
    pygame.draw.rect(экран,(0,255,0),(10,10,300*playr.HP/100,30),border_top_left_radius=5,border_bottom_left_radius=5)
    pygame.draw.rect(экран,(255,0,0),(settings.WIDTH-310,10,300,30),border_radius=5)
    pygame.draw.rect(экран,(0,255,0),(settings.WIDTH-10-300*враг.HP/100,10,300*враг.HP/100,30),border_top_right_radius=5,border_bottom_right_radius=5)
    #энергия
    pygame.draw.rect(экран,(255,0,0),(10,40,300,30),border_radius=5)
    pygame.draw.rect(экран,(0,0,255),(10,40,300*playr.ener/100,30),border_top_left_radius=5,border_bottom_left_radius=5)
    pygame.draw.rect(экран,(255,0,0),(settings.WIDTH-310,40,300,30),border_radius=5)
    pygame.draw.rect(экран,(0,0,255),(settings.WIDTH-10-300*враг.ener/100,40,300*враг.ener/100,30),border_top_right_radius=5,border_bottom_right_radius=5)
    #энергия
def update():
    global ctoit
    global PLAYR
    global xpp
    global ВРАГ
    if select == magik_buttun:
        magik_buttun.aktive = True
    if select == sword_button:
        sword_button.aktive = True
    if select == run_buttun:
        run_buttun.aktive = True
        ctoit = "vыbor"
        PLAYR.runl = False
        PLAYR.runu = False
        PLAYR.rund = False
        PLAYR.runr = False
        xpp = 0
        ВРАГ.ener = 100
        ВРАГ.HP = 100


def vrag_vibor():
    global ctoit,taimer,vr_anime,x_fire,y_fire
    if ВРАГ.tip == "Spirit":
        if random.randint(1,1) == 1 and ВРАГ.ener >= 25:
            print ("ok")
            ctoit = "s_fireball"
            taimer = 60
            x_fire = 725
            y_fire = 325
            vr_anime = "herd_batl"
            ВРАГ.ener -= 25
        else:
            ctoit = "Vыbor"
def run(экран,playr,враг,):  
        global ВРАГ,ctoit_2_0,ctoit,xpp,pl_anime,vr_anime,PLAYR
        ВРАГ = враг
        PLAYR = playr
        pl_anime = "batl_anime"
        vr_anime = "batl"
        taimer = 240
        podg_taimer = 500
        clock = pygame.time.Clock()
        vrag_hp_taimer = 0
        while True:
            global clik
            global select
            clock.tick(120)
            экран.fill((31,61,87))
            экран.blit(фон,(0,0))
            экран.blit(земля,(0,settings.HEIGHT-земля.get_height()))
            if ВРАГ.HP <= 0:
                return
            if vrag_hp_taimer > 0:
                экран.blit(efekt_fire,(950,290))
                экран.blit(deadf,(950+efekt_fire.get_width(),290))
                vr_anime = "herd_batl"
                ВРАГ.HP -= 0.01
                vrag_hp_taimer -= 1
            if vrag_hp_taimer == 1:
                vr_anime = "batl"
            render(экран,playr,враг)
            update()
            
            if ctoit == "fire":
                if ctoit_2_0 == "go":
                    xpp += 5
                    if xpp >= 680 :
                        ctoit_2_0 = "hit"
                        taimer = 120
                if ctoit_2_0 == "hit":
                    taimer -= 1
                    if taimer <= 100:
                        pl_anime = "batl_attak"
                        экран.blit(fire_sword,(800,500-47))
                    if taimer == 99:
                        ВРАГ.HP -= 30 * (1 - ВРАГ.armor/10)
                        vrag_hp_taimer = 500*2
                    if taimer == 0:
                       pl_anime = "batl_anime"
                       ctoit_2_0 = "home"
                if ctoit_2_0 == "home":
                    xpp -= 5
                    if xpp <= 0 :
                        ctoit = "podgotovka_VRAG"
                        podg_taimer = 240
            if ctoit == "podgotovka_VRAG" and vrag_hp_taimer == 0:
                podg_taimer -= 1
                vr_anime = "batl" 
                if podg_taimer == 0:
                    ctoit = "vыbor_VRAG"
            if ctoit == "vыbor_VRAG" and vrag_hp_taimer == 0:
                vrag_vibor()
            if select == run_buttun and random.randint(1,2) == 2:
                select = None
                return
                
            clik = False
            for ev in pygame.event.get():
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    clik = True
                if ev.type == pygame.QUIT:
                    exit(0)
            pygame.display.update()
