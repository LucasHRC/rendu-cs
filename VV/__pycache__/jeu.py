import pygame
import random
import time
from textwrap import wrap

# Initialisation de Pygame
pygame.init()

# Configuration initiale
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Mini-Jeux")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (50, 50, 50)

# Dessiner du texte adaptable
def draw_text_adaptive(text, font_size, color, x, y, max_width, center=True):
    """
    Affiche un texte adaptable dans une zone définie, en ajustant la taille des lignes si nécessaire.

    Args:
        text (str): Texte à afficher.
        font_size (int): Taille de base de la police.
        color (tuple): Couleur du texte.
        x (int): Coordonnée x du texte.
        y (int): Coordonnée y du texte.
        max_width (int): Largeur maximale avant de couper le texte en plusieurs lignes.
        center (bool): Si vrai, centre chaque ligne horizontalement.
    """
    font = pygame.font.Font(pygame.font.get_default_font(), font_size)
    wrapped_lines = wrap(text, width=int(max_width / (font_size * 0.6)))
    for i, line in enumerate(wrapped_lines):
        text_surface = font.render(line, True, color)
        text_rect = text_surface.get_rect()
        if center:
            text_rect.center = (x, y + i * (font_size + 5))
        else:
            text_rect.topleft = (x, y + i * (font_size + 5))
        screen.blit(text_surface, text_rect)

# Dessiner du texte avec titres et sous-titres
def draw_section(title, subtitle, body_lines, x, y, width, font_sizes):
    """
    Organise une section avec titre, sous-titre, et corps de texte.

    Args:
        title (str): Titre principal.
        subtitle (str): Sous-titre.
        body_lines (list of str): Contenu du corps du texte.
        x (int): Coordonnée x de la section.
        y (int): Coordonnée y de la section.
        width (int): Largeur maximale de la section.
        font_sizes (tuple): Tailles des polices pour le titre, sous-titre, et corps.
    """
    title_font, subtitle_font, body_font = font_sizes
    draw_text_adaptive(title, title_font, BLACK, x, y, width)
    draw_text_adaptive(subtitle, subtitle_font, GRAY, x, y + 50, width)
    for i, line in enumerate(body_lines):
        draw_text_adaptive(line, body_font, BLACK, x, y + 100 + i * 30, width)

# Fonction utilitaire pour attendre une touche
def wait_for_key(key):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == key:
                return
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit()

# Mini-jeu 1 : Test de réactivité
def reaction_test():
    screen.fill(WHITE)
    draw_section(
        "Mini-jeu 1 : Test de réactivité",
        "Instructions",
        ["Appuyez sur ESPACE uniquement lorsque l'écran devient rouge."],
        WIDTH // 2,
        HEIGHT // 4,
        WIDTH - 100,
        (36, 24, 20),
    )
    draw_text_adaptive("Appuyez sur Entrée pour commencer.", 20, GRAY, WIDTH // 2, HEIGHT - 50, WIDTH - 100)
    pygame.display.flip()
    wait_for_key(pygame.K_RETURN)

    reaction_times = []

    for attempt in range(2):
        screen.fill(GRAY)
        draw_text_adaptive("Préparez-vous...", 24, WHITE, WIDTH // 2, HEIGHT // 2, WIDTH - 100)
        pygame.display.flip()
        time.sleep(random.uniform(2, 5))

        # L'écran devient rouge
        screen.fill(RED)
        pygame.display.flip()
        start_time = time.time()

        reacted = False
        while not reacted:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    # Empêcher d'enregistrer l'appui avant que l'écran ne devienne rouge
                    if time.time() - start_time >= 0:
                        reaction_time = (time.time() - start_time) * 1000  # en ms
                        reaction_times.append(reaction_time)
                        reacted = True

    screen.fill(WHITE)
    for i, rt in enumerate(reaction_times):
        draw_text_adaptive(f"Essai {i + 1}: {rt:.2f} ms", 24, BLACK, WIDTH // 2, HEIGHT // 2 + i * 40, WIDTH - 100)
    draw_text_adaptive("Appuyez sur Entrée pour continuer.", 20, GRAY, WIDTH // 2, HEIGHT - 50, WIDTH - 100)
    pygame.display.flip()
    wait_for_key(pygame.K_RETURN)

# Mini-jeu 2 : Test de rythme
def rhythm_test():
    screen.fill(WHITE)
    draw_section(
        "Mini-jeu 2 : Test de rythme",
        "Instructions",
        [
            "Après le compte de 1 à 3, appuyez sur ESPACE à chaque seconde.",
            "Essayez de rester le plus proche possible du bon rythme.",
        ],
        WIDTH // 2,
        HEIGHT // 4,
        WIDTH - 100,
        (36, 24, 20),
    )
    draw_text_adaptive("Appuyez sur Entrée pour commencer.", 20, GRAY, WIDTH // 2, HEIGHT - 50, WIDTH - 100)
    pygame.display.flip()
    wait_for_key(pygame.K_RETURN)

    # Compte de 1 à 3
    for i in range(1, 4):
        screen.fill(WHITE)
        draw_text_adaptive(f"{i}", 72, BLACK, WIDTH // 2, HEIGHT // 2, WIDTH - 100)
        pygame.display.flip()
        time.sleep(1)

    # Rythme à tester
    base_time = time.time() + 3  # Commencer après 3 secondes
    timing_diffs = []

    for i in range(4):
        expected_time = base_time + i
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    press_time = time.time()
                    diff = (press_time - expected_time) * 1000  # ms
                    timing_diffs.append(diff)
                    waiting = False

    # Afficher les résultats
    avg_diff = sum(timing_diffs) / len(timing_diffs)
    screen.fill(WHITE)
    for i, diff in enumerate(timing_diffs):
        draw_text_adaptive(f"Seconde {i + 1}: {diff:+.2f} ms", 24, BLACK, WIDTH // 2, HEIGHT // 2 + i * 40, WIDTH - 100)
    draw_text_adaptive(f"Moyenne: {avg_diff:+.2f} ms", 24, BLACK, WIDTH // 2, HEIGHT // 2 + 160, WIDTH - 100)
    draw_text_adaptive("Appuyez sur Entrée pour continuer.", 20, GRAY, WIDTH // 2, HEIGHT - 50, WIDTH - 100)
    pygame.display.flip()
    wait_for_key(pygame.K_RETURN)

# Mini-jeu 3 : Test de rapidité d'écriture
def typing_test():
    screen.fill(WHITE)
    draw_section(
        "Mini-jeu 3 : Écriture rapide",
        "Instructions",
        ["Vous verrez un texte.",
         "Recopiez-le le plus rapidement possible après 5 secondes."],
        WIDTH // 2,
        HEIGHT // 4,
        WIDTH - 100,
        (36, 24, 20),
    )
    draw_text_adaptive("Appuyez sur Entrée pour commencer.", 20, GRAY, WIDTH // 2, HEIGHT - 50, WIDTH - 100)
    pygame.display.flip()
    wait_for_key(pygame.K_RETURN)

    text_to_type = "The quick brown fox jumps over the lazy dog."
    user_input = ""
    start_time = time.time()

    # Décompte avant de commencer
    screen.fill(WHITE)
    draw_text_adaptive("Préparez-vous...", 24, BLACK, WIDTH // 2, HEIGHT // 2, WIDTH - 100)
    pygame.display.flip()
    time.sleep(1)

    for i in range(5, 0, -1):
        screen.fill(WHITE)
        draw_text_adaptive(str(i), 72, BLACK, WIDTH // 2, HEIGHT // 2, WIDTH - 100)
        pygame.display.flip()
        time.sleep(1)

    screen.fill(WHITE)
    draw_text_adaptive("GO!", 72, BLACK, WIDTH // 2, HEIGHT // 2, WIDTH - 100)
    pygame.display.flip()
    time.sleep(1)

    # Le test commence ici
    typing_started = False
    while not typing_started:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode
            if len(user_input) == len(text_to_type):
                typing_started = True

        screen.fill(WHITE)
        draw_text_adaptive(text_to_type, 24, BLACK, WIDTH // 2, HEIGHT // 2, WIDTH - 100)
        draw_text_adaptive(user_input, 24, BLACK, WIDTH // 2, HEIGHT // 2 + 50, WIDTH - 100)
        pygame.display.flip()

    end_time = time.time()
    time_taken = (end_time - start_time) * 1000  # en ms

    screen.fill(WHITE)
    draw_text_adaptive(f"Temps: {time_taken:.2f} ms", 24, BLACK, WIDTH // 2, HEIGHT // 2, WIDTH - 100)
    draw_text_adaptive("Appuyez sur Entrée pour continuer.", 20, GRAY, WIDTH // 2, HEIGHT - 50, WIDTH - 100)
    pygame.display.flip()
    wait_for_key(pygame.K_RETURN)

# Fonction principale du programme
def main():
    global WIDTH, HEIGHT, screen
    try:
        running = True
        while running:
            screen.fill(WHITE)
            draw_section(
                "Mini-Jeux",
                "Choisissez un jeu",
                ["1. Test de réactivité", "2. Test de rythme", "3. Test de rapidité d'écriture"],
                WIDTH // 2,
                HEIGHT // 4,
                WIDTH - 100,
                (36, 24, 20),
            )
            draw_text_adaptive("ÉCHAP pour quitter", 20, GRAY, WIDTH // 2, HEIGHT - 50, WIDTH - 100)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.VIDEORESIZE:
                    WIDTH, HEIGHT = event.w, event.h
                    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_1:
                        reaction_test()
                    elif event.key == pygame.K_2:
                        rhythm_test()
                    elif event.key == pygame.K_3:
                        typing_test()
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
    finally:
        pygame.quit()

# Exécution du jeu
if __name__ == "__main__":
    main()
