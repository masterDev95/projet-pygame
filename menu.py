from pygame import *
from pygame.sprite import *
from pygame.sprite import *
from pygame.time import *
from objects.Bullet import Bullet
from objects.Tank import Tank
from objects.Explosion import Explosion

import sys
import pygame
import pytmx
import pyscroll

# ------------- Gestion Musique

print("On est dans le menu")
musique1 = 'assets/sons/musique_accueil.mp3'
pygame.mixer.init()
pygame.mixer.music.load(musique1)
pygame.mixer.music.set_volume(0.7)
pygame.mixer.music.play()

res = (1280, 720)

# un bouton/image
ls_button_retour =  pygame.image.load("assets/boutons/retour_btn.png")

# Redimmensionner le button
un_image_width = 735
un_image_height = 569
scale = 0.25

ls_button_retour = pygame.transform.scale(ls_button_retour, (int(un_image_width * scale), int(un_image_height * scale)))

# création hitbox
ls_button_retourRect = ls_button_retour.get_rect()

# positionnement
ls_button_retourRect.topleft = (250, 480)

def fonct_menu(display):
    # un bouton/image
    ls_button_un = pygame.image.load("assets/boutons/btn_play.png")
    ls_button_deux =  pygame.image.load("assets/boutons/credits_btn.png")
    ls_button_trois =  pygame.image.load("assets/boutons/quit_btn.png")

    # Redimmensionner le button
    un_image_width = 735
    un_image_height = 569
    scale_gros = 0.3
    scale = 0.2

    ls_button_un = pygame.transform.scale(ls_button_un, (int(un_image_width * scale_gros), int(un_image_height * scale_gros)))
    ls_button_deux = pygame.transform.scale(ls_button_deux, (int(un_image_width * scale), int(un_image_height * scale)))
    ls_button_trois = pygame.transform.scale(ls_button_trois, (int(un_image_width * scale), int(un_image_height * scale)))

    # création hitbox
    ls_button_unRect = ls_button_un.get_rect()
    ls_button_deuxRect = ls_button_deux.get_rect()
    ls_button_troisRect = ls_button_trois.get_rect()

    # positionnement
    ls_button_unRect.topleft = (935, 300)
    ls_button_deuxRect.topleft = (970, 450)
    ls_button_troisRect.topleft = (970, 550)

    # blit
    display.blit(ls_button_un, ls_button_unRect)
    display.blit(ls_button_deux, ls_button_deuxRect)
    display.blit(ls_button_trois, ls_button_troisRect)
    
    fond = pygame.image.load("assets/fond_jeu.png")
    fond = pygame.transform.scale(fond, res)
    fond.set_alpha(128)
    pygame.Surface.convert_alpha(fond)

    # Boucle event
    while 1:
        # print("Entrer dans la boucle event")
        for event in pygame.event.get():
            # print("On attend un event")
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Use event.pos or pg.mouse.get_pos().
                    if ls_button_unRect.collidepoint(event.pos):
                        Game()
                        # jeu()

                    if ls_button_deuxRect.collidepoint(event.pos):
                        EcranCredits(display)
                        display.blit(ls_button_retour, ls_button_retourRect)
                        if ls_button_retourRect.collidepoint(event.pos):
                            print('test')

                    if ls_button_troisRect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
        
        display.blit(fond, (0, 0))
        display.blit(ls_button_un, ls_button_unRect)
        display.blit(ls_button_deux, ls_button_deuxRect)
        display.blit(ls_button_trois, ls_button_troisRect)
        pygame.display.flip()

def EcranCredits(display):
    # blit
    pygame.display.flip()

    credits = pygame.image.load("assets/Menu_Credits.png")
    credits = pygame.transform.scale(credits, res)
    pygame.Surface.convert_alpha(credits)
    
    loop = True
    while loop:
        for e in event.get():
            if e.type == QUIT:  
                pygame.quit()
                sys.exit()
            elif e.type == pygame.MOUSEBUTTONDOWN and display:
                if e.button == 1:
                    if ls_button_retourRect.collidepoint(e.pos):
                        fonct_menu(display)
                        loop = False
                        break
        
        display.blit(credits, (0, 0))
        display.blit(ls_button_retour, ls_button_retourRect)
        pygame.display.flip()
        pygame.display.update()

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = Clock()
        self.init_touches()
        self.win = False
        self.loop = True
        pygame.display.set_caption("Map 1")
        
        #chargement de la carte
        tmx_data = pytmx.util_pygame.load_pygame('assets/maps/map1_TankOne.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, (1280,720))

        #Liste de bloc avec collision
        self.walls = []
        
        for obj in tmx_data.objects:
            if obj.type == 'collision':
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        #Dessiner le groupe de calque
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=1)
        
        self.init_objects()
        self.game_loop()
    
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
        self.player1 = Tank(self.player1_keys_bind, 128, 128, 45)
        self.player2 = Tank(self.player2_keys_bind,
                            self.screen.get_width() - 128,
                            self.screen.get_height() - 128,
                            225)

        #* Initialisation des groupes
        self.tous_les_tanks = pygame.sprite.Group()
        self.tous_les_bullets = pygame.sprite.Group()
        self.toutes_les_explosions = pygame.sprite.Group()
        self.tous_les_tanks.add(self.player1)
        self.tous_les_tanks.add(self.player2)

    #* Méthode de rafraichissement (Screen et objects)
    def update(self):
        # 60 FPS
        delta = self.clock.tick(60)
        
        # Recup des touches appuyées
        keys = key.get_pressed()
        
        self.group.draw(self.screen)
        
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
        
        # Update de l'affichage
        pygame.display.flip()
        
    # Méthode pour instancier les objets nécessaires
    def invoke_instances(self):
        for tank in self.tous_les_tanks:
            if tank.invoke_bullet:
                self.tous_les_bullets.add(
                    Bullet(tank.angle, tank.origin.x, tank.origin.y, tank))
                tank.invoke_bullet = False
                
            if not tank.alive and not tank.has_explode:
                self.toutes_les_explosions.add(Explosion(tank.origin.x, tank.origin.y))
                tank.has_explode = True
                
    def invoke_bouton_retour(self):
        # un bouton/image
        self.ls_button_retour = pygame.image.load("assets/boutons/retour_btn.png")
        self.ls_button_retour = pygame.transform.scale(ls_button_retour, (int(un_image_width * scale), int(un_image_height * scale)))

        # création hitbox
        self.ls_button_retourRect = ls_button_retour.get_rect()

        # positionnement
        self.ls_button_retourRect.topleft = (250, 480)
            
    # Méthode pour gérer les collisions 
    def collision(self):
        for bullet in self.tous_les_bullets:
            for tank in self.tous_les_tanks:
                if bullet.appartenance.id == tank.id:
                    continue
                if bullet.rect.colliderect(tank.rect) and tank.alive:
                    self.invoke_bouton_retour()
                    self.win = True
                    tank.alive = False

    def game_loop(self):
        while self.loop:
            for e in event.get():
                if e.type == QUIT:  
                    pygame.quit()
                    sys.exit()
                elif e.type == pygame.MOUSEBUTTONDOWN and self.win:
                    if e.button == 1:
                        if ls_button_retourRect.collidepoint(e.pos):
                            fonct_menu(self.screen)
                            self.loop = True
                            break
                    
            self.update()
            self.invoke_instances()
            self.collision()
