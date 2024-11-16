import pygame
import time

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Test de Rythme")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)

# Polices dynamiques
def get_font(size):
    return pygame.font.Font(pygame.font.get_default_font(), size)

def draw_text_multiline(screen, text, font, color, rect, line_spacing=5):
    """
    Affiche un texte multiligne centré à l'intérieur d'un rectangle donné.
    Gère automatiquement les retours à la ligne et les sauts explicites (\n).
    """
    # Diviser le texte par lignes en respectant "\n"
    paragraphs = text.split('\n')  # Liste de paragraphes séparés par "\n"
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

    # Calculer la hauteur totale pour centrer verticalement
    total_height = len(lines) * font.size("Tg")[1] + (len(lines) - 1) * line_spacing
    y_offset = rect.y + (rect.height - total_height) // 2

    for line in lines:
        text_surface = font.render(line, True, color)
        text_rect = text_surface.get_rect(center=(rect.centerx, y_offset))
        screen.blit(text_surface, text_rect)
        y_offset += font.size("Tg")[1] + line_spacing

def draw_text(screen, text, font, color, rect):
    """
    Affiche un texte centré dans un rectangle donné.
    """
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

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

        # Affichage du titre
        draw_text(
            screen,
            "Bienvenue au Test de Rythme!",
            title_font,
            BLACK,
            pygame.Rect(0, HEIGHT // 8, WIDTH, 50)
        )

        # Affichage du sous-titre
        draw_text(
            screen,
            "Règles du jeu",
            subtitle_font,
            BLACK,
            pygame.Rect(0, HEIGHT // 4, WIDTH, 40)
        )

        # Affichage des règles en plusieurs lignes
        draw_text_multiline(
            screen,
            (
                "1. Après le décompte, appuyez sur la barre d'espace quatre fois.\n"
                "2. Chaque appui doit être à 1000ms d'écart entre chaque.\n"
                "3. Le but est d'appuyer en rythme pour minimiser l'écart."
            ),
            body_font,
            GRAY,
            body_rect,
        )

        # Instructions pour commencer
        draw_text(
            screen,
            "Appuyez sur Entrée pour commencer.",
            body_font,
            RED,
            pygame.Rect(0, HEIGHT - 100, WIDTH, 40),
        )

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Appuyer sur Entrée pour commencer
                    running = False
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit()

def rhythm_test():
    """
    Exécute le mini-jeu de rythme avec quatre appuis et enregistre les résultats.
    """
    errors = []  # Liste pour stocker les écarts d'appuis
    running = True

    # Affichage du décompte avant le test
    for i in range(3, 0, -1):
        screen.fill(WHITE)
        draw_text(screen, str(i), get_font(72), BLACK, pygame.Rect(0, HEIGHT // 2 - 40, WIDTH, 80))
        pygame.display.flip()
        pygame.time.wait(1000)

    # Afficher "GO" pour commencer
    screen.fill(WHITE)
    draw_text(screen, "GO!", get_font(72), BLACK, pygame.Rect(0, HEIGHT // 2 - 40, WIDTH, 80))
    pygame.display.flip()
    pygame.time.wait(500)

    # Enregistrement des temps d'appuis
    start_time = time.time()
    pressed_times = []
    while len(pressed_times) < 4:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    elapsed_time = (time.time() - start_time) * 1000  # Convertir en ms
                    pressed_times.append(elapsed_time)

                # Si 4 appuis sont enregistrés, on arrête
                if len(pressed_times) == 4:
                    break
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit()

    # Calcul des erreurs par rapport aux 1000ms d'écart
    errors = []
    for i in range(1, len(pressed_times)):
        error = round(pressed_times[i] - pressed_times[i - 1] - 1000)
        errors.append(error)

    # Calcul de la moyenne des erreurs
    mean_error = round(sum(errors) / len(errors))

    
    # Afficher les résultats finaux
    screen.fill(WHITE)
    result_text = (
        f"Seconde 1: {errors[0]} ms\n"
        f"Seconde 2: {errors[1]} ms\n"
        f"Seconde 3: {errors[2]} ms\n"
        f"Moyenne: {mean_error} ms"
    )
    draw_text_multiline(screen, result_text, get_font(28), BLACK, pygame.Rect(0, HEIGHT // 2 - 80, WIDTH, 160))

    # Ajouter le message en bas pour indiquer "Appuyez sur Entrée pour quitter"
    draw_text(
        screen,
        "Appuyez sur Entrée pour quitter.",
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


if __name__ == "__main__":
    introduction()
    rhythm_test()

