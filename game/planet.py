from .utils import *

class Planet(SuperSprite):
    def __init__(self):
        super().__init__(
            pygame.image.load(asset_path("textures", "red_planet.png")),
        )
        self.radius = self.image.get_size()[0] / 2
        self.origin = (game_window.get_width() / 2, game_window.get_height() + self.radius / 2 + 50)
        self.rect = self.image.get_rect(center=self.origin)
        self.enemy_sprites = [pygame.image.load(asset_path("textures", "enemies", f)) for f in os.listdir(asset_path("textures", "enemies"))]
        self.enemies = []
        self.enemyf = 100
        self._oldA = self.angle

    def generate_enemy(self):
        scale = 1.5
        enemy_img : pygame.Surface = self.enemy_sprites[randint(0,len(self.enemy_sprites) - 1)]
        dir = 1 if random() < 0.5 else -1
        self.enemies.append(SuperSprite(
            enemy_img,
            start_pos = (self.radius + enemy_img.get_size()[0] / 2 * scale, self.radius + enemy_img.get_size()[1] / 2  * scale),
            dir = dir,
            angle = dir * radians(180 - randint(10, 40)),
            origin = self.origin,
            speed = -0.01,
            scale = scale
        ))
        self.enemyf = randint(40, 100)

    def move_planet(self, pressed):
        left = pressed[pygame.K_LEFT]
        right = pressed[pygame.K_RIGHT]
        if (left and not right):
            self.angle -= 0.03
        if (right and not left):
            self.angle += 0.03
        if (self._oldA != self.angle):
            self.image, self.rect = rot_center(self.orig_image, degrees(self.angle), self.origin)
        self._oldA = self.angle

    def update(self):
        game_window.blit(self.image, self.rect)
        if (len(self.enemies) < 10 and self.enemyf == 0):
            self.generate_enemy()

        for enemy in self.enemies:
            enemy.update()
        
        if (self.enemyf > 0): self.enemyf -= 1