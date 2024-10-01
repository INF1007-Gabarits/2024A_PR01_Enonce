import pygame
import sys
from config import EDIBLE_GHOST_TIMER, RESET_POS1, RESET_POS3, RESET_POS4
from ghost import *
from pacman import PacMan  # Import the PacMan class
from helper import create_board, create_special_coins
from helper import create_coins
from end import End
import threading

class Game:
    def __init__(self, screen):
        # Initialiser les paramètres du jeu
        self.screen = screen
        self.board = create_board()  # Initialize the board
        self.coins = create_coins(self.board)  # Initialize the coins
        self.special_coins = create_special_coins(self.board)  # Initialize the special coins

        self.pacman = PacMan(self.screen, self.board)  # Initialize Pac-Man
        pygame.display.set_caption("Pac-Man")
        self.font = pygame.font.Font(None, 36)
        self.score = 0
        self.wall_color = (0, 0, 255)

        # Charger les images des fantômes
        red_ghost = pygame.transform.scale(pygame.image.load('assets/images/red.png'), GHOST_SIZE)
        blue_ghost = pygame.transform.scale(pygame.image.load('assets/images/blue.png'), GHOST_SIZE)
        orange_ghost = pygame.transform.scale(pygame.image.load('assets/images/orange.png'), GHOST_SIZE)
        pink_ghost = pygame.transform.scale(pygame.image.load('assets/images/pink.png'), GHOST_SIZE)

        # Créer les fantômes
        self.red_ghost_instance = Ghost(pos=RESET_POS1, img=red_ghost, maze=self.board, screen=screen)
        self.blue_ghost_instance = Ghost(pos=RESET_POS2, img=blue_ghost, maze=self.board, screen=screen)
        self.orange_ghost_instance = Ghost(pos=RESET_POS3, img=orange_ghost, maze=self.board, screen=screen)
        self.pink_ghost_instance = Ghost(pos=RESET_POS4, img=pink_ghost, maze=self.board, screen=screen)

        self.ghosts = [self.red_ghost_instance, self.blue_ghost_instance,
                       self.orange_ghost_instance, self.pink_ghost_instance]
        
        self.end = End()
        self.game_over = False
        self.game_won = False
        

    def start(self):
        # Initialiser les paramètres du jeu
        self.board = create_board()

    def render(self):
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row][col] == 1:
                    pygame.draw.rect(self.screen, (0, 0, 0), (col * 50, row * 50, 50, 50))

                    # Draw the borders
                    thickness = 7  # Thickness of the border lines

                    # Draw the borders
                    if row > 0 and self.board[row - 1][col] == 0:  # Top border
                        pygame.draw.line(self.screen, self.wall_color, (col * 50, row * 50), (col * 50 + 50, row * 50),
                                         thickness)
                    if row < len(self.board) - 1 and self.board[row + 1][col] == 0:  # Bottom border
                        pygame.draw.line(self.screen, self.wall_color, (col * 50, row * 50 + 50),
                                         (col * 50 + 50, row * 50 + 50), thickness)
                    if col > 0 and self.board[row][col - 1] == 0:  # Left border
                        pygame.draw.line(self.screen, self.wall_color, (col * 50, row * 50), (col * 50, row * 50 + 50),
                                         thickness)
                    if col < len(self.board[row]) - 1 and self.board[row][col + 1] == 0:  # Right border
                        pygame.draw.line(self.screen, self.wall_color, (col * 50 + 50, row * 50),
                                         (col * 50 + 50, row * 50 + 50), thickness)
                else:
                    # Draw the empty cells
                    pygame.draw.rect(self.screen, (255, 255, 255), (col * 50, row * 50, 50, 50))

                    # Draw the coins
                    if (col, row) in self.coins:
                        pygame.draw.circle(self.screen, (255, 215, 0), (col * 50 + 25, row * 50 + 25), 4)

                    # Draw the special coins
                    if (col, row) in self.special_coins:
                        pygame.draw.circle(self.screen, (255, 215, 0), (col * 50 + 25, row * 50 + 25), 8)

        # Draw the score
        score_text = self.font.render("Score: " + str(self.score), True, (255, 255, 255))
        self.screen.blit(score_text, (50, 50 * 14))

        # Draw the number of lives
        lives_text = self.font.render("Lives: ", True, (255, 255, 255))
        self.screen.blit(lives_text, (50, 50 * 15))

        pacman_image = pygame.transform.scale(pygame.image.load('assets/images/pacman.png'), (30, 30))
        for i in range(self.pacman.lives):
            self.screen.blit(pacman_image, (150 + i * 40, 50 * 15))

    def handle_keypress(self, event):
        pass
        
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                     if self.check_collision((1, 0)):
                        self.pacman.set_direction((1, 0))
                elif event.key == pygame.K_LEFT:
                    if self.check_collision((-1, 0)):
                        self.pacman.set_direction((-1, 0))
                elif event.key == pygame.K_UP:
                    if self.check_collision((0, -1)):
                        self.pacman.set_direction((0, -1))
                elif event.key == pygame.K_DOWN:
                    if self.check_collision((0, 1)):
                        self.pacman.set_direction((0, 1))

                
    def check_collision(self, direction):
        dx, dy = direction

        new_x = self.pacman.x + dx
        new_y = self.pacman.y + dy

        if 0 <= new_x < len(self.board[0]) and 0 <= new_y < len(self.board):
            if self.board[new_y][new_x] == 1: 
                return True
        return False

    def update(self):
        for ghost in self.ghosts:
            ghost.draw()
            ghost.move()

        self.check_collision_between_ghosts_and_pacman()

        self.pacman.move()

        self.pacman.draw()

        self.check_score()

        self.check_special_coins()

    def check_score(self):
        pacman_position = (self.pacman.x, self.pacman.y)
            
        if pacman_position in self.coins:
            self.coins.remove(pacman_position)
            self.score += 10  # Ajouter 10 points par pièce collectée
            print(f"Score: {self.score}")


        if len(self.coins) == 0:
            self.end.render(True)
            self.game_won = True
            self.game_over = True

    def check_special_coins(self):
        pacman_position = (self.pacman.x, self.pacman.y)

        if pacman_position in self.special_coins:
            self.special_coins.remove(pacman_position)
            self.score += 50 
            self.activate_eat_mode()  # Activer le mode "manger"

    def activate_eat_mode(self):
        timer = threading.Timer(EDIBLE_GHOST_TIMER, self.deactivate_eat_mode)
        timer.start()

        # Make the ghosts edible
        self.red_ghost_instance.edible = True
        self.blue_ghost_instance.edible = True
        self.orange_ghost_instance.edible = True
        self.pink_ghost_instance.edible = True

        self.red_ghost_instance.draw()
        self.blue_ghost_instance.draw()
        self.orange_ghost_instance.draw()
        self.pink_ghost_instance.draw()

    def deactivate_eat_mode(self):
        # Code to deactivate eat mode
        self.red_ghost_instance.edible = False
        self.blue_ghost_instance.edible = False
        self.orange_ghost_instance.edible = False
        self.pink_ghost_instance.edible = False

        self.red_ghost_instance.draw()
        self.blue_ghost_instance.draw()
        self.orange_ghost_instance.draw()
        self.pink_ghost_instance.draw()

    def check_collision_between_ghosts_and_pacman(self):
        for ghost in self.ghosts:
            if ghost.rect.colliderect(self.pacman.rect):
                if ghost.edible:
                    ghost.stop()
                    ghost.die()
                elif not ghost.dead:
                    # Game over
                    if self.pacman.die():
                        self.red_ghost_instance.stop()
                        self.blue_ghost_instance.stop()
                        self.orange_ghost_instance.stop()
                        self.pink_ghost_instance.stop()
                        self.game_over = True
                        self.end.render(False)
                        return 
                    self.pacman.reset()
                    self.red_ghost_instance.reset()
                    self.blue_ghost_instance.reset()
                    self.orange_ghost_instance.reset()
                    self.pink_ghost_instance.reset()

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    game = Game(screen)
    pygame.quit()
    sys.exit()
