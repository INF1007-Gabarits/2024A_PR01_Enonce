import pygame
import random
import sys
import helper
from game import Game
from config import *
from home import Home

# Initialiser Pygame
pygame.init()

# Définir les dimensions de la fenêtre du jeu
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pac-Man")

background_color = (0, 0, 0)  # Couleur de fond noire

# Initialiser la variable du score
wins = 0  # Vous pouvez remplacer par la lecture d'un fichier ou d'une base de données

game = Game(screen)
home = Home(screen)

# Boucle principale du jeu
running = True
game_started = False  

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if home.is_button_clicked(event.pos) and not game_started:
                game_started = True
        elif event.type == pygame.KEYDOWN and game_started:
            game.handle_keypress(event)

    # Mettre à jour les éléments du jeu
    screen.fill(background_color)

    if not game_started:
        # Afficher l'image de fond
        home.render(wins)
    else:
        game.render()
        game.update() 

    if game.game_over:
        if game.game_won:
            wins += 1
            
        game_started = False
        game = Game(screen)

    # Rafraîchir l'affichage
    pygame.display.flip()
    pygame.time.wait(100)  # Réduit la vitesse pour mieux voir les déplacements

pygame.quit()
sys.exit()
