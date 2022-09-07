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
        self.ground_y = self.planet.rect.top
        self.origin = (game_window.get_width() / 2, self.ground_y - self.image.get_size()[1]/2)
        self.jumping = False
        self.totalJumps = 10
        self.jumpCount = 0
        self.animf = 0
        self.bulletf = 0
        self.moving = False
        self.index = 0
        self.bullets = []
    
    def key_handler(self, event):
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_x):
            if (self.bulletf == 0):
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
            if (self.animf > 0): self.animf = 0

        if (left and not right and self.dir == 1):
            flip_list(self.sprites)
            self.dir = -1
        elif (right and not left and self.dir == -1):
            flip_list(self.sprites)
            self.dir = 1
        
        self.orig_image = self.sprites[self.index % len(self.sprites)]

        if pressed[pygame.K_SPACE]:
            if not self.jumping:
                self.jumping = self.rect.bottom >= self.ground_y
                self.jumpCount = self.totalJumps
        elif self.jumping and self.jumpCount > 0:
                self.jumpCount = 0

    def update_player(self):
        if self.jumping:
            if self.jumpCount >= -(self.totalJumps + 1):
                self.rect.bottom -= self.jumpCount * abs(self.jumpCount) * 0.5
                self.jumpCount -= 1
            else:
                self.jumpCount = self.totalJumps
                self.jumping = False
        
        self.rect.bottom = clamp(self.rect.bottom, self.ground_y, 0)

        for bullet in self.bullets:
            bullet.update()
            if (isOutsideSurface(game_window, bullet.rect.topleft)):
                self.bullets.remove(bullet)

        for enemy in self.planet.enemies:
            if pygame.sprite.collide_rect(enemy, self):
                pass #exit()
            for bullet in self.bullets:
                if pygame.sprite.collide_rect(enemy, bullet):
                    self.planet.enemies.remove(enemy)
                    self.bullets.remove(bullet)

        if ((self.animf == 0) and self.moving):
            self.index += 1
            self.animf = 10

        if (self.animf > 0): self.animf -= 1
        if (self.bulletf > 0): self.bulletf -= 1

        self.move_player(pygame.key.get_pressed())
        self.planet.update_planet()
        self.update()
    
    def shoot(self):
        bullet = SuperSprite(pygame.image.load(asset_path("textures", "projectile.png")))
        bullet.start_pos = (self.planet.radius + self.rect.size[0], self.planet.radius + self.rect.size[1] / 2 - self.rect.bottom + self.ground_y + -10)
        bullet.dir = self.dir
        bullet.angle = math.radians(bullet.dir * 2.2)
        bullet.origin = self.planet.center
        bullet.speed = 0.04
        self.bullets.append(bullet)
        self.bulletf = 10

