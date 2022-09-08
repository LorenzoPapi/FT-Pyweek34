from .utils import *
from .planet import Planet

class Player(RotatingSprite):
    def __init__(self):
        self.init_player()
    
    def key_handler(self, event):
        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_x and self.bulletf == 0 and not game.paused):
                self.shoot()
            elif (event.key == pygame.K_p):
                game.paused = not game.paused
                game.fader.image.set_alpha(127 if game.paused else 0)

    def move_player(self, pressed):
        if not game.paused:
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
        if not self.game_over:
            if self.jumping and not game.paused:
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
                if (is_outside_surface(SCREEN, bullet.rect.topleft)):
                    self.bullets.remove(bullet)

            for enemy in self.planet.enemies:
                if pygame.sprite.collide_rect(enemy, self):
                    self.game_over = True
                    game.fader.start(1, False)
                    self.image.set_alpha(0)
                for bullet in self.bullets:
                    if pygame.sprite.collide_rect(enemy, bullet):
                        enemy.hp -= 1
                        self.bullets.remove(bullet)

            if ((self.animf == 0) and self.moving):
                self.index += 1
                self.animf = 10

            if (self.animf > 0): self.animf -= 1
            if (self.bulletf > 0): self.bulletf -= 1

            self.move_player(pygame.key.get_pressed())
            self.planet.update()
            self.draw()
        elif self.game_over and game.fader.has_ended():
            game.fader.start(1)
            self.game_over = False
            game.game_start = False
            self.init_player()
    
    def shoot(self):
        self.bullets.append(StraightLineSprite(
            self.proj_tex,
            start_pos = (self.planet.radius + self.rect.size[0] + 10, self.planet.radius + self.rect.size[1] / 2 - self.rect.bottom + self.ground_y - 10),
            dir = self.dir,
            origin = self.planet.origin,
            speed = self.dir * 40
        ))
        self.bulletf = 5

    def init_player(self):
        super().__init__(
            load_texture("player0.png"),
            load_texture("player1.png"),
        )
        self.proj_tex = load_texture("projectile.png")
        self.planet : Planet = Planet()
        self.ground_y = self.planet.rect.top
        self.origin = (SCREEN_CENTERX, self.ground_y - self.image.get_height()/2)
        self.rect = self.image.get_rect(center=self.origin)
        self.jumping = False
        self.total_jumps = 10
        self.jump_count = 0
        self.animf = 0
        self.bulletf = 0
        self.moving = False
        self.index = 0
        self.game_over = False
        self.bullets = []

game.player = Player()