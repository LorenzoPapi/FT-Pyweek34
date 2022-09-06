import math
import pygame
from game.player import *
from game.utils import *
from random import randint

pygame.init()

class Planet(SuperSprite):
    def __init__(self):
        super().__init__(pygame.image.load(asset_path("texture", "red_planet_2.png")))
        self.radius = self.image.get_size()[0] / 2
        self.center = (game_window.get_width() / 2, game_window.get_height() + self.radius / 2 + 50)
        self.rect = pygame.rect.Rect(self.center[0] - self.radius, self.center[1] - self.radius, self.radius * 2, self.radius * 2)

    def move_planet(self, pressed):
        if (pressed[pygame.K_LEFT]):
            self.angle -= 0.03
        if (pressed[pygame.K_RIGHT]):
            self.angle += 0.03

    def update_planet(self):
        game_window.blit(self.image, self.rect)
        self.image, self.rect = rot_center(self.orig_image, math.degrees(self.angle), self.center)

planet = Planet()
player = Player(planet)

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
        elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            player.key_handler(event)

enemies = []
apple_enemy = pygame.image.load('assets/textures/apple.png')
macaroni_enemy = pygame.image.load('assets/textures/macaroni.png')
pizza_enemy = pygame.image.load('assets/textures/pizza_enemy.png')
enemy_sprites = [apple_enemy, macaroni_enemy, pizza_enemy]
index = enemy_sprites[randint(0,2)]

def generate_enemy(size=40):
    index = enemy_sprites[randint(0,2)]
    enemy = SuperSprite(game_window, index.convert_alpha())
    enemies.append({"sprite": enemy, "angle": 0.4, "start": (planet.size[0]/2 + player.rect.size[0], planet.size[1]/2 + player.rect.size[1] / 2 - player.rect.y + player.ground_y)}) #(planet.size[0]/2 + player.rect.size[0], -planet.size[1]/2 + player.rect.bottom)
    return enemy
generate_enemy()
while running:
    game_window.fill('Black')
    for obj in enemies:
        enemy = obj["sprite"]
        enemy.image = pygame.transform.rotozoom(enemy.orig_image, math.degrees(-obj["angle"]), 1)
        enemy.rect = enemy.image.get_rect(center=(planet.center[0] + (obj["start"][0]) * math.sin(obj["angle"]), planet.center[1] - (obj["start"][1]) * math.cos(obj["angle"])))
        game_window.blit(enemy.image, enemy.rect) 
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

    key_handler()
    event_handler()
    pygame.display.update()
    clock.tick(60)
    