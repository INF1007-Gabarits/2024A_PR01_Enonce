import pygame
from config import *
import random

class Ghost:
    def __init__(self, pos, img, maze, screen):
        self.pos = list(pos)  # Position en pixels
        self.speed = SPEED  # Vitesse en pixels par frame
        self.img = img  # Image du fantôme
        self.direction = Direction.UP  # Direction initiale
        self.dead = False  # État du fantôme
        self.maze = maze  # Labyrinthe
        self.rect = pygame.Rect(self.pos, GHOST_SIZE)  # Crée un rectangle pour le fantôme
        self.screen = screen
        self.death_timer = 0
        self.edible = False
        self.edible_img = pygame.transform.scale(pygame.image.load('assets/images/powerup.png'), GHOST_SIZE)
        self.dead_img = pygame.transform.scale(pygame.image.load('assets/images/dead.png'), GHOST_SIZE)   # Image du fantôme quand il est mort

    def draw(self):

        if not self.dead and not self.edible:
            self.screen.blit(self.img, self.pos)
        elif not self.dead and self.edible:
            self.screen.blit(self.edible_img, self.pos)
        else:
            self.screen.blit(self.dead_img, self.pos)

    def move(self):
        if not self.dead:
            future_x = self.pos[0] + self.direction[0] * self.speed
            future_y = self.pos[1] + self.direction[1] * self.speed

            future_rect = pygame.Rect(future_x, future_y, GHOST_SIZE[0], GHOST_SIZE[1])

            if self.check_collision(future_rect) is False:
                self.pos[0] = future_x
                self.pos[1] = future_y
                self.rect.topleft = (future_x, future_y)
            else:
                self.change_direction()

        # Gérer le cas où le fantôme est "mort" avec un timer pour sa résurrection
        elif self.death_timer > 0:
            self.death_timer -= 1

            # Une fois le timer expiré, réinitialiser la position du fantôme et son état
            if self.death_timer == 0:
                # Choisissez une position aléatoire pour réinitialiser le fantôme
                self.pos = random.choice(RANDOM_POS)
                self.dead = False
                self.direction = Direction.UP


    def check_collision(self, rect):
        # Vérifier si le rectangle du fantôme touche un mur
        for x in range(int(rect.left / TILE_WIDTH), int(rect.right / TILE_WIDTH) + 1):
            for y in range(int(rect.top / TILE_HEIGHT), int(rect.bottom / TILE_HEIGHT) + 1):
                if 0 <= x < len(self.maze[0]) and 0 <= y < len(self.maze):
                    if self.maze[y][x] == 1: # Vérifier si le fantôme touche un mur
                        return True
        return False

    def die(self):
        self.dead = True
        self.death_timer = 65

    def change_direction(self):
        directions_possibles = [Direction.DOWN, Direction.LEFT, Direction.UP, Direction.RIGHT]
        random.shuffle(directions_possibles)

        for direction in directions_possibles:
            dx, dy = direction
            next_x = self.pos[0] + dx * self.speed
            next_y = self.pos[1] + dy * self.speed

            next_rect = pygame.Rect(next_x, next_y, GHOST_SIZE[0], GHOST_SIZE[1])

            if not self.check_collision(next_rect):
                self.direction = direction

                return  # Sortir de la méthode une fois la direction changée

    def stop(self):
        self.direction = Direction.STOP

    def reset(self):
        self.pos = random.choice(RANDOM_POS)
        self.dead = False
        self.direction = random.choice([Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN])
        self.death_timer = 0
        self.edible = False
