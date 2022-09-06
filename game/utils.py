import math
import pygame
from pygame.locals import *
import os

game_window = pygame.display.set_mode((1200, 900), DOUBLEBUF, 16)
# no work
game_speed = 1
#colors = {"RED": (255, 64, 64), "WHITE": (255, 255, 255)}

def change_game_speed(v):
    global game_speed
    game_speed = v

def clamp(v, maxv, minv):
    return min(max(v, minv), maxv)

def isOutsideSurface(surf : pygame.Surface, point):
    h, w = surf.get_height(), surf.get_width()
    return (point[0] < 0 or point[0] > w) or (point[1] < 0 or point[1] > h)

# https://stackoverflow.com/questions/4183208/how-do-i-rotate-an-image-around-its-center-using-pygame
def rot_center(image : pygame.Surface, angle, center):
    rotated = pygame.transform.rotate(image, angle)
    return rotated, rotated.get_rect(center = image.get_rect(center = center).center)

def asset_path(*argv):
    p = os.path.join(".", "assets")
    for f in argv:
        p = os.path.join(p, f)
    return p

class SuperSprite(pygame.sprite.Sprite):
    def __init__(self, image : pygame.Surface):
        super().__init__()
        self.start_pos = (0, 0)
        self.image = image.convert_alpha()
        self.rect = self.image.get_rect()
        self.angle = 0
        self.scale = 1
        self.orig_image = self.image
        self._oldS = self.scale
        self._oldA = self.angle
        self._oldOI = self.orig_image
    
    def update(self):
        self.angle *= game_speed
        if (self._oldS != self.scale or self._oldA != self.angle or self._oldOI != self.orig_image):
            self.image = pygame.transform.rotozoom(self.orig_image, math.degrees(-self.angle), self.scale)
        game_window.blit(self.image, self.rect)
        pygame.draw.rect(game_window, (255, 64, 255), self.rect, 2)
        self._oldS = self.scale
        self._oldA = self.angle
        self._oldOI = self.orig_image