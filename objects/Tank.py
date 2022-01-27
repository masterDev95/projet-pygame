from imp import reload
from pygame import *
from pygame.sprite import *

import math

class Tank(Sprite):
    def __init__(self, keys_bind):
        super().__init__()
        self.image = image.load('assets/tank.png').convert()
        self.rect = self.image.get_rect().move(64, 64)
        self.speed = .2
        self.keys = None
        self.delta = .0
        self.keys_bind = keys_bind
        self.angle = .0
        self.rot_speed = .3
        self.invoke_bullet = False
        self.reload_time = 60*2
        self.reload = 0
        self.x = 64.0
        self.y = 64.0
        self.originx = self.rect.centerx
        self.originy = self.rect.bottom
                
    def update_event(self, keys, delta):
        self.keys = keys
        self.delta = delta
        self.update_motion()
        self.update_angle()
        self.update_keyboard()
        self.update_reload()
        
    def update_motion(self):
        key_up = self.keys[self.keys_bind['move_up']]
        key_down = self.keys[self.keys_bind['move_down']]
        
        velocity = (key_down - key_up) * self.speed
        
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * velocity
        horizontal = math.sin(radians) * velocity
        
        self.y -= vertical * self.delta
        self.x -= horizontal * self.delta
        
        self.rect.x = self.x
        self.rect.y = self.y

    def update_angle(self):
        key_left = self.keys[self.keys_bind['move_left']]
        key_right = self.keys[self.keys_bind['move_right']]
        self.angle += (key_left - key_right) * self.rot_speed * self.delta
        self.angle = self.angle % 360
        
    def update_keyboard(self):
        key_fire = self.keys[self.keys_bind['fire']]
        if key_fire and self.reload == 0:
            self.reload = self.reload_time
            self.invoke_bullet = True
            
    def update_reload(self):
        if self.reload > 0:
            self.reload -= 1           
        
    def draw(self, win):
        self.blit_rotate_center(win, self.image, (self.rect.x, self.rect.y), self.angle)
    
    def blit_rotate_center(self, win, image, top_left, angle):
        rotated_image = transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center=image.get_rect(topleft=top_left).center)
        win.blit(rotated_image, new_rect.topleft)
        