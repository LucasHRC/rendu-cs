import pygame
import time
import random
import csv

# Import des mini-jeux
import minijeu1
import minijeu2
import minijeu3

def main():
    # Initialiser Pygame
    pygame.init()

    # Lancer le premier mini-jeu (Test de Réaction)
    minijeu1.introduction()  # Affiche l'introduction
    minijeu1.reaction_test()  # Lance le mini-jeu

    # Lancer le deuxième mini-jeu (Test de Rythme)
    minijeu2.introduction()  # Affiche l'introduction
    minijeu2.rhythm_test()  # Lance le mini-jeu

    # Lancer le troisième mini-jeu (Test de Rapidité d'Écriture)
    minijeu3.typing_test()  # Lance le mini-jeu

    # Quitter Pygame proprement à la fin de l'enchaînement
    pygame.quit()

if __name__ == "__main__":
    main()
import pygame
import time
import random
import csv

# Import des mini-jeux
import minijeu1
import minijeu2
import minijeu3

def main():
    # Initialiser Pygame
    pygame.init()

    # Création de l'écran
    screen = pygame.display.set_mode((800, 600))  # Vous pouvez ajuster la taille selon vos besoins
    pygame.display.set_caption("Mini-jeux en chaîne")

    # Couleur de fond
    WHITE = (255, 255, 255)

    # Lancer le premier mini-jeu (Test de Réaction)
    minijeu1.introduction(screen)  # Affiche l'introduction
    minijeu1.reaction_test(screen)  # Lance le mini-jeu

    # Réinitialiser l'écran avant de commencer le deuxième mini-jeu
    screen.fill(WHITE)
    pygame.display.update()

    # Lancer le deuxième mini-jeu (Test de Rythme)
    minijeu2.introduction(screen)  # Affiche l'introduction
    minijeu2.rhythm_test(screen)  # Lance le mini-jeu

    # Réinitialiser l'écran avant de commencer le troisième mini-jeu
    screen.fill(WHITE)
    pygame.display.update()

    # Lancer le troisième mini-jeu (Test de Rapidité d'Écriture)
    minijeu3.typing_test(screen)  # Lance le mini-jeu

    # Quitter Pygame proprement à la fin de l'enchaînement
    pygame.quit()

if __name__ == "__main__":
    main()
