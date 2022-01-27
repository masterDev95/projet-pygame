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

tous_les_tanks = pygame.sprite.Group()
tous_les_bullets = pygame.sprite.Group()
tous_les_tanks.add(player1)

def draw(win):
    for bullet in tous_les_bullets:
        bullet.update_event(delta)
        x, y = (bullet.rect.x, bullet.rect.y)
        w, h = bullet.image.get_size()
        bullet.blit_rotate(screen, bullet.image, (x, y), (w/2, h/2), bullet.angle)
        
    for tank in tous_les_tanks:
        tank.update_event(keys, delta)
        x, y = (tank.rect.x, tank.rect.y)
        w, h = tank.image.get_size()
        tank.blit_rotate(screen, tank.image, (x, y), (w/2, h/2), tank.angle)
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
        tous_les_bullets.add(Bullet(player1.angle, player1.origin.x, player1.origin.y))
        player1.invoke_bullet = False

    draw(screen)

    
    screen.fill((255, 192, 203))
    tous_les_tanks.update()
    
