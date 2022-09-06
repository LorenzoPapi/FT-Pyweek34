import math
import pygame
from game.player import *
from game.utils import *
from random import randint

pygame.init()
colors = {"RED": (255, 64, 64), "WHITE": (255, 255, 255)}

class Planet(SuperSprite):
    def __init__(self, window):
        super().__init__(window, pygame.image.load('assets/textures/red_planet_2.png').convert_alpha())
        self.size = self.image.get_size()
        self.center = (self.window.get_width() / 2, self.window.get_height() + 300)
        self.rect = pygame.rect.Rect((self.center[0]-self.size[0]/2, self.center[1]-self.size[1]/2), self.size)

    def move_planet(self, pressed):
        if (pressed[pygame.K_LEFT]):
            self.angle -= 0.025
        if (pressed[pygame.K_RIGHT]):
            self.angle += 0.025

    def update_planet(self):
        self.window.blit(self.image, self.rect)
        self.image, self.rect = rot_center(self.orig_image, math.degrees(self.angle), self.center)

planet = Planet(window)
player = Player(window, planet)
#enemy = Enemy(window, planet, randint(0,3))

caption = pygame.display.set_caption('Catch the Ketchup!')
clock = pygame.time.Clock()
bullets = []
enemies = []
running = True

def key_handler():
    pressed = pygame.key.get_pressed()
    planet.move_planet(pressed)
    player.move_player(pressed)

def event_handler():
    global running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = None
            pygame.quit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_x:
            generate_bullet()


def generate_bullet(size=16):
    
    bullet = SuperSprite(window, pygame.image.load('assets/textures/projectile.png').convert_alpha())
    bullets.append({"sprite": bullet, "angle": 0, "start": (planet.size[0]/2 + player.rect.size[0], planet.size[1]/2 + player.rect.size[1] / 2 - player.rect.y + player.ground_y)}) #(planet.size[0]/2 + player.rect.size[0], -planet.size[1]/2 + player.rect.bottom)
    return bullet

enemies = []
apple_enemy = pygame.image.load('assets/textures/apple.png')
macaroni_enemy = pygame.image.load('assets/textures/macaroni.png')
pizza_enemy = pygame.image.load('assets/textures/pizza_enemy.png')
enemy_sprites = [apple_enemy, macaroni_enemy, pizza_enemy]
index = enemy_sprites[randint(0,2)]

def generate_enemy(size=40):
    index = enemy_sprites[randint(0,2)]
    enemy = SuperSprite(window, index.convert_alpha())
    enemies.append({"sprite": enemy, "angle": 0.4, "start": (planet.size[0]/2 + player.rect.size[0], planet.size[1]/2 + player.rect.size[1] / 2 - player.rect.y + player.ground_y)}) #(planet.size[0]/2 + player.rect.size[0], -planet.size[1]/2 + player.rect.bottom)
    return enemy
generate_enemy()
while running:
    window.fill('Black')
    event_handler()
    for obj in bullets:
        bullet = obj["sprite"]
        bullet.image = pygame.transform.rotozoom(bullet.orig_image, math.degrees(-obj["angle"]), 1)
        bullet.rect = bullet.image.get_rect(center=(planet.center[0] + (obj["start"][0]) * math.sin(obj["angle"]), planet.center[1] - (obj["start"][1]) * math.cos(obj["angle"])))
        print(bullet.rect)
        window.blit(bullet.image, bullet.rect) 
        pygame.draw.rect(window, (255, 64, 255), bullet.rect, 2)
        obj["angle"] += 0.01
        if (isOutsideSurface(window, bullet.rect.topleft)):
            bullets.remove(obj)
    for obj in enemies:
        enemy = obj["sprite"]
        enemy.image = pygame.transform.rotozoom(enemy.orig_image, math.degrees(-obj["angle"]), 1)
        enemy.rect = enemy.image.get_rect(center=(planet.center[0] + (obj["start"][0]) * math.sin(obj["angle"]), planet.center[1] - (obj["start"][1]) * math.cos(obj["angle"])))
        window.blit(enemy.image, enemy.rect) 
        obj["angle"] += 0.005
        if pygame.sprite.collide_rect(enemy, player):
            print("a")
            pygame.quit()
        for obj2 in bullets:
            if pygame.sprite.collide_rect(enemy,obj2["sprite"]):
                enemies.remove(obj)
                bullets.remove(obj2)

    
        #if pygame.sprite.collide_rect(enemy,bullet)

    planet.update_planet()
    player.update_player()

    pygame.display.flip()
    key_handler()
    clock.tick(60)
    