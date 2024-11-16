import pygame
import time
import random

# Initialisation de pygame
pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Test de Rapidité d'Écriture")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GRAY = (50, 50, 50)
LIGHT_GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Polices
def get_font(size):
    return pygame.font.Font(None, size)

# Base de mots sans accents pour générer un texte
word_list = [
    "chien", "chat", "voiture", "maison", "arbre", "souris", "table", "laptop", "mouton", "elephant",
    "ordinateur", "maison", "bureau", "vache", "nuage", "ocean", "paysage", "foret", "jardin", "fleur",
    "ciel", "montagne", "océan", "piscine", "robot", "musique", "voilier", "océan", "paon", "papillon",
    "drapeau", "bonte", "calme", "poisson", "route", "velo", "chanson", "lecture", "sports", "saison"
]

def generate_text():
    """
    Génère un texte aléatoire de 10 mots.
    """
    return " ".join(random.sample(word_list, 10))

def draw_text(text, font, color, x, y, max_width):
    """
    Affiche le texte à la position (x, y), en veillant à ce qu'il ne dépasse pas la largeur spécifiée.
    Le texte sera découpé en plusieurs lignes si nécessaire.
    """
    words = text.split(' ')
    lines = []
    current_line = ""

    for word in words:
        # Tester si le mot ajouté à la ligne actuelle dépasse la largeur
        test_line = current_line + " " + word if current_line else word
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word  # Nouveau mot commence une nouvelle ligne

    if current_line:
        lines.append(current_line)

    # Affichage des lignes de texte
    y_offset = y
    for line in lines:
        rendered_text = font.render(line, True, color)
        x_offset = x - rendered_text.get_width() // 2  # Centrer horizontalement
        screen.blit(rendered_text, (x_offset, y_offset))
        y_offset += rendered_text.get_height()

def typing_test():
    """
    Exécute le test de rapidité d'écriture.
    """
    screen.fill(WHITE)
    font = get_font(36)
    
    # Générer un texte aléatoire
    text_to_type = generate_text()

    # Page d'instructions
    title = "Test de Rapidité d'Écriture"
    subtitle = "Préparez-vous à taper le texte le plus rapidement possible!"
    instructions = [
        "1. Un texte va être affiché pendant 5 secondes.",
        "2. Après le décompte, commencez à taper le texte exactement comme il apparaît.",
        "3. Le temps que vous prendrez pour taper sera mesuré."
    ]
    
    # Affichage du titre et sous-titre
    screen.fill(WHITE)
    title_text = font.render(title, True, DARK_GRAY)
    subtitle_text = get_font(24).render(subtitle, True, LIGHT_GRAY)

    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))
    screen.blit(subtitle_text, (WIDTH // 2 - subtitle_text.get_width() // 2, HEIGHT // 4 + 60))

    # Affichage des instructions séparées, chaque ligne étant affichée une à une
    instruction_font = get_font(24)
    y_offset = HEIGHT // 2  # Position initiale pour les instructions
    for instruction in instructions:
        draw_text(instruction, instruction_font, DARK_GRAY, WIDTH // 2, y_offset, WIDTH - 80)
        y_offset += 40  # Espacement entre chaque ligne d'instruction

    # Affichage de l'indication pour commencer
    start_text = get_font(24).render("Appuyez sur Entrée pour commencer", True, RED)
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT - 80))

    pygame.display.flip()
    
    # Attente de l'entrée de l'utilisateur pour commencer
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting_for_input = False
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit()

    # Afficher le texte à taper avant le décompte
    screen.fill(WHITE)
    draw_text(f"Texte à taper : {text_to_type}", font, BLACK, WIDTH // 2, HEIGHT // 4, WIDTH - 40)
    pygame.display.flip()

    # Décompte de 5 secondes avant de commencer
    start_countdown = time.time()
    while time.time() - start_countdown < 5:
        screen.fill(WHITE)
        remaining_time = 5 - (time.time() - start_countdown)
        
        # Afficher à la fois le texte à taper et le décompte
        draw_text(f"Texte à taper : {text_to_type}", font, BLACK, WIDTH // 2, HEIGHT // 4, WIDTH - 40)

        # Affichage du décompte
        countdown_text = font.render(f"Début dans {int(remaining_time)}...", True, DARK_GRAY)
        countdown_x_offset = WIDTH // 2 - countdown_text.get_width() // 2
        screen.blit(countdown_text, (countdown_x_offset, HEIGHT // 2 + 100))

        pygame.display.flip()

    # Enregistrer le temps de début
    typing_start_time = time.time()

    # Lancer le test : Attendre que l'utilisateur commence à taper
    user_input = ""
    start_time = time.time()
    
    while user_input != text_to_type:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        # Affichage du texte tapé par l'utilisateur
        screen.fill(WHITE)
        typed_text = font.render(f"Votre texte : {user_input}", True, GREEN)
        
        # Gérer le retour à la ligne du texte que l'utilisateur écrit
        draw_text(f"Texte à taper : {text_to_type}", font, BLACK, WIDTH // 2, HEIGHT // 4, WIDTH - 40)

        # Afficher aussi le texte original pour référence
        draw_text(f"Votre texte : {user_input}", font, GREEN, WIDTH // 2, HEIGHT // 2, WIDTH - 40)

        pygame.display.flip()

    # Calcul du temps total
    total_time = time.time() - start_time

    # Calcul du temps de réaction (temps avant de commencer à taper après les 5 secondes)
    reaction_time = round(time.time() - typing_start_time - 5, 2)

    # Calcul du temps moyen par mot
    num_words = len(text_to_type.split())
    typing_time_per_word = round(total_time / num_words, 2)

    # Calcul de la vitesse de frappe en mots par minute (wpm)
    typing_speed = round((num_words / total_time) * 60, 2)

    # Affichage des résultats
    screen.fill(WHITE)
    result_font = get_font(28)
    time_text = result_font.render(f"Temps total : {total_time:.2f} secondes", True, DARK_GRAY)
    reaction_text = result_font.render(f"Temps de réaction : {reaction_time} secondes", True, DARK_GRAY)
    typing_time_per_word_text = result_font.render(f"Temps par mot : {typing_time_per_word} secondes", True, DARK_GRAY)
    typing_speed_text = result_font.render(f"Vitesse de frappe : {typing_speed} mots/minute", True, DARK_GRAY)
    
    screen.blit(time_text, (WIDTH // 2 - time_text.get_width() // 2, HEIGHT // 3))
    screen.blit(reaction_text, (WIDTH // 2 - reaction_text.get_width() // 2, HEIGHT // 3 + 40))
    screen.blit(typing_time_per_word_text, (WIDTH // 2 - typing_time_per_word_text.get_width() // 2, HEIGHT // 3 + 80))
    screen.blit(typing_speed_text, (WIDTH // 2 - typing_speed_text.get_width() // 2, HEIGHT // 3 + 120))
    
    message = result_font.render("Appuyez sur Entrée pour revenir au menu.", True, RED)
    screen.blit(message, (WIDTH // 2 - message.get_width() // 2, HEIGHT - 100))
    
    pygame.display.flip()

    # Attente de l'entrée de l'utilisateur pour quitter ou recommencer
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit()

if __name__ == "__main__":
    typing_test()
    pygame.quit()
