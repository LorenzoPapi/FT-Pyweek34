from turtle import update
import pygame
from game.player import Player
from sys import exit

pygame.init()
player = Player()

colors = {"RED": (255, 64, 64), "WHITE": (255, 255, 255)}

window = pygame.display.set_mode((900, 900))
caption = pygame.display.set_caption('hello')
clock = pygame.time.Clock()

planet_img = pygame.image.load('FT-Pyweek34/assets/textures/red_planet.png').convert_alpha()
planet_img = pygame.transform.rotozoom(planet_img, 0, 1.5)
projectile_img = pygame.image.load('FT-Pyweek34/assets/textures/projectile.png').convert_alpha()
projectile_img = pygame.transform.rotozoom(projectile_img, 0, 2.5)
planet = planet_img.get_rect(center = (450, 1450))
bullets = []
game_true = True

def generateBullet(size = 50):
    bullet_obj = {"rect": projectile_img.get_rect(topleft = (player.rect.x, player.rect.y)), "gravity": 7}
    bullets.append(bullet_obj)
    return bullet_obj

while True:
    window.fill('Black')
    window.blit(planet_img, planet)
    pygame.draw.rect(window, colors["WHITE"], player.rect)
    player.update_player()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                new_bullet = generateBullet()
        elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            player.move_player(event)

    for obj in bullets:
        window.blit(projectile_img, obj["rect"])
        obj["rect"].x += obj["gravity"]

    pygame.display.flip()
    clock.tick(60)

