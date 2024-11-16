import pygame
import sys
import importlib
import game  # Import de game.py
import minijeu1
import minijeu2
import minijeu3
import csv
import os
import subprocess
from datetime import datetime

# Initialisation de Pygame
pygame.init()

# Configuration initiale
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Mini-Jeux")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (220, 220, 220)
DARK_GRAY = (50, 50, 50)
RED = (255, 0, 0)

# Polices de texte
FONT_TITLE = pygame.font.Font(pygame.font.get_default_font(), 48)
FONT_SUBTITLE = pygame.font.Font(pygame.font.get_default_font(), 30)
FONT_BODY = pygame.font.Font(pygame.font.get_default_font(), 24)
FONT_SMALL = pygame.font.Font(pygame.font.get_default_font(), 18)

# Liste des options du menu
menu_items = ["Démarrer le Test", "Leaderboard", "Quitter"]

# Variable de sélection
selected_item = -1  # Pas de sélection par défaut

# Fonction pour dessiner du texte centré
def draw_text(text, font, color, x, y):
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(x, y))
    screen.blit(surface, rect)

# Fonction pour dessiner une boîte autour d'un texte
def draw_box(text, font, color, x, y, width, height, background_color=LIGHT_GRAY, border_color=BLACK):
    pygame.draw.rect(screen, background_color, (x - width // 2, y - height // 2, width, height))
    pygame.draw.rect(screen, border_color, (x - width // 2, y - height // 2, width, height), 2)
    draw_text(text, font, color, x, y)

# Fonction pour dessiner le menu
def draw_menu():
    screen.fill(WHITE)  # Fond blanc

    # Titre principal
    draw_text("Mini-Jeux", FONT_TITLE, BLACK, WIDTH // 2, HEIGHT // 4)

    # Sous-titre
    draw_text("Choisissez une option", FONT_SUBTITLE, DARK_GRAY, WIDTH // 2, HEIGHT // 4 + 60)

    # Dessin des options du menu dans des boîtes
    global selected_item
    for index, item in enumerate(menu_items):
        color = BLACK if index != selected_item else WHITE
        box_color = LIGHT_GRAY if index != selected_item else DARK_GRAY
        box_width = 400
        box_height = 50
        y_position = HEIGHT // 2 + index * (box_height + 10)

        if index == len(menu_items) - 1:  # "Quitter"
            box_color = RED  # La boîte "Quitter" sera rouge
            color = WHITE  # Texte en blanc

        # Dessiner la boîte avec texte
        draw_box(item, FONT_BODY, color, WIDTH // 2, y_position, box_width, box_height, background_color=box_color)

    # Texte "ÉCHAP pour quitter"
    draw_text("ÉCHAP pour quitter", FONT_SMALL, DARK_GRAY, WIDTH // 2, HEIGHT - 50)

    pygame.display.flip()

# Fonction pour gérer l'input de la souris
def handle_mouse_input():
    global selected_item
    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    for index, item in enumerate(menu_items):
        item_rect = pygame.Rect(0, HEIGHT // 2 + index * (50 + 10) - 25, WIDTH, 50)
        if item_rect.collidepoint(mouse_x, mouse_y):
            selected_item = index
            break

# Nom du fichier CSV
CSV_FILE = "score.csv"

def collect_user_data():
    """
    Affiche une interface Pygame simple pour collecter les informations utilisateur.
    Champs centrés avec disposition verticale (pseudo, âge, sexe, main dominante).
    Les données sont stockées dans la variable userdata et ne sont pas encore écrites dans un fichier.
    """
    # Initialisation des données utilisateur
    user_data = {"pseudo": "", "age": "", "sexe": None, "main_dominante": None}
    fields = ["pseudo", "age"]  # Liste pour la navigation avec Tab
    active_field_index = 0  # Index du champ actif
    active_field = fields[active_field_index]  # Champ initial actif
    message = ""  # Message d'erreur ou de validation

    # Styles et dimensions
    label_font = pygame.font.Font(None, 20)
    input_font = pygame.font.Font(None, 24)
    button_font = pygame.font.Font(None, 20)
    title_font = pygame.font.Font(None, 36)

    input_box_width, input_box_height = 200, 35
    button_width, button_height = 120, 35
    button_color = (192, 192, 192)
    button_active_color = (135, 206, 250)
    button_text_color = BLACK

    sexes = ["Homme", "Femme"]
    mains = ["Droitier", "Gaucher"]

    # Boucle principale
    running = True
    while running:
        screen.fill(WHITE)

        # Titre principal
        draw_text("Bienvenue !", title_font, BLACK, WIDTH // 2, HEIGHT // 10)
        draw_text("Veuillez entrer vos informations", label_font, DARK_GRAY, WIDTH // 2, HEIGHT // 10 + 40)

        # Champs de texte pour Pseudo et Âge
        y_offset = HEIGHT // 4
        draw_text("Entrez votre pseudo :", label_font, BLACK, WIDTH // 4, y_offset - 20)
        pygame.draw.rect(screen, DARK_GRAY if active_field == "pseudo" else LIGHT_GRAY, 
                         (WIDTH // 4 - input_box_width // 2, y_offset, input_box_width, input_box_height), 
                         border_radius=5)
        pseudo_text = input_font.render(user_data["pseudo"], True, BLACK)
        screen.blit(pseudo_text, (WIDTH // 4 - input_box_width // 2 + 10, y_offset + 5))

        draw_text("Entrez votre âge :", label_font, BLACK, WIDTH * 3 // 4, y_offset - 20)
        pygame.draw.rect(screen, DARK_GRAY if active_field == "age" else LIGHT_GRAY, 
                         (WIDTH * 3 // 4 - input_box_width // 2, y_offset, input_box_width, input_box_height), 
                         border_radius=5)
        age_text = input_font.render(user_data["age"], True, BLACK)
        screen.blit(age_text, (WIDTH * 3 // 4 - input_box_width // 2 + 10, y_offset + 5))

        # Boutons pour Sexe (Homme/Femme)
        y_offset += 100
        draw_text("Sexe :", label_font, BLACK, WIDTH // 2, y_offset - 30)
        for i, sexe in enumerate(sexes):
            button_rect = pygame.Rect(WIDTH // 2 - (len(sexes) * button_width) // 2 + i * (button_width + 20), y_offset, button_width, button_height)
            pygame.draw.rect(screen, button_active_color if user_data["sexe"] == sexe else button_color,
                             button_rect, border_radius=5)
            text_surface = button_font.render(sexe, True, button_text_color)
            screen.blit(text_surface, text_surface.get_rect(center=button_rect.center))

        # Boutons pour Main Dominante (Droitier/Gaucher)
        y_offset += 100
        draw_text("Main dominante :", label_font, BLACK, WIDTH // 2, y_offset - 30)
        for i, main in enumerate(mains):
            button_rect = pygame.Rect(WIDTH // 2 - (len(mains) * button_width) // 2 + i * (button_width + 20), y_offset, button_width, button_height)
            pygame.draw.rect(screen, button_active_color if user_data["main_dominante"] == main else button_color,
                             button_rect, border_radius=5)
            text_surface = button_font.render(main, True, button_text_color)
            screen.blit(text_surface, text_surface.get_rect(center=button_rect.center))

        # Bouton Valider
        y_offset += 100
        button_rect = pygame.Rect(WIDTH // 2 - 100, y_offset, 200, 50)
        pygame.draw.rect(screen, button_active_color if button_rect.collidepoint(pygame.mouse.get_pos()) else button_color,
                         button_rect, border_radius=5)
        draw_text("Commencer", input_font, WHITE, button_rect.centerx, button_rect.centery)

        # Affichage du message d'erreur ou validation
        if message:
            draw_text(message, label_font, RED, WIDTH // 2, y_offset + 70)

        pygame.display.flip()

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Navigation et saisie au clavier
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:  # Navigation entre champs
                    active_field_index = (active_field_index + 1) % len(fields)
                    active_field = fields[active_field_index]
                elif event.key == pygame.K_BACKSPACE and active_field in fields:
                    user_data[active_field] = user_data[active_field][:-1]
                elif active_field in ["pseudo", "age"] and event.unicode.isprintable():
                    user_data[active_field] += event.unicode

            # Interactions avec la souris
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Bouton Valider
                if button_rect.collidepoint(event.pos):
                    if not user_data["pseudo"] or not user_data["age"] or not user_data["sexe"] or not user_data["main_dominante"]:
                        message = "Veuillez remplir tous les champs."
                    elif not user_data["age"].isdigit():
                        message = "L'âge doit être un nombre."
                    else:
                        # Si le pseudo est "leonard", déclencher l'easter egg
                        if user_data["pseudo"].lower() == "leonard":
                            run_leonard_easteregg()
                            return None  # Sortir immédiatement pour éviter la suite de la collecte

                        return user_data  # Renvoie simplement le dictionnaire de données collectées

                # Boutons Sexe
                for i, sexe in enumerate(sexes):
                    button_rect = pygame.Rect(WIDTH // 2 - (len(sexes) * button_width) // 2 + i * (button_width + 20), HEIGHT // 4 + 100, button_width, button_height)
                    if button_rect.collidepoint(event.pos):
                        user_data["sexe"] = sexe

                # Boutons Main Dominante
                for i, main in enumerate(mains):
                    button_rect = pygame.Rect(WIDTH // 2 - (len(mains) * button_width) // 2 + i * (button_width + 20), HEIGHT // 4 + 200, button_width, button_height)
                    if button_rect.collidepoint(event.pos):
                        user_data["main_dominante"] = main

                # Champs de texte (Pseudo ou Âge)
                if pygame.Rect(WIDTH // 4 - input_box_width // 2, HEIGHT // 4, input_box_width, input_box_height).collidepoint(event.pos):
                    active_field = "pseudo"
                elif pygame.Rect(WIDTH * 3 // 4 - input_box_width // 2, HEIGHT // 4, input_box_width, input_box_height).collidepoint(event.pos):
                    active_field = "age"

def run_leonard_easteregg():
    """
    Affiche un message spécial et demande de choisir entre Doodle ou La Quête.
    Lance ensuite le jeu correspondant selon le choix de l'utilisateur.
    """
    screen.fill(WHITE)
    draw_text("Bonjour Léo !", FONT_TITLE, BLACK, WIDTH // 2, HEIGHT // 3)
    draw_text("Que veux-tu faire ?", FONT_BODY, BLACK, WIDTH // 2, HEIGHT // 2)

    # Afficher les options
    draw_text("1. Doodle", FONT_BODY, BLACK, WIDTH // 2, HEIGHT // 2 + 50)
    draw_text("2. La Quête", FONT_BODY, BLACK, WIDTH // 2, HEIGHT // 2 + 100)

    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    subprocess.run(['python', 'Doodle.py'])
                    waiting_for_input = False
                elif event.key == pygame.K_2:
                    subprocess.run(['python', 'main.py'])
                    waiting_for_input = False

def run_program():
    global selected_item
    if selected_item == 0:  # Démarrer le Test
        # Collecter les données utilisateur
        userdata = collect_user_data()

        # Lancer les mini-jeux dans l'ordre avec les données utilisateur
        minijeu1.introduction()  # Introduction du premier jeu
        minijeu1.reaction_test()  # Test de réaction du premier jeu

        minijeu2.introduction()  # Introduction du deuxième jeu
        minijeu2.rhythm_test()   # Test du rythme du deuxième jeu

        minijeu3.typing_test()   # Test de frappe du troisième jeu

    elif selected_item == 1:  # Leaderboard
        # Lancer le leaderboard
        importlib.import_module("leaderboard").run()

    elif selected_item == 2:  # Quitter
        pygame.quit()
        sys.exit()


# Fonction principale du menu
def main_menu():
    global selected_item

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if selected_item != -1:
                    run_program()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # Mise à jour de l'input souris
        handle_mouse_input()

        # Afficher le menu
        draw_menu()

        pygame.time.Clock().tick(60)  # Limite à 60 FPS

if __name__ == "__main__":
    main_menu()
