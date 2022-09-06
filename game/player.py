import pygame
import os
from .utils import *

class Player(SuperSprite):
    def __init__(self, planet):
        super().__init__(pygame.image.load(asset_path("texture", "player_2.png")))
        self.images = [
            self.orig_image,
            pygame.transform.flip(self.orig_image, True, False)
        ]
        
        self.planet = planet
        self.ground_y = planet.rect.topleft[1] - self.image.get_size()[1]
        self.rect = self.image.get_rect(center=(game_window.get_width() / 2, self.ground_y))
        
        self.gravity_y = 7
        self.friction = 1
        self.frames = 0
        self.jumpf = 0
        self.bulletf = 0
        self.dir = 0
        self.bullets = []
    
    def key_handler(self, event):
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_x):
            if (self.frames >= (self.bulletf + 10) or self.bulletf == 0):
                self.shoot()

    def move_player(self, pressed):
        self.orig_image = self.images[self.dir]
        if (pressed[pygame.K_LEFT] and not pressed[pygame.K_RIGHT] and self.dir != 1):
            self.dir = 1
        elif (pressed[pygame.K_RIGHT] and not pressed[pygame.K_LEFT] and self.dir != 0):
            self.dir = 0
        if (pressed[pygame.K_SPACE] and self.rect.y >= self.ground_y and self.gravity_y == 7):
            self._jump(False)
        elif (not pressed[pygame.K_SPACE] and self.gravity_y == -7):
            self._jump(True)

    def _jump(self, down):
        self.gravity_y = (1 if down else -1) * 7
        self.friction = 1.1 if down else 1
        self.jumpf = 0 if down else self.frames

    def update_player(self):
        self.rect.y = clamp(self.rect.y + self.gravity_y * self.friction, self.ground_y, 0)
        if (self.frames == (self.jumpf + 20)):
            self._jump(True)
        
        for obj in self.bullets:
            bullet : SuperSprite = obj["sprite"]
            bullet.rect = bullet.image.get_rect(center=(self.planet.center[0] + (obj["start"][0]) * math.sin(bullet.angle), self.planet.center[1] - (obj["start"][1]) * math.cos(bullet.angle)))
            bullet.update()
            bullet.angle += (1 if obj["dir"] == 0 else -1) * 0.04
            if (isOutsideSurface(game_window, bullet.rect.topleft)):
                self.bullets.remove(obj)

        self.frames += 1
        self.update()
    
    def shoot(self):
        bullet = SuperSprite(pygame.image.load(asset_path("texture", "projectile.png")))
        self.bullets.append({"sprite": bullet, "dir": self.dir, "start": (self.planet.radius + self.rect.size[0], self.planet.radius + self.rect.size[1] / 2 - self.rect.y + self.ground_y)})
        self.bulletf = self.frames

