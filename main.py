import pygame
import globals

#* Initialisation jeu
pygame.init()
pygame.mixer.init()

# Musique d'intro
generique = 'assets/sons/musique_accueil.mp3'
pygame.mixer.music.load(generique)
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play()

# On part dans le Menu
globals.scene()
