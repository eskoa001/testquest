# 1 - importer biblioteker
import random as r
import pygame as pg
from pygame.locals import *
import sys
import math

# 2 - definer constanter
BACKGROUND = (135, 206, 235) # definerer bakgrunns farge som himmel blå
Farger = {
  "Blå": (0,0,255),
  "Rød": (255,0,0),
  "Grønn": (0,255,0),
  "gress" : (150,255,100)
}
WINDOW_WIDTH = 640 # definerer bredde på vinduet
WINDOW_HEIGHT = 480 # definerer høyde på vinduet
FRAMES_PER_SECOND = 60 # definerer hvor mange frames (bilder) som vises hvert sekund
speed = 200/FRAMES_PER_SECOND # definerer farten til spiller
keys = [K_a,K_b,K_c,K_d,K_e,K_f,K_g,K_h,K_i,K_j,K_k,K_l,K_m,K_n,K_o,K_p,K_q,K_r,K_s,K_t,K_u,K_v,K_w,K_x,K_y,K_z,K_SPACE]
keys_alt = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"," "]

# 2.5 definer klasser
class spiller: 
    def __init__(self, x, y, hp, penger, dir):
        self.x = x
        self.y = y
        self.hp = hp
        self.penger = penger
        self.dir = dir
class felt:
    def __init__(self, a, b, forklaring, hotkey, funk):
        self.a = a
        self.b = b
        self.forklaring = forklaring
        self.hotkey = hotkey
        self.funk = funk
class level:
    def __init__(self, alle_felt, oppdater, tegn, start):
        self.alle_felt = alle_felt
        self.oppdater = oppdater
        self.tegn = tegn
        self.start = start

# 2.5.5 definer funksjoner
def _quit(): # avslutter spillet ved å lukke vinduet og slutte programmet
    pg.quit()  
    sys.exit()
def tast_trykket(t): # tester om tast a er trykket ned denne framen
    return trykkede_taster[t] and not trykkede_taster_f[t] # returnerer True hvis en tast a er trykket denne framen men ikke forige. Returnerer ellers false
def spiller_i_felt(f): 
    return _spiller.x > f.a and _spiller.x < f.b
def ny_snakkeboble(a):
    while (font.size(a)[0] > bobble_lengde):
        txt = ""
        for i in range(len(a)):
            if (font.size(txt+a[i])[0] < bobble_lengde):
                txt += a[i]
            else:
                a = a[i:]
                alle_snakkebobbler.append(txt)
                break
    alle_snakkebobbler.append(a)

    # til test level
def funk1():
    ny_snakkeboble("Bla blabla")
def funk2():
    print("2")
def levelstart1():
    pass
def leveltick1():
    pass
def leveltegn1():
    pg.draw.rect(window,Farger["gress"],(0,WINDOW_HEIGHT-200,WINDOW_WIDTH,200)) # gress

# 3 - Initialize verden
pg.init()
window = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pg.time.Clock()
 
# 4 - lag fonter 
font = pg.font.SysFont("Arial", 24)
font_big = pg.font.SysFont("Arial", 50)
font_small = pg.font.SysFont("Arial", 18)

# 5 - definer variabeler
tid = 0
komando = ""
alle_snakkebobbler = []
_spiller = spiller(WINDOW_WIDTH/2,400,100,0,1)
alle_leveler = [
    level( # test level
    [
        felt(100,200,"interact","x", funk1), 
        felt(100,300,"interact","y", funk2)
    ], 
    leveltick1,
    leveltegn1,
    levelstart1),
    level( # test level 2 med samme funk som level 1
    [
        felt(100,200,"interact","x", funk1), 
        felt(100,300,"interact","y", funk2)
    ], 
    leveltick1,
    leveltegn1,
    levelstart1)
]
_level = alle_leveler[0]
_level.start()
aktiv_felt = []
    # variabler til rendering
step_speed = 10
scale = 5
l = 5
r = 10
border = 3
bobble_lengde = WINDOW_WIDTH-border*4-200

# 6 - Loop for alltid
while True:

    # 7 - test etter og håndter events
    for event in pg.event.get():
        if event.type == pg.QUIT:            
            _quit() # lukker programmet om vinduet krysses ut av bruker

    # 8 - gjør alle "per frame" handlinger
        # henter ny input fra bruker
    trykkede_taster = pg.key.get_pressed()
    trykkede_musetaster = pg.mouse.get_pressed()
        # oppdater tid
    tid += 1/FRAMES_PER_SECOND
        # beveg spiller
    if (len(alle_snakkebobbler)==0): # --------------------------------------------------------
        if (trykkede_taster[K_LEFT]): _spiller.x -= speed; _spiller.dir=-1
        if (trykkede_taster[K_RIGHT]): _spiller.x += speed; _spiller.dir=1
        if (not (trykkede_taster[K_LEFT] ^ trykkede_taster[K_RIGHT])):
            _spiller.dir = 0 
    t = alle_leveler.index(_level)
    if (_spiller.x>WINDOW_WIDTH):
        if (t < len(alle_leveler)-1):
            _level = alle_leveler[t+1]
            _level.start()
            _spiller.x = 0
            print("Ny level:", t+1)
        else:
            _spiller.x = WINDOW_WIDTH
    if (_spiller.x<0):
        if (t > 0):
            _level = alle_leveler[t-1]
            _level.start()
            _spiller.x = WINDOW_WIDTH
            print("Ny level:", t-1)
        else:
            _spiller.x = 0
        # oppdater felt
    aktiv_felt = []
    for i in _level.alle_felt:
        if (spiller_i_felt(i)):
            aktiv_felt.append(i)
        # oppdater komando
    for i in range(len(keys)):
        if (tast_trykket(keys[i])):
            komando += str(keys_alt[i])
    if (tast_trykket(K_BACKSPACE)):
        komando = komando[:-1]
    if (tast_trykket(K_RETURN)):
        for i in aktiv_felt:
            if (komando == i.hotkey):
                i.funk()
        komando = ""
        # oppdater snakkeboble
    if (tast_trykket(K_TAB)):
        alle_snakkebobbler = alle_snakkebobbler[1:]

        # oppdater levelen
    _level.oppdater()

        # lagrer denne framens input til neste frame. Vi bruker dette for å teste etter endringer
    trykkede_taster_f = trykkede_taster
    trykkede_musetaster_f = trykkede_musetaster

    # 9 - Clear the window
    window.fill(BACKGROUND)
    
    # 10 - tegn alle elementene
        # tegn level
    _level.tegn()
        # tegn spiller
    if (_spiller.dir == 1 or _spiller.dir == -1):
        step_d = (math.sin(tid*step_speed)+1)/2
    else: step_d = 0
    if (_spiller.dir == 1):
        pg.draw.line(window, (50, 50, 50), (_spiller.x, _spiller.y-(30)*scale), (_spiller.x, _spiller.y-(10)*scale), l*scale) # kropp
        pg.draw.rect(window, (139, 69, 19), (_spiller.x+(-10-l/2)*scale, _spiller.y-(30+step_d)*scale, 10*scale, 15*scale)) # sekk
        pg.draw.ellipse(window, (50, 50, 50), (_spiller.x-r/2*scale, _spiller.y-(30+r)*scale, r*scale, r*scale)) # hode
        pg.draw.line(window, (50, 50, 50), (_spiller.x-7*scale, _spiller.y-(30+r/2)*scale), (_spiller.x+7*scale, _spiller.y-(30+r/2)*scale), int(round(l*scale/5,0))) # hatt
    if (_spiller.dir == -1):
        pg.draw.line(window, (50, 50, 50), (_spiller.x, _spiller.y-(30)*scale), (_spiller.x, _spiller.y-(10)*scale), l*scale) # kropp
        pg.draw.rect(window, (139, 69, 19), (_spiller.x+l/2*scale, _spiller.y-(30+step_d)*scale, 10*scale, 15*scale)) # sekk
        pg.draw.ellipse(window, (50, 50, 50), (_spiller.x-r/2*scale, _spiller.y-(30+r)*scale, r*scale, r*scale)) # hode
        pg.draw.line(window, (50, 50, 50), (_spiller.x-7*scale, _spiller.y-(30+r/2)*scale), (_spiller.x+7*scale, _spiller.y-(30+r/2)*scale), int(round(l*scale/5,0))) # hatt
    if (_spiller.dir == 0):
        pg.draw.line(window, (50, 50, 50), (_spiller.x, _spiller.y-(30)*scale), (_spiller.x, _spiller.y-(10)*scale), l*scale) # kropp
        pg.draw.rect(window, (139, 69, 19), (_spiller.x+(-5)*scale, _spiller.y-(30+step_d)*scale, 10*scale, 15*scale)) # sekk
        pg.draw.ellipse(window, (50, 50, 50), (_spiller.x-r/2*scale, _spiller.y-(30+r)*scale, r*scale, r*scale)) # hode
        pg.draw.line(window, (50, 50, 50), (_spiller.x-7*scale, _spiller.y-(30+r/2)*scale), (_spiller.x+7*scale, _spiller.y-(30+r/2)*scale), int(round(l*scale/5,0))) # hatt
        # tegn komando boks
    pg.draw.rect(window, (0, 0, 0), (0,WINDOW_HEIGHT-50,WINDOW_WIDTH,50))
    txt = "> " + komando
    if (math.sin(tid*5)<=0): txt += "_"
    bilde = font.render(txt, True, (255, 255, 255))
    window.blit(bilde, (10, WINDOW_HEIGHT+(50-font.size(txt)[1])/2-50))
        # tegn tips linje
    t = 10
    for i in aktiv_felt:
        txt = "[" + i.hotkey + "] " + i.forklaring
        bilde = font.render(txt, True, (255, 255, 255))
        window.blit(bilde, (10, t))
        t += font.size(txt)[1] + 5  
        # tegn sankke boble
    if (alle_snakkebobbler != []):
        pg.draw.rect(window, (100, 100, 100), (0,WINDOW_HEIGHT-100,WINDOW_WIDTH,50))
        pg.draw.rect(window, (255, 255, 255), (border,WINDOW_HEIGHT-(100-border),WINDOW_WIDTH-border*2,50-border*2))
        txt = alle_snakkebobbler[0]
        if (len(alle_snakkebobbler) >= 2): txt += " ..."
        bilde = font.render(txt, True, (0, 0, 0))
        window.blit(bilde, (20, WINDOW_HEIGHT-100+(50-font.size(txt)[1])/2))
        txt = "Trykk TAB for neste"
        bilde = font_small.render(txt, True, (0, 0, 0))
        window.blit(bilde, (WINDOW_WIDTH-font_small.size(txt)[0]-border*2, WINDOW_HEIGHT-50-font_small.size(txt)[1]-border*2))
        txt = "(" + str(len(alle_snakkebobbler)-1) +  ")"
        bilde = font_small.render(txt, True, (0, 0, 0))
        window.blit(bilde, (WINDOW_WIDTH-font_small.size(txt)[0]-border*2, WINDOW_HEIGHT-100+border*2))

    # 11 - Update the window
    pg.display.update()

    # 12 - Slow things down a bit
    clock.tick(FRAMES_PER_SECOND)  # make pygame wait
