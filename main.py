import sys
import pygame
from pygame import *
from pygame.sprite import *
from pygame.time import *

from objects.Tank import Tank

#* Initialisation jeu
pygame.init()
screen = display.set_mode((640, 480), vsync=1)
display.set_caption("Projet PyGame")
clock = Clock()

#* Gestion player1
player1_keys_bind = {
    'move_left': K_LEFT,
    'move_right': K_RIGHT,
    'move_up': K_UP,
    'move_down': K_DOWN
}
player1 = Tank(player1_keys_bind)

tous_les_sprites = pygame.sprite.Group()
tous_les_sprites.add(player1)

def draw(win, player_car):
    player_car.draw(win)
    display.update()

#* Game loop
while True:
    for e in event.get():
        if e.type == QUIT:
            pygame.quit()
            sys.exit()
        
    delta = clock.tick(60)
    keys = key.get_pressed()

    draw(screen, player1)

    player1.update_event(keys, delta, screen)
    
    screen.fill((255, 192, 203))
    tous_les_sprites.update()
    
