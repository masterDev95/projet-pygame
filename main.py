import pygame
from pygame import *
from pygame.sprite import *
from pygame.time import *
from objects.Bullet import Bullet
from objects.Explosion import Explosion

from objects.Tank import Tank
from menu import *

#* Initialisation jeu
pygame.init()
screen = display.set_mode((640, 480), vsync=1)

# Variable
dark = (0, 0, 0)

# On créer l'écran et on charge les différentes images
res = (1280, 720)
display = pygame.display.set_mode(res)

fond = pygame.image.load("assets/fond_jeu.png")
fond = pygame.transform.scale(fond, res)
fond.set_alpha(128)
pygame.Surface.convert_alpha(fond)

# Musique d'intro
pygame.mixer.init()
generique = 'assets/sons/musique_accueil.mp3'
pygame.mixer.music.load(generique)
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play()

# On met un nom à la fenêtre et on positionne l'image de fond
pygame.display.set_caption("Tank One")
icone = pygame.image.load('assets/icone.png')
pygame.display.set_icon(icone)

# Effet fade in ecran titre
for i in range(0, 255, 5):
    fond.set_alpha(i)
    pygame.Surface.convert_alpha(fond)
    display.fill(dark)
    display.blit(fond, (0, 0))
    pygame.display.flip()
    pygame.time.wait(int(60/2))

#On part dans le Menu
fonct_menu(display)


