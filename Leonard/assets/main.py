import pygame
import sys
import random
import time

# Initialisation de Pygame
pygame.init()

# Taille de la fenêtre
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Jeu de Léonard avec Pygame")

# Couleurs
WHITE = (255, 255, 255)
BLUE = (135, 206, 235)  # Couleur du ciel
GREY = (105, 105, 105)  # Couleur de la plateforme

# Charger les images en version plus petite
try:
    leonard_img = pygame.image.load("assets/leonard.png").convert_alpha()
    leonard_img = pygame.transform.scale(leonard_img, (100, 100))  # Personnage réduit
    wei_img = pygame.image.load("assets/wei.png").convert_alpha()
    wei_img = pygame.transform.scale(wei_img, (50, 50))
    haltere_img = pygame.image.load("assets/haltere.png").convert_alpha()
    haltere_img = pygame.transform.scale(haltere_img, (50, 50))
    pizza_img = pygame.image.load("assets/pizza.png").convert_alpha()
    pizza_img = pygame.transform.scale(pizza_img, (50, 50))
    nutella_img = pygame.image.load("assets/nutella.png").convert_alpha()
    nutella_img = pygame.transform.scale(nutella_img, (50, 50))
    pet_img = pygame.image.load("assets/pet.png").convert_alpha()
except FileNotFoundError:
    print("Assurez-vous que tous les assets sont dans le dossier 'assets'.")
    sys.exit()

# Variables du personnage
leonard_x, leonard_y = 100, screen_height - 150
velocity_y = 0
gravity = 0.8
jump_strength = -14
double_jump_allowed = False
on_platform = False  # Vérifie si le personnage est sur une plateforme

# Variables de jeu
score = 0
wei_count = 0
game_speed = 6
pet_foudroyant_active = False
pet_foudroyant_duration = 5
pet_foudroyant_start_time = None

# Variables des objets
object_types = ["wei", "haltere", "pizza", "nutella"]
objects = []

# Variables des plateformes en mouvement
platforms = []

# Fonction pour créer des objets aléatoires
def create_random_object():
    obj_type = random.choice(object_types)
    obj_x = screen_width
    obj_y = random.choice([screen_height - 80, screen_height - 180, screen_height - 280])
    return {"type": obj_type, "x": obj_x, "y": obj_y, "speed": game_speed}

# Fonction pour créer une plateforme en mouvement
def create_moving_platform():
    plat_x = screen_width
    plat_y = random.choice([screen_height - 200, screen_height - 300])
    return {"x": plat_x, "y": plat_y, "width": 120, "height": 20, "speed": game_speed}

# Boucle de jeu principale
clock = pygame.time.Clock()
running = True
while running:
    screen.fill(BLUE)  # Fond bleu pour le ciel

    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not double_jump_allowed and (leonard_y >= screen_height - 150 or on_platform):
                    velocity_y = jump_strength  # Premier saut
                    double_jump_allowed = True
                    on_platform = False
                elif double_jump_allowed:
                    velocity_y = jump_strength  # Double saut
                    double_jump_allowed = False
            elif event.key == pygame.K_p and wei_count >= 5:
                pet_foudroyant_active = True
                pet_foudroyant_start_time = time.time()
                wei_count = 0  # Réinitialise le compteur Wei

    # Appliquer la gravité et mettre à jour la position
    leonard_y += velocity_y
    if not on_platform:
        velocity_y += gravity  # Appliquer la gravité uniquement si non sur une plateforme

    # Repositionnement au sol
    if leonard_y >= screen_height - 150:
        leonard_y = screen_height - 150
        double_jump_allowed = False

    # Mise à jour des objets
    if random.randint(1, 60) == 1:
        objects.append(create_random_object())

    # Mise à jour des plateformes
    if random.randint(1, 120) == 1:
        platforms.append(create_moving_platform())

    # Mettre à jour la position des objets et détecter les collisions
    for obj in objects[:]:
        obj["x"] -= obj["speed"]

        # Collision avec Léonard
        if leonard_x < obj["x"] < leonard_x + leonard_img.get_width() and leonard_y < obj["y"] < leonard_y + leonard_img.get_height():
            if obj["type"] == "wei":
                score += 2
                wei_count += 1
            elif obj["type"] == "haltere":
                score += 1
            elif obj["type"] == "pizza":
                score -= 1
                wei_count = 0
            elif obj["type"] == "nutella":
                score -= 2
                wei_count = 0
            objects.remove(obj)  # Supprime l'objet après interaction

        # Supprimer les objets hors de l'écran
        if obj["x"] < -50:
            objects.remove(obj)

    # Mettre à jour la position des plateformes
    on_platform = False
    for platform in platforms[:]:
        platform["x"] -= platform["speed"]

        # Vérifie si Léonard atterrit sur une plateforme
        if leonard_x + 50 > platform["x"] and leonard_x < platform["x"] + platform["width"]:
            if leonard_y + leonard_img.get_height() >= platform["y"]:
                leonard_y = platform["y"] - leonard_img.get_height()
                on_platform = True
                velocity_y = 0  # Réinitialise la vitesse verticale

        # Supprimer les plateformes hors de l'écran
        if platform["x"] < -platform["width"]:
            platforms.remove(platform)

    # Activer l'effet Pet Foudroyant
    if pet_foudroyant_active:
        game_speed = 12  # Double la vitesse des objets pendant l'effet
        screen.blit(pet_img, (leonard_x - 20, leonard_y + 30))
        if time.time() - pet_foudroyant_start_time >= pet_foudroyant_duration:
            pet_foudroyant_active = False
            game_speed = 6

    # Affichage des objets
    for obj in objects:
        if obj["type"] == "wei":
            screen.blit(wei_img, (obj["x"], obj["y"]))
        elif obj["type"] == "haltere":
            screen.blit(haltere_img, (obj["x"], obj["y"]))
        elif obj["type"] == "pizza":
            screen.blit(pizza_img, (obj["x"], obj["y"]))
        elif obj["type"] == "nutella":
            screen.blit(nutella_img, (obj["x"], obj["y"]))

    # Affichage des plateformes
    for platform in platforms:
        pygame.draw.rect(screen, GREY, (platform["x"], platform["y"], platform["width"], platform["height"]))

    # Affichage de Léonard
    screen.blit(leonard_img, (leonard_x, leonard_y))

    # Affichage du score et du compteur Wei
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    wei_text = font.render(f"Wei Count: {wei_count}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(wei_text, (10, 50))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
