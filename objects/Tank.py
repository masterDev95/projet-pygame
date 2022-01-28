from pygame import *
from pygame.sprite import *

import math

class Tank(Sprite):
    last_id = 0
    
    def __init__(self, keys_bind, x, y):
        super().__init__()
        self.image = image.load('assets/tank.png').convert_alpha()
        self.rect = self.image.get_rect().move(x, y)
        self.speed = .2
        self.keys = None
        self.delta = .0
        self.keys_bind = keys_bind
        self.angle = .0
        self.rot_speed = .3
        self.invoke_bullet = False
        self.reload_time = 60*2
        self.reload = 0
        self.x = float(x)
        self.y = float(y)
        self.origin = Vector2()
        self.id = Tank.last_id
        self.alive = True
        self.has_explode = False
        Tank.last_id += 1
                
    def update_event(self, keys, delta):
        self.keys = keys
        self.delta = delta
        self.update_motion()
        self.update_angle()
        self.update_keyboard()
        self.update_reload()
        if not self.alive and not self.has_explode:
            self.image = image.load('assets/tank_destroyed.png').convert_alpha()
        
    def update_motion(self):
        key_up = self.keys[self.keys_bind['move_up']]
        key_down = self.keys[self.keys_bind['move_down']]
        
        velocity = (key_down - key_up) * self.speed
        
        self.radians = math.radians(self.angle)
        vertical = math.cos(self.radians) * velocity
        horizontal = math.sin(self.radians) * velocity
        
        self.y -= vertical * self.delta
        self.x -= horizontal * self.delta
            
        self.rect.x = self.x
        self.rect.y = self.y
        
        self.origin = Vector2(self.x, self.y)

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
            
    def blit_rotate(self, surf, image, pos, originPos, angle):
        image_rect = image.get_rect(topleft = (pos[0] - originPos[0], pos[1]-originPos[1]))
        offset_center_to_pivot = Vector2(pos) - image_rect.center
        
        rotated_offset = offset_center_to_pivot.rotate(-angle)

        rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)

        rotated_image = transform.rotate(image, angle)
        rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)

        surf.blit(rotated_image, rotated_image_rect)
        draw.rect(surf, (255, 0, 0), (*rotated_image_rect.topleft, *rotated_image.get_size()),2)
        