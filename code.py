import pygame
from sys import exit

pygame.init()
window = pygame.display.set_mode((900, 900))
caption = pygame.display.set_caption('hello')
clock = pygame.time.Clock()

planet = pygame.Rect(-315, 550, 1500, 1500)
player = pygame.Rect(415, 450, 50, 100)

projectile = pygame.Rect(415, 450, 50, 50)
projectile2 = pygame.Rect(415, 450, 50, 50)
projectile3 = pygame.Rect(415, 450, 50, 50)

projectile_gravity = 7
projectile_move = False
projectile_list = []
game_true = True

while True:
    window.fill('Black')
    pygame.draw.ellipse(window, (255,64,64), planet)
    pygame.draw.rect(window, (255,64,64), projectile)
    pygame.draw.rect(window, 'White', player)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
        if event.key == pygame.K_SPACE:
            projectile.x += projectile_gravity

    pygame.display.flip()
    clock.tick(60)
    
