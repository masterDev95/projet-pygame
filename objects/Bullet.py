from pygame import *
from pygame.sprite import *

import math

class Bullet(Sprite):
    def __init__(self, angle, x, y):
        super().__init__()
        self.image = image.load('assets/bullet.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.speed = .1
        self.delta = .0
        self.angle = angle
        self.x = float(x)
        self.y = float(y)
        
    def update_event(self, keys, delta):
        self.keys = keys
        self.delta = delta
        self.update_motion()
        
    def update_motion(self):
        velocity = (self.speed * self.delta)

        radians = math.radians(self.angle)
        vertical = math.cos(radians) * velocity
        horizontal = math.sin(radians) * velocity

        self.x += horizontal
        self.y += vertical
        
        self.rect.x = self.x
        self.rect.y = self.y
    
    def update_angle(self):
        key_left = self.keys[self.keys_bind['move_left']]
        key_right = self.keys[self.keys_bind['move_right']]
        self.angle += (key_left - key_right) * self.rot_speed * self.delta
        self.angle = self.angle % 360
        print(self.angle)
        
    def draw(self, win):
        self.blit_rotate_center(win, self.image, (self.rect.x, self.rect.y), self.angle)
    
    def blit_rotate_center(self, win, image, top_left, angle):
        rotated_image = transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center=image.get_rect(topleft=top_left).center)
        win.blit(rotated_image, new_rect.topleft)
