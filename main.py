import math
import pygame
from game.player import Player
from sys import exit

pygame.init()
window = pygame.display.set_mode((1200, 900))
colors = {"RED": (255, 64, 64), "WHITE": (255, 255, 255)}
player = Player(window)

class Planet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.rotozoom(pygame.image.load('assets/textures/red_planet_2.png').convert_alpha(), 0, 1)
        self.size = self.image.get_size()
        self.center = (window.get_width() / 2, window.get_height() + 300)
        self.rect = pygame.rect.Rect((self.center[0]-self.size[0]/2, self.center[1]-self.size[1]/2), self.size)
planet = Planet()

caption = pygame.display.set_caption('hello')
clock = pygame.time.Clock()
bullets = []

def event_handler():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                generate_bullet()
            player.move_player(event)

def generate_bullet(size = 16):
    bullet = pygame.sprite.Sprite()
    bullet.image = pygame.transform.rotozoom(pygame.image.load("assets/textures/projectile.png").convert_alpha(), 0, 2.5)
    bullet.orig_image = bullet.image
    bullet.rect = bullet.image.get_rect(center=player.rect.center)
    bullets.append({"sprite": bullet, "angle": 0, "start": bullet.rect.center})
    return bullet

while 1:
    window.fill('Black')
    window.blit(planet.image, planet.rect)
    player.update_player()
    event_handler()

    for obj in bullets:
        bullet = obj["sprite"]
        window.blit(bullet.image, (bullet.rect.center))
        bullet.image = pygame.transform.rotozoom(bullet.orig_image, math.degrees(-obj["angle"]), 1)
        bullet.rect = bullet.image.get_rect(center=(planet.center[0] + (obj["start"][0]) * math.sin(obj["angle"]), planet.center[1] - 300 - (obj["start"][1]) * math.cos(obj["angle"])))
        
        obj["angle"] += 0.025

    pygame.display.flip()
    clock.tick(60)
