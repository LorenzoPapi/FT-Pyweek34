import math
import pygame
from game.player import *
from game.utils import *

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

while running:
    game_window.fill('Black')

    planet.update_planet()
    player.update_player()

    key_handler()
    event_handler()
    pygame.display.update()
    clock.tick(60)
    