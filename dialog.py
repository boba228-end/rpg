import pygame
import json
pygame.init()

dialog  = {}
chek_point = None

def start_dialog(name):
    global dialog
    global chek_point
    f = open(f"dialogs/{name}.json")
    dialog = json.load(f)
    f.close()

    chek_point = dialog["meta"]

def get_text():
    #что говорит персонаж
    return(dialog[chek_point]["text"])

def get_otv():
    #что можно ответить(список)
    return(dialog[chek_point]["vibora"])

def vibor_sdelan(otv):
    global chek_point
    # otv = ответ игрока(словарик)
    chek_point = otv["next"]

