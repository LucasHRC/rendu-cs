import pygame
import random
import sys

# Initialisation de Pygame
pygame.init()

# Dimensions de l'écran
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Doodle Jump")

# Définition des couleurs
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Définir les paramètres de la gravité et du saut
GRAVITY = 0.5
JUMP_VELOCITY = -12
PLATFORM_FALL_SPEED = 2

# Classe du joueur
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)  # Position initiale
        self.speed_x = 0
        self.velocity_y = 0
        self.on_ground = False
        self.is_alive = True
        self.max_height = self.rect.top  # Hauteur maximale atteinte

    def update(self):
        """ Met à jour la position du joueur et applique la gravité """
        if self.is_alive:
            # Applique la gravité uniquement si le joueur n'est pas sur une plateforme
            if not self.on_ground:
                self.velocity_y += GRAVITY

            self.rect.x += self.speed_x
            self.rect.y += self.velocity_y

            # Si le joueur sort de l'écran, il réapparaît de l'autre côté
            if self.rect.left < 0:
                self.rect.left = SCREEN_WIDTH
            if self.rect.right > SCREEN_WIDTH:
                self.rect.right = 0

            # Si le joueur tombe sous l'écran, il meurt
            if self.rect.bottom > SCREEN_HEIGHT:
                self.is_alive = False

            # Met à jour la hauteur maximale atteinte
            if self.rect.top < self.max_height:
                self.max_height = self.rect.top

        return self.is_alive

    def jump(self):
        """ Le joueur saute s'il est sur une plateforme """
        if self.on_ground:
            self.velocity_y = JUMP_VELOCITY
            self.on_ground = False

    def check_platform_collision(self, platforms):
        """ Vérifie les collisions du joueur avec les plateformes """
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.rect.bottom <= platform.rect.centery + 10 and self.rect.bottom >= platform.rect.centery - 10:
                self.velocity_y = 0
                self.rect.bottom = platform.rect.top
                self.on_ground = True
                break

# Classe pour les plateformes
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((60, 15))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        """ Déplace les plateformes vers le bas et les réinitialise """
        self.rect.y += PLATFORM_FALL_SPEED
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.y = random.randint(-100, -10)
            self.rect.x = random.randint(0, SCREEN_WIDTH - 60)

# Fonction principale du jeu
def game_loop():
    # Initialisation des objets
    player = Player()
    platforms = pygame.sprite.Group()

    # Créer les plateformes initiales
    for i in range(30):  # Augmente le nombre de plateformes
        platform = Platform(random.randint(0, SCREEN_WIDTH - 60), random.randint(50, SCREEN_HEIGHT - 50))
        platforms.add(platform)

    all_sprites = pygame.sprite.Group(player, *platforms)

    camera_y = 0  # Initialisation de la caméra
    score = 0  # Score basé sur la hauteur max

    clock = pygame.time.Clock()

    while True:
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Mise à jour du joueur et des plateformes
        player.update()
        platforms.update()

        # Vérification des collisions avec les plateformes
        player.check_platform_collision(platforms)

        # Mise à jour du score en fonction de la hauteur maximale atteinte
        score = (player.max_height - camera_y) // 10  # Conversion en centimètres

        # Déplacement de la caméra
        if player.rect.top < player.max_height:  # Si le joueur grimpe à une nouvelle hauteur
            camera_y = player.max_height
        camera_y = max(camera_y, player.max_height)

        # Affichage
        screen.fill(WHITE)

        # Afficher les plateformes
        for platform in platforms:
            screen.blit(platform.image, platform.rect)

        # Afficher le joueur
        screen.blit(player.image, player.rect)

        # Afficher le score
        font = pygame.font.SysFont('Arial', 24)
        score_text = font.render(f"Score: {score} cm", True, BLACK)
        screen.blit(score_text, (10, 10))

        # Mettre à jour l'écran
        pygame.display.flip()

        # Limiter les FPS
        clock.tick(60)

if __name__ == "__main__":
    game_loop()
