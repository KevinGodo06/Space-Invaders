import Library.g2d as g2d
from random import randint
import os
import sys

# --- FIX PER I PERCORSI ---
# Trova la cartella dove risiede questo file .py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Funzione helper per caricare le risorse
def resource_path(relative_path):
    return os.path.join(BASE_DIR, relative_path)
# ---------------------------

DMARGIN = 50
ARENA_W, ARENA_H, ASTRO_W, ASTRO_H = 600, 600, 28, 16

class Astro:
    def __init__(self, x, y, w, h):
        self._x = x
        self._y = y
        self._w = w
        self._h = h
        self._dx = 5
        self._dy = 5
        self._c = 0
        self._dx_alieni = 3
        self._dy_alieni = 5
    
    def pos(self):
        return self._x, self._y

    def teleport(self, x, y):
        self._x = x
        self._y = y
        
    def move(self, tasto):
        if self._x - DMARGIN >= 0 and self._x + DMARGIN <= ARENA_W - ASTRO_W:
            if "ArrowLeft" in tasto:
                self._x -= self._dx
            if "ArrowRight" in tasto:
                self._x += self._dx
        else:
            if self._x - DMARGIN < 0 and "ArrowRight" in tasto:
                self._x += self._dx
            else:
                if self._x + DMARGIN > ARENA_W - ASTRO_W and "ArrowLeft" in tasto:
                    self._x -= self._dx
                    
    def shoot_move_alieno(self):
        self._y += self._dy
        
    def shoot_move_personaggio(self):
        self._y -= self._dy
        # NOTA: Uso resource_path qui
        g2d.draw_image(resource_path("img/sparo1.png"), (self._x, self._y))
       
    def natural_move(self):
        if self._c < 150:
            if self._c % 4 == 0:
                self._x += self._dx_alieni
            self._c += 1
        else:
            self._c = 0
            self._y += self._dy_alieni
            self._dx_alieni = -self._dx_alieni
            
    def shootinalien(self, x, y):
        if self._x <= x <= self._x + self._w and self._y <= y <= self._y + self._h:
            return True
        else:
            return False
        
a = Astro((ARENA_W - DMARGIN)/2, ARENA_H - ASTRO_H - DMARGIN, 28, 16)

# Creazione alieni
alieni = [
    Astro(ARENA_W * 10, ARENA_H * 10, 32, 20),
    Astro(100 + ASTRO_W/2, DMARGIN*1, 32, 20), Astro(150 + ASTRO_W/2, DMARGIN*1, 32, 20), Astro(200 + ASTRO_W/2, DMARGIN*1, 32, 20), Astro(250 + ASTRO_W/2, DMARGIN*1, 32, 20), Astro(300 + ASTRO_W/2, DMARGIN*1, 32, 20), Astro(350 + ASTRO_W/2, DMARGIN*1, 32, 20),
    Astro(100 + ASTRO_W/2, DMARGIN*2, 32, 20), Astro(150 + ASTRO_W/2, DMARGIN*2, 32, 20), Astro(200 + ASTRO_W/2, DMARGIN*2, 32, 20), Astro(250 + ASTRO_W/2, DMARGIN*2, 32, 20), Astro(300 + ASTRO_W/2, DMARGIN*2, 32, 20), Astro(350 + ASTRO_W/2, DMARGIN*2, 32, 20),
    Astro(100 + ASTRO_W/2, DMARGIN*3, 32, 20), Astro(150 + ASTRO_W/2, DMARGIN*3, 32, 20), Astro(200 + ASTRO_W/2, DMARGIN*3, 32, 20), Astro(250 + ASTRO_W/2, DMARGIN*3, 32, 20), Astro(300 + ASTRO_W/2, DMARGIN*3, 32, 20), Astro(350 + ASTRO_W/2, DMARGIN*3, 32, 20),
    Astro(100 + ASTRO_W/2, DMARGIN*4, 32, 20), Astro(150 + ASTRO_W/2, DMARGIN*4, 32, 20), Astro(200 + ASTRO_W/2, DMARGIN*4, 32, 20), Astro(250 + ASTRO_W/2, DMARGIN*4, 32, 20), Astro(300 + ASTRO_W/2, DMARGIN*4, 32, 20), Astro(350 + ASTRO_W/2, DMARGIN*4, 32, 20),
]

c = 0
countdown = 0
alienshoot = Astro(ARENA_W, ARENA_H, 6, 12)
myshoot = Astro(ARENA_W, ARENA_H, 4, 14)
b = False
vittoria = False

vite = 3 

def tick():
    global c, b, countdown, vittoria, vite

    if vite >= 0 and vittoria == False:
        g2d.clear_canvas()
        g2d.set_color((0, 0, 0))
        g2d.draw_rect((0,0), (ARENA_W, ARENA_H))
        
        # Uso resource_path per tutte le immagini
        g2d.draw_image(resource_path("img/astronave28x16.png"), a.pos())

        for i in range(vite):
            g2d.draw_image(resource_path("img/Vita.png"), (10, DMARGIN + 50 * i))

        for i in alieni:
            g2d.draw_image(resource_path("img/alieno32x20.png"), i.pos())
            i.natural_move()

        if (c % 120 == 0):
            AlienShooting = randint(0, len(alieni)-1)
            x, y = alieni[AlienShooting].pos()
            alienshoot.teleport(x, y)

        alienshoot.shoot_move_alieno()
        g2d.draw_image(resource_path("img/sparo2.png"), alienshoot.pos())

        t = g2d.current_keys()
        a.move(t)

        if "Spacebar" in t and not b:
            x, y = a.pos()
            x += 12
            myshoot.teleport(x, y)
            g2d.draw_image(resource_path("img/sparo1.png"), (x, y))
            b = True
            countdown = 0

        if(b):
            countdown += 1

        if(countdown >= 120):
            b = False
        myshoot.shoot_move_personaggio()

        for i in alieni:
            x, y = myshoot.pos()

            if i.shootinalien(x, y):
                alieni.remove(i)
                b = False
                myshoot.teleport(ARENA_W, ARENA_H)

        x, y = alienshoot.pos()
        
        c += 1

        if a.shootinalien(x, y):
            alienshoot.teleport(ARENA_W, ARENA_H)
            vite -= 1

        if len(alieni) == 1:
            vittoria = True
        
    else:
        if vittoria == True and vite > -1:
            g2d.draw_image(resource_path("img/Hai vinto.jpg"), (0, 0))
        else:
            g2d.draw_image(resource_path("img/Hai perso.png"), (0, 0))

    t = g2d.current_keys()

    if "Enter" in t:
        g2d.close_canvas()

        
def main():
    g2d.init_canvas((ARENA_W, ARENA_H))
    g2d.main_loop(tick, 60)
main()