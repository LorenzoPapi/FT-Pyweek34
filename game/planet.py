import pygame
from random import randint
from .utils import *

class Planet(SuperSprite):
    def __init__(self):
        super().__init__(pygame.image.load(asset_path("textures", "red_planet.png")))
        self.radius = self.image.get_size()[0] / 2
        self.center = (game_window.get_width() / 2, game_window.get_height() + self.radius / 2 + 50)
        self.rect = pygame.rect.Rect(self.center[0] - self.radius, self.center[1] - self.radius, self.radius * 2, self.radius * 2)
        self.enemy_sprites = [
            'apple.png',
            'macaroni.png',
            'pizza.png'
        ]
        for i in range(0, len(self.enemy_sprites)):
            self.enemy_sprites[i] = pygame.image.load(asset_path("textures", "enemies", self.enemy_sprites[i]))
        
        self.enemies = []
        self.frames = 0

    def generate_enemy(self):
        enemy_img : pygame.Surface = self.enemy_sprites[randint(0,len(self.enemy_sprites) - 1)]
        enemy = SuperSprite(enemy_img)
        enemy.start_pos = (self.radius + enemy_img.get_size()[0] / 2, self.radius + enemy_img.get_size()[1] / 2)
        enemy.angle = math.radians(randint(10, 40))
        self.enemies.append(enemy)

    def move_planet(self, pressed):
        left = pressed[pygame.K_LEFT]
        right = pressed[pygame.K_RIGHT]
        if (left and not right):
            self.angle -= 0.03
        if (right and not left):
            self.angle += 0.03

    def update_planet(self):
        game_window.blit(self.image, self.rect)
        self.image, self.rect = rot_center(self.orig_image, math.degrees(self.angle), self.center)
        
        if (len(self.enemies) < 6 and self.frames % 100 == 0):
            self.generate_enemy()

        for enemy in self.enemies:
            enemy : SuperSprite = enemy
            enemy.rect = enemy.image.get_rect(center=(self.center[0] + (enemy.start_pos[0]) * math.sin(enemy.angle), self.center[1] - (enemy.start_pos[1]) * math.cos(enemy.angle)))
            enemy.update()
            enemy.angle -= 0.005
        self.frames += 1