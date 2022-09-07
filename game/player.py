from .utils import *
from .planet import Planet

class Player(SuperSprite):
    def __init__(self):
        super().__init__(
            pygame.image.load(asset_path("textures", "player.png")),
            pygame.image.load(asset_path("textures", "walking_player.png")),
        )
        self.planet : Planet = Planet()
        self.ground_y = self.planet.rect.top
        self.origin = (game_window.get_width() / 2, self.planet.rect.top - self.image.get_size()[1]/2)
        self.rect = self.image.get_rect(center=self.origin)
        self.jumping = False
        self.total_jumps = 10
        self.jump_count = 0
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
            self.dir = -1
        elif (right and not left and self.dir == -1):
            self.dir = 1
        
        self.orig_image = self.sprites[self.index % len(self.sprites)]

        if pressed[pygame.K_SPACE]:
            if not self.jumping:
                self.jumping = self.rect.bottom >= self.ground_y
                self.jump_count = self.total_jumps
        elif self.jumping and self.jump_count > 0:
            self.jump_count = 0

    def update_player(self):
        if self.jumping:
            if self.jump_count >= -(2 * self.total_jumps):
                friction = 0.8 if self.jump_count > 0 else 0.4
                self.rect.bottom -= self.jump_count * abs(self.jump_count) * 0.5 * friction
                self.jump_count -= 1
            else:
                self.jump_count = self.total_jumps
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
        self.planet.update()
        self.draw()
    
    def shoot(self):
        self.bullets.append(SuperSprite(
            pygame.image.load(asset_path("textures", "projectile.png")),
            start_pos = (self.planet.radius + self.rect.size[0], self.planet.radius + self.rect.size[1] / 2 - self.rect.bottom + self.ground_y-10),
            dir = self.dir,
            angle = radians(self.dir * 2),
            origin = self.planet.origin,
            speed = 0.04
        ))
        self.bulletf = 10

