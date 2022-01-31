import sys
import pygame
import globals
import scenes.SceneEcranTitre


class SceneCredits:
    def __init__(self):
        self.screen = pygame.display.set_mode(globals.res)
        self.credits = pygame.image.load("assets/Menu_Credits.png")
        self.credits = pygame.transform.scale(self.credits, globals.res)
        pygame.Surface.convert_alpha(self.credits)
        
        self.init_bouton_retour()
        self.game_loop()
        
    def init_bouton_retour(self):
        # Redimmensionner le button
        un_image_width = 735
        un_image_height = 569
        scale = 0.25
        
        # un bouton/image
        self.ls_button_retour = pygame.image.load("assets/boutons/retour_btn.png")
        self.ls_button_retour = pygame.transform.scale(
            self.ls_button_retour, (int(un_image_width * scale), int(un_image_height * scale)))

        # création hitbox
        self.ls_button_retourRect = self.ls_button_retour.get_rect()

        # positionnement
        self.ls_button_retourRect.topleft = (250, 480)
    
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
        self.screen.blit(self.credits, (0, 0))
        self.screen.blit(self.ls_button_retour, self.ls_button_retourRect)
        pygame.display.flip()
        pygame.display.update()
        