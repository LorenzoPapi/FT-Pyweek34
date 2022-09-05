import pygame
import os

def clamp(v, maxv, minv):
    return min(max(v, minv), maxv)

class Player(pygame.sprite.Sprite):
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.image = pygame.image.load(os.path.join("assets", "textures", "player.png")).convert_alpha()
        self.rect = self.image.get_rect(center=(self.window.get_width() / 2, 450))
        self.gravity_y = 0
        self.friction = 1
        self.frames = 0
        self.jumpf = 0

    def move_player(self, event):
        key = event.key
        if (key == pygame.K_LEFT):
            pass    
        if (key == pygame.K_RIGHT):
            pass
        if (key == pygame.K_SPACE and self.rect.y >= 450):
            self.gravity_y = -7
            self.friction = 1
            self.jumpf = self.frames

    def update_player(self):
        self.window.blit(self.image, self.rect)
        self.rect.y += self.gravity_y * self.friction
        self.rect.y = clamp(self.rect.y, 450, 0)
        if (self.frames == (self.jumpf + 10)):
            self.gravity_y = 7
            self.friction = 0.5
            self.jumpf = 0
        self.frames += 1
