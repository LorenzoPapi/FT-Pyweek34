from .utils import *

class Planet(RotatingSprite):
    def __init__(self):
        self.initialize_planet()

    def generate_enemy(self):
        enemy = None
        if (random() < 0.7):
            scale = 2
            enemy_index = randint(0,len(self.walking_enemies) / 2 - 1) * 2
            image = self.walking_enemies[enemy_index]
            dir = 1 if random() < 0.5 else -1
            enemy = RotatingSprite(
                image, self.walking_enemies[enemy_index + 1],
                start_pos = (self.radius + image.get_width() / 2 * scale, self.radius + image.get_height() / 2  * scale),
                dir = dir,
                angle = radians(180 - randint(10, 40)),
                origin = self.origin,
                speed = -0.02,
                scale = scale
            )
            enemy.maxhp = enemy.hp = 3
        else:
            enemy_index = randint(0,len(self.flying_enemies) / 2 - 1) * 2
            image = self.flying_enemies[enemy_index]
            dir = 1 if random() < 0.5 else -1
            enemy = DoubleSinSprite(
                image, self.flying_enemies[enemy_index + 1],
                start_pos = (700, 300),
                dir = dir,
                angle = dir * radians(90),
                origin = (SCREEN_CENTERX, self.rect.top + image.get_height() - randint(20, 50)),
                speed = -0.04,
            )
            enemy.maxhp = enemy.hp = 5
        self.enemies.append(enemy)
        self.enemyf = randint(ceil(60 - game.score / 15) - 1, 120)


    def move_planet(self, pressed):
        left = pressed[pygame.K_LEFT]
        right = pressed[pygame.K_RIGHT]
        if (left and not right):
            self.angle -= self.speed
        if (right and not left):
            self.angle += self.speed

    def initialize_planet(self):
        self.speed = 5
        if not hasattr(self, "cache"):
            self.cache = [(pygame.transform.rotate(TEXTURES["red_planet.png"], a)).convert_alpha() for a in range(0, 360, self.speed)]
            self.walking_enemies = [t for i, t in TEXTURES.items() if i.startswith("enemies") and i.find("f_") == -1]
            self.flying_enemies = [t for i, t in TEXTURES.items() if i.startswith("enemies") and i.find("f_") != -1]
        super().__init__(
            pygame.transform.scale2x(self.cache[0]),
            speed = 5
        )
        self.radius = self.image.get_width() / 2
        self.origin = (SCREEN_CENTERX, SCREEN_HEIGHT + self.radius / 2 - 50)
        self.rect = self.image.get_rect(center=self.origin)
        self.enemies = []
        self.enemyf = 30

    def update(self):
        rotated = pygame.transform.scale2x(self.cache[round(self.angle / self.speed) % len(self.cache)])
        SCREEN.blit(rotated, rotated.get_rect(center = (self.image.get_rect(center = self.origin).center)))
        if not game.paused:
            if (len(self.enemies) < 10 and self.enemyf == 0): self.generate_enemy()
            if (self.enemyf > 0): self.enemyf -= 1
        
        for enemy in self.enemies:
            if enemy.hp <= 0:
                SOUNDS["score_up.mp3"].play()
                game.score += 20 if enemy.maxhp == 5 else 10
                if game.player.lives < 3 and game.score >= 150 and game.score % 150 <= 10:
                    game.player.lives += 1
                self.enemies.remove(enemy)
            else:
                if game.player.moving and enemy.maxhp != 5 and not is_outside_surface(SCREEN, enemy.rect.topleft):
                    enemy.mul = 1.5 if (enemy.angle < pi and game.player.dir == 1) or (enemy.angle > pi and game.player.dir == -1) else 0.5
                else:
                    enemy.mul = 1
                pygame.draw.rect(SCREEN, "GREEN", (enemy.rect.left, enemy.rect.top, (enemy.image.get_width()) * enemy.hp / enemy.maxhp, 10))
                pygame.draw.rect(SCREEN, "WHITE", (enemy.rect.left, enemy.rect.top, enemy.image.get_width(), 10), 2)
                enemy.update()
                enemy.animate()
                
            