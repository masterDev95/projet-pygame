from pygame import *
from pygame.sprite import *

class Explosion(Sprite):
    def __init__(self, x, y):
        super().__init__()
        sprites_folder = 'assets/explosion'
        self.sprites = [image.load(f'{sprites_folder}/Explosion_{n}.png') for n in range(1, 7)]
        self.current_sprite = .0
        self.image = self.sprites[int(self.current_sprite)]
        self.rect = self.image.get_rect()
        self.x = float(x)
        self.y = float(y)
        
    def update(self, delta):
        self.current_sprite += 1/6
            
        if self.current_sprite >= len(self.sprites):
            self.kill()
            return
        
        self.image = self.sprites[int(self.current_sprite)]
        
    def blit_rotate(self, surf, image, pos, originPos, angle):
        image_rect = image.get_rect(topleft = (pos[0] - originPos[0], pos[1]-originPos[1]))
        offset_center_to_pivot = Vector2(pos) - image_rect.center
        
        rotated_offset = offset_center_to_pivot.rotate(-angle)

        rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)

        rotated_image = transform.rotozoom(image, angle, .6)
        rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)

        surf.blit(rotated_image, rotated_image_rect)
