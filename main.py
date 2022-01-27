import sys
import pygame
from pygame import *
from pygame.sprite import *
from pygame.time import *
from objects.Bullet import Bullet

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
    'move_down': K_DOWN,
    'fire': K_SPACE
}
player1 = Tank(player1_keys_bind)

tous_les_sprites = pygame.sprite.Group()
tous_les_sprites.add(player1)

def draw(win):
    for object in tous_les_sprites:
        object.update_event(keys, delta)
        object.draw(screen)
    display.update()

#* Game loop
while True:
    for e in event.get():
        if e.type == QUIT:
            pygame.quit()
            sys.exit()
        
    delta = clock.tick(60)
    keys = key.get_pressed()
    
    if (player1.invoke_bullet):
        tous_les_sprites.add(Bullet(player1.angle, player1.rect.centerx, player1.rect.bottom))
        player1.invoke_bullet = False

    draw(screen)

    
    screen.fill((255, 192, 203))
    tous_les_sprites.update()
    
