import math
import pygame
from config import *

class PacMan:
    def __init__(self, screen, board):
        self.screen = screen
        self.board = board
        self.x, self.y = PACMAN_START_POS
        self.size = 40  # Size of Pac-Man (radius)
        self.color = (255, 255, 0)  # Yellow color for Pac-Man
        self.size_grid = 50  
        self.direction = None
        self.frame_count = 0
        self.changed_direction = None
        self.mouth_open_angle = 45  # Angle of the mouth opening (in degrees)
        self.lives = 3
        self.screen_pos = grid_to_screen(grid_pos=[self.x, self.y], tile_size=[self.size_grid, self.size_grid])
        self.rect = pygame.Rect(self.screen_pos, PACMAN_SIZE)
        
    def draw(self):
        # Load the Pac-Man image
        pacman_image = pygame.image.load('assets/images/pacman.png')
        pacman_image = pygame.transform.scale(pacman_image, (self.size, self.size))

        # Rotate the image based on the direction
        if self.direction is None or self.direction == (1, 0):  # Default to the right
            rotated_image = pacman_image
        elif self.direction == (-1, 0):  # Left
            rotated_image = pygame.transform.rotate(pacman_image, 180)
        elif self.direction == (0, -1):  # Down
            rotated_image = pygame.transform.rotate(pacman_image, 90)
        elif self.direction == (0, 1):  # Up
            rotated_image = pygame.transform.rotate(pacman_image, 270)

        # Calculate the screen position of Pac-Man
        screen_x = self.x * self.size_grid
        screen_y = self.y * self.size_grid

        # Draw the rotated image at the current position
        self.screen.blit(rotated_image, (screen_x, screen_y))

    def move(self):
        if self.direction:
            dx, dy = self.direction
            new_x = self.x + dx
            new_y = self.y + dy
            if self.board[new_y][new_x] == 0:
                self.x = new_x
                self.y = new_y
                self.screen_pos = grid_to_screen(grid_pos=[self.x, self.y], tile_size=[self.size_grid, self.size_grid])
                self.rect.topleft = self.screen_pos

    def set_direction(self, direction):
        self.direction = direction

    def stop(self):
        self.direction = None

    def reset(self):
        self.x, self.y = PACMAN_START_POS
        self.direction = None

    def die(self):

        if self.lives == 0:
            # Game over
            return True
        
        # Reduce the number of lives
        self.lives -= 1

        self.reset()