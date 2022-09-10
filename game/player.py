from .utils import *
from .planet import Planet


class Player(RotatingSprite):
    def __init__(self):
        self.init_player()

    def key_handler(self, event):
        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_x and self.bulletf == 0 and not game.paused):
                self.shoot()
            if (self.game_over and event.key == pygame.K_SPACE):
                self.init_player()
                game.paused = False

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
                if (self.animf > 0):
                    self.animf = 0

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
            self.planet.update()
            self.draw()

            for bullet in self.bullets:
                bullet.update()
                if (is_outside_surface(SCREEN, bullet.rect.topleft)):
                    self.bullets.remove(bullet)

            if not game.paused:
                if self.jumping:
                    if self.jump_count >= -(2 * self.total_jumps):
                        friction = 1 if self.jump_count > 0 else 0.4
                        self.rect.bottom -= self.jump_count * abs(self.jump_count) * 0.5 * friction
                        self.jump_count -= 1
                    else:
                        self.jump_count = self.total_jumps
                        self.jumping = False
                self.rect.bottom = clamp(self.rect.bottom, self.ground_y, 0)

                for enemy in self.planet.enemies:
                    for bullet in self.bullets:
                        if pygame.sprite.collide_rect(enemy, bullet):
                            enemy.hp -= 1
                            self.bullets.remove(bullet)
                    if pygame.sprite.collide_rect(enemy, self):
                        SOUNDS["hit.mp3"].play()
                        self.lives -= 1
                        self.planet.enemies.remove(enemy)
                        if self.lives == 0:
                            enemy.hp = 0
                            self.game_over = True
                            SOUNDS["battle.mp3"].stop()
                            SOUNDS["game_over.mp3"].play()

                if self.animf == 0 and self.moving:
                    self.index += 1
                    self.animf = 5

                if (self.animf > 0):
                    self.animf -= 1
                if (self.bulletf > 0):
                    self.bulletf -= 1

                self.move_player(pygame.key.get_pressed())
            else:
                score = FONTS["Cave-Story"].render("Paused", False, (255, 0, 0))
                SCREEN.blit(score, (S_INFO["cx"] - score.get_width() / 2, S_INFO["cy"] - score.get_height() / 2 - self.image.get_height()))
        else:
            game.paused = True
            draw_middle("game_over.png")


    def shoot(self):
        self.bullets.append(StraightLineSprite(
            TEXTURES["projectile.png"],
            start_pos=(self.planet.radius + self.rect.size[0] + 10, self.planet.radius + self.rect.size[1] / 2 - self.rect.bottom + self.ground_y - 10),
            dir=self.dir,
            origin=self.planet.origin,
            speed=self.dir * 40
        ))
        self.bulletf = 3
        SOUNDS["shoot.mp3"].set_volume(0.3)
        SOUNDS["shoot.mp3"].play()

    def init_player(self):
        super().__init__(
            TEXTURES["player0.png"],
            TEXTURES["player1.png"],
        )
        if hasattr(self, "planet"):
            self.planet.initialize_planet()
            SOUNDS["battle.mp3"].play(loops=-1)
        else:
            self.planet: Planet = Planet()
        self.ground_y = self.planet.rect.top
        self.origin = (S_INFO["cx"], self.ground_y - self.image.get_height()/2)
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
        game.score = 0
        self.lives = 1


game.player = Player()
