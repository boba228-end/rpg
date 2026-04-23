import pygame
from scripts import settings

vopros = ""
pygame.init()
max_sim = 24
time = pygame.time.Clock()
leters = "qwertyuiop[]';lkjhgfdsazxcvbnm,."
ruleters = "йцукенгшщзхъэждлорпавыфячсмитьбю"
font_text = pygame.font.Font("scripts/imperial_one/Webfont/Imperial Web.ttf",50)
def konwert(simvol):
    if simvol == ("space"):
        return(" ")
    index = leters.index(simvol)
    return(ruleters[index])
def run(экран:pygame.Surface):
    global vopros
    while True:
        time.tick(settings.FPS)
        экран.fill((0,0,0))
        y = 100
        for i in range(0,len(vopros),max_sim):
            sub_text = vopros[i:i+max_sim]
            tetx_image = font_text.render(sub_text,True,(50,50,50))
            экран.blit(tetx_image,(50,y))
            y += 55

        for ev in pygame.event.get():
            if ev.type == pygame.KEYDOWN:
                kname = pygame.key.name(ev.key)
                vopros += konwert(kname)
        pygame.display.update()