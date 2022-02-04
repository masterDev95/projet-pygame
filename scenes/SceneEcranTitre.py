import sys
import pygame
import globals

import scenes.SceneGame
import scenes.SceneCredits
import scenes.SceneControl


class SceneEcranTitre:
    def __init__(self):
        self.dark = (0, 0, 0)

        # Appelle des méthodes d'initialisation
        self.init_screen()
        self.init_boutons()

        # Boucle de jeu
        self.game_loop()

    def init_screen(self):
        # On créer l'écran et on charge les différentes images
        self.screen = pygame.display.set_mode(globals.res, vsync=1)
        self.fond = pygame.image.load("assets/fond_jeu.png")
        self.fond = pygame.transform.scale(self.fond, globals.res)
        self.fond.set_alpha(0)
        pygame.Surface.convert_alpha(self.fond)

        # Effet fade in
        for i in range(0, 255, 5):
            self.fond.set_alpha(i)
            pygame.Surface.convert_alpha(self.fond)
            self.screen.fill(self.dark)
            self.screen.blit(self.fond, (0, 0))
            pygame.display.flip()

    def init_boutons(self):
        # un bouton/image
        self.ls_button_un = pygame.image.load("assets/boutons/btn_play.png")
        self.ls_button_deux = pygame.image.load("assets/boutons/credits_btn.png")
        self.ls_button_trois = pygame.image.load("assets/boutons/quit_btn.png")
        self.ls_button_quatre = pygame.image.load("assets/boutons/unmute.png")
        self.ls_button_cinq = pygame.image.load("assets/boutons/control.png")

        # Redimmensionner les boutons
        un_image_width = 735
        un_image_height = 569
        scale_gros = 0.3
        scale = 0.2
        scale_petit = 0.08

        self.ls_button_un = pygame.transform.scale(self.ls_button_un, (int(un_image_width * scale_gros), int(un_image_height * scale_gros)))
        self.ls_button_deux = pygame.transform.scale(self.ls_button_deux, (int(un_image_width * scale), int(un_image_height * scale)))
        self.ls_button_trois = pygame.transform.scale(self.ls_button_trois, (int(un_image_width * scale), int(un_image_height * scale)))
        self.ls_button_quatre = pygame.transform.scale(self.ls_button_quatre, (int(un_image_width * scale_petit), int(un_image_width * scale_petit)))
        self.ls_button_cinq = pygame.transform.scale(self.ls_button_cinq, (int(un_image_width * scale_petit), int(un_image_width * scale_petit)))


        # création hitbox
        self.ls_button_unRect = self.ls_button_un.get_rect()
        self.ls_button_deuxRect = self.ls_button_deux.get_rect()
        self.ls_button_troisRect = self.ls_button_trois.get_rect()
        self.ls_button_quatreRect = self.ls_button_quatre.get_rect()
        self.ls_button_cinqRect = self.ls_button_cinq.get_rect()

        # positionnement
        self.ls_button_unRect.topleft = (935, 300)
        self.ls_button_deuxRect.topleft = (970, 450)
        self.ls_button_troisRect.topleft = (970, 550)
        self.ls_button_quatreRect.topleft = (1200, 650)
        self.ls_button_cinqRect.topleft = (1120, 649)



    def draw_scene(self):
        self.screen.blit(self.ls_button_un, self.ls_button_unRect)
        self.screen.blit(self.ls_button_deux, self.ls_button_deuxRect)
        self.screen.blit(self.ls_button_trois, self.ls_button_troisRect)
        self.screen.blit(self.ls_button_quatre, self.ls_button_quatreRect)
        self.screen.blit(self.ls_button_cinq, self.ls_button_cinqRect)
        self.screen.blit(self.fond, (0, 0))
        self.screen.blit(self.ls_button_un, self.ls_button_unRect)
        self.screen.blit(self.ls_button_deux, self.ls_button_deuxRect)
        self.screen.blit(self.ls_button_trois, self.ls_button_troisRect)
        self.screen.blit(self.ls_button_quatre, self.ls_button_quatreRect)
        self.screen.blit(self.ls_button_cinq, self.ls_button_cinqRect)
        pygame.display.flip()

    def game_loop(self):
        musicplaying = True
        showcontrol = True
        # Boucle event
        while True:
            for event in pygame.event.get():
                # Quitte le jeu
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.ls_button_unRect.collidepoint(event.pos):
                            globals.scene = scenes.SceneGame.SceneGame()
                        if self.ls_button_deuxRect.collidepoint(event.pos):
                            globals.scene = scenes.SceneCredits.SceneCredits()
                        if self.ls_button_troisRect.collidepoint(event.pos):
                            pygame.quit()
                            sys.exit()
                        if self.ls_button_quatreRect.collidepoint(event.pos) and musicplaying:
                            pygame.mixer.music.pause()
                            musicplaying = False
                            self.ls_button_quatre = pygame.image.load("assets/boutons/mute.png")
                            self.ls_button_quatre = pygame.transform.scale(self.ls_button_quatre, (int(735 * 0.08), int(735 * 0.08)))
                        else:
                            pygame.mixer.music.unpause()
                            musicplaying = True
                            self.ls_button_quatre = pygame.image.load("assets/boutons/unmute.png")
                            self.ls_button_quatre = pygame.transform.scale(self.ls_button_quatre, (int(735 * 0.08), int(735 * 0.08)))
                        if self.ls_button_cinqRect.collidepoint(event.pos):
                            globals.scene = scenes.SceneControl.SceneControl()

            self.draw_scene()