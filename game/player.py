import pygame
import os
from .utils import *

class Player(SuperSprite):
    def __init__(self, window, planet):
        super().__init__(window, pygame.image.load(os.path.join("assets", "textures", "player_2.png")).convert_alpha())
        self.ground_y = planet.rect.topleft[1] - self.image.get_size()[1]
        self.rect = self.image.get_rect(center=(self.window.get_width() / 2, self.ground_y))
        self.gravity_y = 7
        self.friction = 1
        self.frames = 0
        self.jumpf = 0
        self.dir = 0

    def move_player(self, pressed):
        #if (pressed[pygame.K_LEFT] and self.dir != 1):
        #    self.dir = 1
        #    self.image = pygame.transform.flip(self.image.copy(), True, False)
        #elif (pressed[pygame.K_RIGHT] and self.dir != 0):
        #    self.dir = 0
        #    self.image = pygame.transform.flip(self.image.copy(), True, False)
        if (pressed[pygame.K_SPACE] and self.rect.y >= self.ground_y and self.gravity_y == 7):
            self.gravity_y = -7
            self.friction = 1
            self.jumpf = self.frames
        elif (not pressed[pygame.K_SPACE] and self.gravity_y == -7):
            self.gravity_y = 7
            self.friction = 1.1
            self.jumpf = 0

    def update_player(self):
        self.rect.y += self.gravity_y * self.friction
        self.rect.y = clamp(self.rect.y, self.ground_y, 0)
        if (self.frames == (self.jumpf + 20)):
            self.gravity_y = 7
            self.friction = 1.1
            self.jumpf = 0
        self.frames += 1
        self.update()
