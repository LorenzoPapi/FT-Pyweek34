from .utils import *

class Planet(RotatingSprite):
    def __init__(self):
        super().__init__(
            load_texture("red_planet.png"),
        )
        self.orig_image = pygame.transform.scale(self.orig_image, (1500, 1500))
        self.radius = self.image.get_width() / 2
        self.origin = (SCREEN_CENTERX, SCREEN_HEIGHT + self.radius / 2 - 100)
        self.rect = self.image.get_rect(center=self.origin)
        lst = sorted(os.listdir(asset_path("textures", "enemies")))
        self.walking_enemies = [load_texture("enemies", f) for f in lst if not f.startswith("f_")]
        self.flying_enemies = [load_texture("enemies", f) for f in lst if f.startswith("f_")]
        self.enemies = []
        self.enemyf = 100

    def generate_walking_enemy(self):
        enemy = None
        if (random() < 0.5):
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
        else:
            enemy_index = randint(0,len(self.flying_enemies) / 2 - 1) * 2
            image = self.flying_enemies[enemy_index]
            dir = 1 if random() < 0.5 else -1
            enemy = LineSprite(
                image, self.flying_enemies[enemy_index + 1],
                start_pos = (700, 200),
                dir = dir,
                angle = dir * radians(90),
                origin = (SCREEN_CENTERX, self.rect.top - image.get_height() / 2 - randint(0, 60)),
                speed = -0.06,
            )
        self.enemies.append(enemy)
        self.enemyf = randint(40, 100)


    def move_planet(self, pressed):
        left = pressed[pygame.K_LEFT]
        right = pressed[pygame.K_RIGHT]
        if (left and not right):
            self.angle -= 2
        if (right and not left):
            self.angle += 2

    def update(self):
        blit_rotate_center(SCREEN, self.image, (self.rect.topleft), self.angle)
        if (len(self.enemies) < 10 and self.enemyf == 0):
            self.generate_walking_enemy()

        for enemy in self.enemies:
            enemy.update()
            enemy.animate()
        
        if (self.enemyf > 0): self.enemyf -= 1