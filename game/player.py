import pygame
from .utils import *
from .planet import Planet

class Player(SuperSprite):
    def __init__(self):
        super().__init__(pygame.image.load(asset_path("textures", "player.png")))
        self.sprites = [
            self.orig_image,
            pygame.image.load(asset_path("textures", "walking_player.png")),
        ]
        
        self.planet : Planet = Planet()
        self.ground_y = self.planet.rect.topleft[1] - self.image.get_size()[1]
        self.rect = self.image.get_rect(center=(game_window.get_width() / 2, self.ground_y))
        
        self.gravity_y = 7
        self.friction = 1
        self.frames = 0
        self.jumpf = 0
        self.bulletf = 0
        self.dir = -1
        self.moving = False
        self.index = 0
        self.bullets = []
    
    def _flip_images(self):
        old_sprites = self.sprites.copy()
        self.sprites.clear()
        for s in old_sprites:
            self.sprites.append(pygame.transform.flip(s, True, False))

    def key_handler(self, event):
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_x):
            if (self.frames >= (self.bulletf + 10) or self.bulletf == 0):
                self.shoot()

    def move_player(self, pressed):
        self.planet.move_planet(pressed)
        right = pressed[pygame.K_RIGHT]
        left = pressed[pygame.K_LEFT]
        if (left ^ right):
            self.moving = True
        else:
            self.moving = False
            self.index = 0

        if (left and not right and self.dir != 1):
            if (self.dir != -1):
                pass 
            self._flip_images()
            self.dir = 1
        elif (right and not left and self.dir != 0):
            if (self.dir != -1): self._flip_images()
            self.dir = 0
        
        if self.index >= len(self.sprites):
            self.index = 0
        self.orig_image = self.sprites[self.index]
        
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
            bullet.rect = bullet.image.get_rect(center=(self.planet.center[0] + (bullet.start_pos[0]) * math.sin(bullet.angle), self.planet.center[1] - (bullet.start_pos[1]) * math.cos(bullet.angle)))
            bullet.update()
            bullet.angle += (1 if obj["dir"] != 1 else -1) * 0.04
            if (isOutsideSurface(game_window, bullet.rect.topleft)):
                self.bullets.remove(obj)

        for enemy in self.planet.enemies:
            if pygame.sprite.collide_rect(enemy, self):
                pass#exit()
            for bullet in self.bullets:
                if pygame.sprite.collide_rect(enemy, bullet["sprite"]):
                    self.planet.enemies.remove(enemy)
                    self.bullets.remove(bullet)

        if ((self.frames % 10 == 0) and self.moving):
            self.index += 1
            print(self.index)

        self.frames += 1
        self.move_player(pygame.key.get_pressed())
        self.planet.update_planet()
        self.update()
    
    def shoot(self):
        bullet = SuperSprite(pygame.image.load(asset_path("textures", "projectile.png")))
        bullet.start_pos = (self.planet.radius + self.rect.size[0], self.planet.radius + self.rect.size[1] / 2 - self.rect.y + self.ground_y)
        self.bullets.append({"sprite": bullet, "dir": self.dir})
        self.bulletf = self.frames

