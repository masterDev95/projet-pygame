import sys
import pygame
import globals
import scenes.SceneEcranTitre
class SceneControl:
    def __init__(self):
        self.screen = pygame.display.set_mode(globals.controlres)
        self.control = pygame.image.load("assets/controlfull.png")
        self.control = pygame.transform.scale(self.control, globals.controlres)
        pygame.Surface.convert_alpha(self.control)

        self.init_bouton_retour()
        self.game_loop()

    def init_bouton_retour(self):
        # Redimmensionner le button
        un_image_width = 735
        un_image_height = 569
        scale = 0.2

        # un bouton/image
        self.ls_button_retour = pygame.image.load("assets/boutons/retour_btn.png")
        self.ls_button_retour = pygame.transform.scale(
            self.ls_button_retour, (int(un_image_width * scale), int(un_image_height * scale)))

        # création hitbox
        self.ls_button_retourRect = self.ls_button_retour.get_rect()

        # positionnement
        self.ls_button_retourRect.topleft = (950, 10)

    def game_loop(self):
        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif e.type == pygame.MOUSEBUTTONDOWN and self.screen:
                    if e.button == 1:
                        if self.ls_button_retourRect.collidepoint(e.pos):
                            globals.scene = scenes.SceneEcranTitre.SceneEcranTitre()
            self.draw()

    def draw(self):
        self.screen.blit(self.control, (0, 0))
        self.screen.blit(self.ls_button_retour, self.ls_button_retourRect)
        pygame.display.flip()
        pygame.display.update()