import pygame
from config import screen_width, screen_height

class Home:
    def __init__(self, screen):
        # Initialiser les paramètres du jeu
        self.screen = screen

        # Créer le bouton "Play"
        self.button_color = (255, 255, 0)  # Couleur jaune pour le bouton
        self.font = pygame.font.Font(None, 50)
        self.small_font = pygame.font.Font(None, 36)
        self.background_img = pygame.image.load('assets/images/background.jpg')
        self.background = pygame.transform.scale(self.background_img, (screen_width, screen_height))
        self.button_rect = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 140, 200, 50)

        # Créer un rectangle pour le bouton "Play"
        self.button_text = self.font.render("Play", True, (0, 0, 0))

    def render(self, nb_wins):
        self.screen.blit(self.background, (0, 0))
        self.draw_button()
        self.draw_play_text()
        self.verify_cursor()
        self.draw_nb_wins(nb_wins)
        
    def draw_button(self):
        pygame.draw.rect(self.screen, self.button_color, self.button_rect)

    def draw_play_text(self):
        text_x = self.button_rect.x + (self.button_rect.width - self.button_text.get_width()) // 2
        text_y = self.button_rect.y + (self.button_rect.height - self.button_text.get_height()) // 2
        self.screen.blit(self.button_text, (text_x, text_y))

    def verify_cursor(self):
        # Vérifier si la souris survole le bouton
        if self.button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def draw_nb_wins(self, nb_wins):
        # Afficher le score
        nb_wins_text = self.small_font.render(f"Number of Wins: {nb_wins}", True, (255, 255, 0))
        nb_wins_text_rect = nb_wins_text.get_rect(center=(screen_width // 2, screen_height // 2 + 225))
        self.screen.blit(nb_wins_text, nb_wins_text_rect)


    def is_button_clicked(self, pos):
        return self.button_rect.collidepoint(pos)