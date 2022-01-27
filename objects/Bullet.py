from pygame import *
from pygame.sprite import *

import math

class Bullet(Sprite):
    def __init__(self, angle, x, y):
        super().__init__()
        self.image = image.load('assets/bullet.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.speed = .5
        self.delta = .0
        self.angle = angle
        self.x = float(x)
        self.y = float(y)
        
    def update_event(self, delta):
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
        
    def blit_rotate(self, surf, image, pos, originPos, angle):
        image_rect = image.get_rect(topleft = (pos[0] - originPos[0], pos[1]-originPos[1]))
        offset_center_to_pivot = Vector2(pos) - image_rect.center
        
        rotated_offset = offset_center_to_pivot.rotate(-angle)

        rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)

        rotated_image = transform.rotate(image, angle)
        rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)

        surf.blit(rotated_image, rotated_image_rect)
