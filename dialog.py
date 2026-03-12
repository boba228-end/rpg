import pygame
import json
from scripts import widget
from scripts import settings
from scripts import share
pygame.init()

dialog  = {}
chek_point = None
in_dialog = False
nome = None
max_sim = 71
font = pygame.font.Font(None,80)
font_2 = pygame.font.Font(None,40)
Buttons_vidor = [] 
def start_dialog(name):
    global dialog
    global chek_point
    global nome
    global in_dialog
    global Buttons_vidor,button
    global Buttons_vidor
    nome = name
    f = open(f"dialogs/{name}.json",encoding="utf-8")
    dialog = json.load(f)
    f.close()

    chek_point = dialog["meta"]
    in_dialog = True
    button = None
    y = 680
    for i in get_otv():
        print(i)
        u = widget.Vidor_Button(50,y,settings.WIDTH,50,"gray","gray",i['otv'],"Black","Yellow",45)
        u.slot = lambda otv = i:vibor_sdelan(otv)
        Buttons_vidor.append(u)
        y -= 45
        

def get_text():
    #что говорит персонаж
    return(dialog[chek_point]["text"])

def get_otv():
    #что можно ответить(список)
    return(dialog[chek_point]["vibora"])

def vibor_sdelan(otv):
    global chek_point
    global in_dialog
    if "aqtion" in otv:
        if otv["aqtion"] == "add exp":
            caunt = otv["caunt"]
            share.inkris_exp(caunt)
    # otv = ответ игрока(словарик)
    chek_point = otv["next"]
    if chek_point == "конец":
        in_dialog = False
        return()
    Buttons_vidor.clear()
    y = 680
    for i in get_otv():
        u = widget.Vidor_Button(50,y,settings.WIDTH,50,"gray","gray",i['otv'],"Black","Yellow",45)
        u.slot = lambda otv = i:vibor_sdelan(otv)
        Buttons_vidor.append(u)
        y -= 45

def change_meta(name,new_meta):

    global in_dialog
    start_dialog(name)
    in_dialog = False
    f = open(f"dialogs/{name}.json","w")
    dialog["meta"] = new_meta
    json.dump(dialog,f)
    f.close()



def render(экран,klik):
    if in_dialog == False:
        return
    else:
        name_image = font.render(nome,True,"black")
        экран.blit(name_image,(35,412))
        pygame.draw.rect(экран,"gray",(0,2/3*settings.HEIGHT,settings.WIDTH,settings.HEIGHT/3))
        text = get_text()
        y = 540
        for i in Buttons_vidor:
            i.render(экран)
            i.update(klik)
        for i in range(0,len(text),max_sim):
            sub_text = text[i:i+max_sim]
            tetx_image = font_2.render(sub_text,True,(50,50,50))
            экран.blit(tetx_image,(50,y))
            y += 55
