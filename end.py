import pygame
from config import screen_width, screen_height


class End:
    def __init__(self):
        pygame.init()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.white = (255, 255, 255)

        # Set up the screen
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Résultat du Jeu')
        
        # Load background image
        self.background_image = pygame.image.load('assets/images/game_over.jpg')
        self.background_image = pygame.transform.scale(self.background_image, (self.screen_width, self.screen_height))
        
        # Set up font
        self.font = pygame.font.Font(None, 74)

    def render(self, result):
        # Determine the message based on the result
        if result == True:
            text = self.font.render('Vous avez gagné !', True, self.white)
        else:
            text = self.font.render('Vous avez perdu...', True, self.white)
        
        # Text position
        text_rect = text.get_rect(center=(self.screen_width / 2, self.screen_height / 2 + 50))
        
        # Draw everything
        self.screen.blit(self.background_image, (0, 0))
        self.screen.blit(text, text_rect)
            
        pygame.display.flip()

        pygame.time.wait(5000)  # Wait for 5 seconds before closing the window