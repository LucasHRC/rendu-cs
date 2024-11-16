import pygame
import random
import time
import csv
from datetime import datetime

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Test de Réaction")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)

# Polices dynamiques
def get_font(size):
    return pygame.font.Font(pygame.font.get_default_font(), size)

# Nom du fichier CSV
CSV_FILE = "score.csv"

def save_to_csv(react1, react2, mean_react):
    """
    Enregistre les résultats dans le fichier CSV en ajoutant uniquement
    les temps de réaction et la moyenne à la suite de l'enregistrement de l'utilisateur.
    """
    file_exists = False
    existing_data = []
    
    # Lire le contenu existant du fichier CSV pour savoir si des données existent
    try:
        with open(CSV_FILE, 'r', newline='') as file:
            reader = csv.reader(file)
            existing_data = list(reader)
            file_exists = True
    except FileNotFoundError:
        pass

    # Si le fichier n'existe pas encore, on l'initialise avec un en-tête.
    if not file_exists:
        with open(CSV_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Pseudo", "Age", "Sexe", "Main Dominante", "React1 (ms)", "React2 (ms)", "MeanReact (ms)"])

    # Ajouter les résultats à la fin de la ligne correspondante
    if file_exists and existing_data:
        # Prendre la dernière ligne avec les informations de l'utilisateur
        last_user_data = existing_data[-1]
        
        # Ajouter uniquement les résultats (temps de réaction 1, 2 et la moyenne)
        with open(CSV_FILE, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([last_user_data[0], last_user_data[1], last_user_data[2], last_user_data[3], last_user_data[4], react1, react2, mean_react])

def draw_text_multiline(screen, text, font, color, rect, line_spacing=5):
    """
    Affiche un texte multiligne centré à l'intérieur d'un rectangle donné.
    Gère automatiquement les retours à la ligne et les sauts explicites (\n).
    """
    paragraphs = text.split('\n')
    lines = []
    
    for paragraph in paragraphs:
        words = paragraph.split(' ')
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] <= rect.width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "
        lines.append(current_line.strip())  # Ajouter la dernière ligne du paragraphe

    total_height = len(lines) * font.size("Tg")[1] + (len(lines) - 1) * line_spacing
    y_offset = rect.y + (rect.height - total_height) // 2

    for line in lines:
        text_surface = font.render(line, True, color)
        text_rect = text_surface.get_rect(center=(rect.centerx, y_offset))
        screen.blit(text_surface, text_rect)
        y_offset += font.size("Tg")[1] + line_spacing

def introduction():
    """
    Affiche une introduction expliquant les règles du mini-jeu.
    """
    running = True
    while running:
        screen.fill(WHITE)

        title_font = get_font(42)
        subtitle_font = get_font(28)
        body_font = get_font(22)

        body_rect = pygame.Rect(100, HEIGHT // 3, WIDTH - 200, HEIGHT // 3)

        draw_text_multiline(
            screen,
            "Bienvenue au Test de Réaction!",
            title_font,
            BLACK,
            pygame.Rect(0, HEIGHT // 8, WIDTH, 50)
        )

        draw_text_multiline(
            screen,
            "Règles du jeu",
            subtitle_font,
            BLACK,
            pygame.Rect(0, HEIGHT // 4, WIDTH, 40)
        )

        draw_text_multiline(
            screen,
            (
                "1. Lorsque l'écran devient vert, appuyez sur une touche aussi vite que possible.\n"
                "2. Vous ferez deux essais, et une moyenne sera calculée.\n"
                "3. Les résultats seront enregistrés automatiquement."
            ),
            body_font,
            GRAY,
            body_rect,
        )

        draw_text_multiline(
            screen,
            "Appuyez sur une touche pour commencer.",
            body_font,
            RED,
            pygame.Rect(0, HEIGHT - 100, WIDTH, 40),
        )

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                running = False
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit()

def reaction_test():
    """
    Exécute le mini-jeu de test de réaction avec deux itérations et enregistre les résultats.
    """
    results = []  # Liste pour stocker les temps de réaction
    for i in range(2):  # Deux itérations
        # Afficher "Préparez-vous"
        screen.fill(WHITE)
        draw_text_multiline(screen, "Préparez-vous...", get_font(28), BLACK, pygame.Rect(0, HEIGHT // 2 - 20, WIDTH, 40))
        pygame.display.flip()
        pygame.time.wait(2000)

        # Attente aléatoire avant le changement de couleur
        wait_time = random.uniform(2, 5)
        pygame.time.wait(int(wait_time * 1000))

        # Changement de couleur (début du test)
        screen.fill(GREEN)
        pygame.display.flip()

        # Enregistrer le temps de départ au moment où l'écran devient vert
        start_time = time.time()

        # Surveillance des appuis de touches après que l'écran devient vert
        reacted = False
        while not reacted:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    # Enregistrer le temps de réaction quand une touche est pressée
                    reaction_time = (time.time() - start_time) * 1000  # Convertir en ms
                    results.append(round(reaction_time))
                    reacted = True
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

        # Message d'indication après avoir enregistré le temps
        screen.fill(WHITE)
        draw_text_multiline(
            screen,
            f"Réaction: {results[-1]} ms",
            get_font(28),
            RED,
            pygame.Rect(0, HEIGHT // 2 - 20, WIDTH, 40),
        )
        pygame.display.flip()
        pygame.time.wait(2000)

    # Calcul de la moyenne des temps de réaction
    mean_reaction = round(sum(results) / len(results))

    # Afficher les résultats finaux
    screen.fill(WHITE)
    draw_text_multiline(
        screen,
        f"Test terminé !\nRéaction 1: {results[0]} ms\nRéaction 2: {results[1]} ms\nMoyenne: {mean_reaction} ms",
        get_font(28),
        BLACK,
        pygame.Rect(0, HEIGHT // 2 - 40, WIDTH, 80),
    )

    # Ajouter le message en bas pour indiquer "Appuyez sur Entrée pour la suite"
    draw_text_multiline(
        screen,
        "Appuyez sur Entrée pour la suite.",
        get_font(22),
        BLACK,
        pygame.Rect(0, HEIGHT - 50, WIDTH, 40),
    )
    
    pygame.display.flip()

    # Attendre que l'utilisateur appuie sur "Entrée" pour continuer
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Si la touche Entrée est pressée, on continue
                    waiting_for_input = False
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit()

    # Sauvegarder les résultats dans le fichier CSV
    save_to_csv(results[0], results[1], mean_reaction)

    # Quitter proprement
    #pygame.quit()

if __name__ == "__main__":
    introduction()
    reaction_test()
