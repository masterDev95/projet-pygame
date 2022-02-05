from pygame import *
import pygame
from pygame.sprite import *

import math

class Tank(Sprite):
    # id statique qui s'incrémente à chaque nouvel objet
    last_id = 0
    
    def __init__(self, keys_bind, team, x, y, angle=0):
        super().__init__()
        self.image = image.load('assets/tank.png').convert_alpha()
        self.rect = self.image.get_rect().move(x, y)
        self.speed = .1
        self.keys = None
        self.delta = .0
        self.keys_bind = keys_bind
        self.angle = float(angle)
        self.rot_speed = .15
        self.invoke_bullet = False
        self.reload_time = 60*2
        self.reload = 0
        self.x = float(x)
        self.y = float(y)
        self.origin = Vector2()
        self.id = Tank.last_id
        self.alive = True
        self.has_explode = False
        self.can_move = True
        self.mask = pygame.mask.from_surface(self.image)
        self.team = team
        
        self.collision_box = {
            'left': False,
            'right': False,
            'top': False,
            'bottom': False
        }
        
        if self.team == 'red':
            self.image.fill((255, 0, 0), None, pygame.BLEND_MULT)
        else:
            self.image.fill((0, 0, 255), None, pygame.BLEND_ADD)
            
        Tank.last_id += 1
                
    def update_event(self, keys, delta):
        self.keys = keys
        self.delta = delta
        
        if self.alive:
            self.update_keyboard()
            self.update_reload()
        self.update_motion()
        
        # Update du masque
        self.mask = pygame.mask.from_surface(self.image)

        # Si le char est détruit, on remplace l'image par le char détruit
        if not self.alive and not self.has_explode:
            self.image = image.load('assets/tank_destroyed.png').convert_alpha()
        
    # Update des mouvements
    def update_motion(self):
        key_up = self.keys[self.keys_bind['move_up']]
        key_down = self.keys[self.keys_bind['move_down']]
        
        go_up = key_up * (not self.collision_box['top'])
        go_down = key_down * (not self.collision_box['bottom'])
        go_left = self.keys[self.keys_bind['move_left']] * (not self.collision_box['left'])
        go_right = self.keys[self.keys_bind['move_right']] * (not self.collision_box['right'])
    
        vertical = go_up - go_down 
        horizontal = (go_left - go_right) * (not key_up and not key_down)
        
        if vertical < 0:
            self.angle = 0
        if vertical > 0:
            self.angle = 180
        if horizontal < 0:
            self.angle = 90
        if horizontal > 0:
            self.angle = 270
        
        # Coord en float
        self.y -= vertical * self.delta * self.speed * self.alive
        self.x -= horizontal * self.delta * self.speed * self.alive
            
        # Coord du rect
        self.rect.x = self.x
        self.rect.y = self.y
        
        # Coord de l'origine du sprite
        self.origin = Vector2(self.x, self.y)
        
    # Update des inputs
    def update_keyboard(self):
        key_fire = self.keys[self.keys_bind['fire']]
        if key_fire and self.reload == 0:
            self.reload = self.reload_time
            self.invoke_bullet = True
            
    # Rechargement des balles
    def update_reload(self):
        if self.reload > 0:
            self.reload -= 1
            
    # Méthode de dessin du sprite avec gestion de l'orientation
    def blit_rotate(self, surf, image, pos, originPos, angle):
        image_rect = image.get_rect(topleft = (pos[0] - originPos[0], pos[1]-originPos[1]))
        offset_center_to_pivot = Vector2(pos) - image_rect.center
        rotated_offset = offset_center_to_pivot.rotate(-angle)
        rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)
        rotated_image = transform.rotate(image, angle)
        rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)
        self.rect = rotated_image_rect
        surf.blit(rotated_image, rotated_image_rect)
        