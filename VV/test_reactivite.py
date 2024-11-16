# test_reactivite.py

import pygame
import sys
import menu  # Réimportation pour revenir au menu

# Fonction principale du test de réactivité
def run():
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Test de Réactivité")

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    font = pygame.font.Font(None, 40)

    text = font.render("Test de Réactivité - Appuyez sur Entrée pour revenir", True, BLACK)
    screen.fill(WHITE)
    screen.blit(text, (50, HEIGHT // 2))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False  # Sortir de la boucle pour revenir au menu
    menu.main_menu()  # Revenir au menu
