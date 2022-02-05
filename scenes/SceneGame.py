import sys
import pygame
import pytmx
import pyscroll
import globals

from pygame import *
from pygame.time import *
from objects.Bullet import Bullet
from objects.Explosion import Explosion

from objects.Tank import Tank
import scenes.SceneEcranTitre


class SceneGame:
    def __init__(self, scr=0, scb=0):
        # Membres
        self.screen = pygame.display.set_mode(globals.res)
        self.clock = Clock()
        self.win = False
        self.loop = True
        self.score_value_r = scr
        self.score_value_b = scb
        self.font = pygame.font.Font('Headlines-Medium.otf', 32)
        self.fire_sound = pygame.mixer.Sound('assets/sons/fire.wav')
        self.explosion_sound = pygame.mixer.Sound('assets/sons/explosion.wav')
        
        pygame.display.set_caption("Map 1")
        pygame.mixer.Sound.set_volume(self.fire_sound, 0.1)
        pygame.mixer.Sound.set_volume(self.explosion_sound, 0.1)
        
        # Appelle des méthodes d'initialisation
        self.map_load()
        self.init_touches()
        self.init_objects()
        
        # Boucle de jeu
        self.game_loop()
        
    #* Chargement de la carte
    def map_load(self):
        tmx_data = pytmx.util_pygame.load_pygame('assets/maps/map1_TankOne.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, globals.res)
        
        # Liste de bloc avec collision
        self.walls = []
        
        for obj in tmx_data.objects:
            if obj.type == 'collision':
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
                
        # Dessiner le groupe de calque
        self.level_group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=1)
    
    #* Dico touches des joueurs
    def init_touches(self):
        self.player1_keys_bind = {
            'move_left': K_LEFT,
            'move_right': K_RIGHT,
            'move_up': K_UP,
            'move_down': K_DOWN,
            'fire': K_SPACE
        }

        self.player2_keys_bind = {
            'move_left': K_q,
            'move_right': K_d,
            'move_up': K_z,
            'move_down': K_s,
            'fire': K_TAB
        }

    def init_objects(self):
        #* Initialisation des joueurs
        self.player1 = Tank(self.player1_keys_bind, 'red', 128, 128, 90)
        self.player2 = Tank(self.player2_keys_bind, 'blue',
                            self.screen.get_width() - 128,
                            self.screen.get_height() - 128,
                            270)

        #* Initialisation des groupes
        self.tous_les_tanks = pygame.sprite.Group()
        self.tous_les_bullets = pygame.sprite.Group()
        self.toutes_les_explosions = pygame.sprite.Group()
        self.tous_les_tanks.add(self.player1)
        self.tous_les_tanks.add(self.player2)

    def game_loop(self):
        while self.loop:
            for e in event.get():
                if e.type == QUIT:  
                    pygame.quit()
                    sys.exit()
                if e.type == pygame.MOUSEBUTTONDOWN and self.win:
                    if e.button == 1 and self.ls_button_retourRect != None:
                        if self.ls_button_retourRect.collidepoint(e.pos):
                            globals.scene = scenes.SceneEcranTitre.SceneEcranTitre()
                        if self.ls_button_rejouerRect.collidepoint(e.pos):
                            for tank in self.tous_les_tanks:
                                tank.kill()
                            self.__init__(self.score_value_r, self.score_value_b)
                            
            self.update()
            self.invoke_instances()
            self.collision()
            
    #* Méthode de rafraichissement (Screen et objects)
    def update(self):
        # 60 FPS
        delta = self.clock.tick(60)
        
        # Recup des touches appuyées
        keys = key.get_pressed()
        
        self.level_group.draw(self.screen)
        
        # Update des bullets
        for bullet in self.tous_les_bullets:
            bullet.update_event(delta)
            x, y = (bullet.rect.x, bullet.rect.y)
            w, h = bullet.image.get_size()
            bullet.blit_rotate(self.screen, bullet.image, (x, y),
                               (w/2, h/2), bullet.angle)
        
        # Update des tanks
        for tank in self.tous_les_tanks:
            tank.update_event(keys, delta)
            x, y = (tank.rect.x, tank.rect.y)
            w, h = tank.image.get_size()
            tank.blit_rotate(self.screen, tank.image, (x, y),
                             (w/2, h/2), tank.angle)
        
        # Update des explosions
        for explosion in self.toutes_les_explosions:
            explosion.update(delta)
            x, y = (explosion.x, explosion.y)
            w, h = explosion.image.get_size()
            explosion.blit_rotate(self.screen, explosion.image,
                                  (x, y), (w/2, h/2), 0)
        
        if self.win:
            self.screen.blit(self.ls_button_retour, self.ls_button_retourRect)
            self.screen.blit(self.ls_button_rejouer, self.ls_button_rejouerRect)
        
        self.show_score_red()
        self.show_score_blue()
        
        # Update de l'affichage
        pygame.display.flip()
        
    #* Méthode pour instancier les objets nécessaires
    def invoke_instances(self):
        for tank in self.tous_les_tanks:
            if tank.invoke_bullet:
                self.fire_sound.play()
                self.tous_les_bullets.add(
                    Bullet(tank.angle, tank.origin.x, tank.origin.y, tank))
                tank.invoke_bullet = False
                
            if not tank.alive and not tank.has_explode:
                self.toutes_les_explosions.add(Explosion(tank.origin.x, tank.origin.y))
                tank.has_explode = True
                
    #* Méthode pour gérer les collisions 
    def collision(self):
        for bullet in self.tous_les_bullets:
            for tank in self.tous_les_tanks:
                if bullet.appartenance.id == tank.id:
                    continue
                if bullet.rect.colliderect(tank.rect) and tank.alive:
                    self.explosion_sound.play()
                    self.invoke_boutons()
                    self.win = True
                    tank.alive = False
                    if tank.team == 'red':
                        self.score_value_r += 1
                    else:
                        self.score_value_b += 1
            for wall in self.walls:
                if wall.colliderect(bullet) and bullet.can_collide:
                    bullet.kill()
                                    
        for tank in self.tous_les_tanks:
            tank.collision_box = {
                'left': False,
                'right': False,
                'top': False,
                'bottom': False
            }
            for wall in self.walls:
                if tank.rect.colliderect(wall):
                    if abs(wall.left - tank.rect.right) < 10:
                        tank.collision_box['right'] = True
                    if abs(wall.right - tank.rect.left) < 10:
                        tank.collision_box['left'] = True
                    if abs(wall.top - tank.rect.bottom) < 10:
                        tank.collision_box['bottom'] = True
                    if abs(wall.bottom - tank.rect.top) < 10:
                        tank.collision_box['top'] = True
                    
    def invoke_boutons(self):
        # Redimmensionner le button
        un_image_width = 735
        un_image_height = 569
        scale = 0.25
        
        # un bouton/image
        self.ls_button_retour = pygame.image.load("assets/boutons/retour_btn.png")
        self.ls_button_retour = pygame.transform.scale(
            self.ls_button_retour, (int(un_image_width * scale), int(un_image_height * scale)))
        
        self.ls_button_rejouer = pygame.image.load("assets/boutons/btn_rejouer.png")
        self.ls_button_rejouer = pygame.transform.scale(
            self.ls_button_rejouer, (int(un_image_width * scale), int(un_image_height * scale)))

        # création hitbox
        self.ls_button_retourRect = self.ls_button_retour.get_rect()
        self.ls_button_rejouerRect = self.ls_button_rejouer.get_rect()

        # positionnement
        self.ls_button_retourRect.topleft = (250, 480)
        self.ls_button_rejouerRect.topleft = (530, 480)

    def show_score_red(self):
        score_value_red = self.font.render("Score Rouge : " + str(self.score_value_b), True, (255, 0, 0))
        bg = Surface(score_value_red.get_size())
        bg.set_alpha(140)
        self.screen.blit(bg, (10, 10))
        self.screen.blit(score_value_red, (10, 10))

    def show_score_blue(self):
        score_value_blue = self.font.render("Score Bleu : " + str(self.score_value_r), True, (0, 0, 255))
        bg = Surface(score_value_blue.get_size())
        bg.set_alpha(140)
        self.screen.blit(bg, (self.screen.get_width() - score_value_blue.get_width() - 10, 10))
        self.screen.blit(score_value_blue, (self.screen.get_width() - score_value_blue.get_width() - 10, 10))
        