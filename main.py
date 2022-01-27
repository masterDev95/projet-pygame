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

player2_keys_bind = {
    'move_left': K_q,
    'move_right': K_d,
    'move_up': K_z,
    'move_down': K_s,
    'fire': K_TAB
}

player1 = Tank(player1_keys_bind, 64, 64)
player2 = Tank(player2_keys_bind,
               screen.get_width() - 64, screen.get_height() - 64)

tous_les_tanks = pygame.sprite.Group()
tous_les_bullets = pygame.sprite.Group()
tous_les_tanks.add(player1)
tous_les_tanks.add(player2)

def draw(win):
    delta = clock.tick(60)
    keys = key.get_pressed()
    
    for bullet in tous_les_bullets:
        bullet.update_event(delta)
        x, y = (bullet.rect.x, bullet.rect.y)
        w, h = bullet.image.get_size()
        bullet.blit_rotate(screen, bullet.image, (x, y),
                           (w/2, h/2), bullet.angle)
        
    for tank in tous_les_tanks:
        tank.update_event(keys, delta)
        x, y = (tank.rect.x, tank.rect.y)
        w, h = tank.image.get_size()
        tank.blit_rotate(screen, tank.image, (x, y),
                         (w/2, h/2), tank.angle)
    display.update()
    
def invoke_bullet():
    for tank in tous_les_tanks:
        if (tank.invoke_bullet):
            tous_les_bullets.add(
                Bullet(tank.angle, tank.origin.x, tank.origin.y, tank))
            tank.invoke_bullet = False
            
def collision():
    for bullet in tous_les_bullets:
        for tank in tous_les_tanks:
            if bullet.appartenance.id == tank.id:
                continue
            if bullet.rect.colliderect(tank.rect):
                tank.kill()

#* Game loop
while True:
    for e in event.get():
        if e.type == QUIT:  
            pygame.quit()
            sys.exit()
    
    draw(screen)
    invoke_bullet()
    collision()
    
    screen.fill((255, 192, 203))
    tous_les_tanks.update()
    
