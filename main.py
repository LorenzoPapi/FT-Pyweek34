import pygame
from game.utils import *
from game.player import Player

pygame.init()

player = Player()

caption = pygame.display.set_caption('Catch the Ketchup!')
clock = pygame.time.Clock()
running = 1

def event_handler():
    global running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = 0
            pygame.quit()
        elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            player.key_handler(event)

while running:
    game_window.fill('Black')
    player.update_player()

    pygame.display.update()
    event_handler()
    clock.tick(60)
    