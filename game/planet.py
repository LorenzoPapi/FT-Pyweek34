from .utils import *

class Planet(RotatingSprite):
    def __init__(self):
        super().__init__(
            load_texture("red_planet.png"),
        )
        self.image = pygame.transform.scale2x(pygame.transform.scale2x(self.image))
        self.radius = self.image.get_width() / 2
        self.origin = (SCREEN_CENTERX, SCREEN_HEIGHT + self.radius / 2 + 400)
        self.rect = self.image.get_rect(center=self.origin)
        lst = sorted(os.listdir(asset_path("textures", "enemies")))
        self.walking_enemies = [load_texture("enemies", f) for f in lst if not f.startswith("f_")]
        self.flying_enemies = [load_texture("enemies", f) for f in lst if f.startswith("f_")]
        self.enemies = []
        self.enemyf = 100

    def generate_walking_enemy(self):
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
                angle = dir * radians(180 - randint(10, 40)),
                origin = self.origin,
                speed = -0.01,
                scale = scale
            )
            enemy.hp = 2
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
                speed = -0.02,
            )
            enemy.hp = 5
        self.enemies.append(enemy)
        self.enemyf = randint(40, 100)


    def move_planet(self, pressed):
        left = pressed[pygame.K_LEFT]
        right = pressed[pygame.K_RIGHT]
        if (left and not right):
            self.angle -= 0
        if (right and not left):
            self.angle += 0

    def update(self):
        blit_rotate_center(SCREEN, self.image, (self.rect.topleft), self.angle)
        if not game.paused:
            if (len(self.enemies) < 10 and self.enemyf == 0):
                self.generate_walking_enemy()

            if (self.enemyf > 0): self.enemyf -= 1
        
        for enemy in self.enemies:
            enemy.update()
            enemy.animate()
            if (enemy.hp and enemy.hp <= 0):
                self.enemies.remove(enemy)
        
            