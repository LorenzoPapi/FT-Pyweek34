import pygame
from sys import exit

pygame.init()

colors = {"RED": (255, 64, 64), "WHITE": (255, 255, 255)}

window = pygame.display.set_mode((900, 900))
caption = pygame.display.set_caption('hello')
clock = pygame.time.Clock()

planet = pygame.Rect(-315, 550, 1500, 1500)
player = pygame.Rect(415, 450, 50, 100)

bullets = []
game_true = True

def generateBullet(size = 50):
    bullet_obj = {"rect": pygame.Rect(player.x, player.y, size, size), "gravity": 7}
    bullets.append(bullet_obj)
    return bullet_obj

while True:
    window.fill('Black')
    pygame.draw.ellipse(window, colors["RED"], planet)
    pygame.draw.rect(window, colors["WHITE"], player)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                new_bullet = generateBullet()

    for obj in bullets:
        pygame.draw.rect(window, colors["RED"], obj.rect)
        obj.rect.x += obj.gravity

    pygame.display.flip()
    clock.tick(60)

