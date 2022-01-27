from pygame import *
from pygame.sprite import *

import math

class Tank(Sprite):
    def __init__(self, keys_bind):
        super().__init__()
        self.image = image.load('assets/tank.png').convert_alpha()
        self.rect = self.image.get_rect().move(64, 64)
        self.speed = .2
        self.keys = None
        self.delta = .0
        self.keys_bind = keys_bind
        self.angle = 0
        self.rot_speed = .3
        
    def update_event(self, keys, delta, screen):
        self.keys = keys
        self.delta = delta
        self.update_motion()
        self.update_angle()
        
    def update_motion(self):
        key_up = self.keys[self.keys_bind['move_up']]
        key_down = self.keys[self.keys_bind['move_down']]
        
        velocity = (key_down - key_up) * self.speed * self.delta
        
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * velocity
        horizontal = math.sin(radians) * velocity
        
        self.rect.x += horizontal
        self.rect.y += vertical

    def update_angle(self):
        key_left = self.keys[self.keys_bind['move_left']]
        key_right = self.keys[self.keys_bind['move_right']]
        self.angle += (key_left - key_right) * self.rot_speed * self.delta % 360
        self.angle = self.angle % 360
        print(self.angle)
        
    def draw(self, win):
        self.blit_rotate_center(win, self.image, (self.rect.x, self.rect.y), self.angle)
    
    def blit_rotate_center(self, win, image, top_left, angle):
        rotated_image = transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center=image.get_rect(topleft=top_left).center)
        win.blit(rotated_image, new_rect.topleft)
        