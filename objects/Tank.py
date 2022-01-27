from pygame import *
from pygame.sprite import *

class Tank(Sprite):
    def __init__(self, keys_bind):
        super().__init__()
        self.image = image.load('assets/tank.png').convert()
        self.rect = self.image.get_rect().move(64, 64)
        self.speed = .2
        self.keys = None
        self.delta = .0
        self.keys_bind = keys_bind
        
    def update_event(self, keys, delta):
        self.keys = keys
        self.delta = delta
        self.update_motion()
        
    def update_motion(self):
        key_left = self.keys[self.keys_bind['move_left']]
        key_right = self.keys[self.keys_bind['move_right']]
        key_up = self.keys[self.keys_bind['move_up']]
        key_down = self.keys[self.keys_bind['move_down']]
        
        self.rect.x += (key_right - key_left) * self.speed * self.delta
        self.rect.y += (key_down - key_up) * self.speed * self.delta
