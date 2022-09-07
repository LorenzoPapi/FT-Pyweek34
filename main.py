from game.utils import *
from game.player import Player

pygame.init()

player = Player()

caption = pygame.display.set_caption('Catch the Ketchup!')
title_screen = pygame.image.load('assets/textures/home_screen_final.gif')
clock = pygame.time.Clock()
running = 0

def event_handler():
    global running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = 0
            pygame.quit()
        elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            player.key_handler(event)
        if not running:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                running = 1

while running:
    if running:
        game_window.fill('Black')
        player.update_player()

        pygame.display.update()
        event_handler()
        clock.tick(60)
    else:
        game_window.blit(title_screen, (0,0))
        event_handler()

    