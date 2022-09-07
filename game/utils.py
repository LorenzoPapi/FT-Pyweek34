from math import sin, cos, degrees, radians
from pygame.locals import DOUBLEBUF
from random import randint, random
import pygame
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


def isOutsideSurface(surf: pygame.Surface, point):
    h, w = surf.get_height(), surf.get_width()
    return (point[0] < 0 or point[0] > w) or (point[1] < 0 or point[1] > h)

# https://stackoverflow.com/questions/4183208/how-do-i-rotate-an-image-around-its-center-using-pygame


def rot_center(image: pygame.Surface, angle, center):
    rotated = pygame.transform.rotozoom(image, angle, 1)
    return rotated, rotated.get_rect(center=image.get_rect(center=center).center)


def asset_path(*argv):
    p = os.path.join(".", "assets")
    for f in argv:
        p = os.path.join(p, f)
    return p


def flip_list(lst: list):
    old = lst.copy()
    lst.clear()
    lst.extend([pygame.transform.flip(s, True, False) for s in old])


class SuperSprite(pygame.sprite.Sprite):
    def __init__(self, *args : pygame.Surface, **kargs):
        super().__init__()
        self.sprites = [s.convert_alpha() for s in args]
        
        self.origin = kargs.get("origin", (0, 0))
        self.start_pos = kargs.get("start_pos", (0, 0))
        self.speed = kargs.get("speed", 0)
        
        self.dir = kargs.get("dir", 1)  # -1 is left, 1 is right
        self.scale = kargs.get("scale", 1)
        self.angle = kargs.get("angle", 0)
        self.orig_image = self.sprites[0]        
        
        self._oldD = self.dir
        self._oldS = self.scale
        self._oldA = self.angle
        self._oldOI = self.orig_image

        if (self.dir == -1):
            flip_list(self.sprites)
            self.orig_image = self.sprites[0]

        self.image = pygame.transform.rotozoom(self.orig_image, degrees(-self.angle), self.scale)
        self.rect = self.image.get_rect(center=self.origin)

    def change_image(self):
        if (self.dir != self._oldD):
            flip_list(self.sprites)
            self.orig_image = self.sprites[0]
        if (self._oldS != self.scale or self._oldA != self.angle or self._oldOI != self.orig_image):
            self.image = pygame.transform.rotozoom(self.orig_image, degrees(-self.angle), self.scale)

    def draw(self):
        self.change_image()
        game_window.blit(self.image, self.rect)
        pygame.draw.rect(game_window, (255, 64, 255), self.rect, 2)
        self._oldS = self.scale
        self._oldA = self.angle
        self._oldOI = self.orig_image
        self._oldD = self.dir

    def update(self):
        self.angle += self.dir * self.speed
        self.angle *= game_speed
        self.change_image()
        self.rect = self.image.get_rect(center=((self.origin[0] + (self.start_pos[0]) * sin(self.angle), self.origin[1] - (self.start_pos[1]) * cos(self.angle))))
        self.draw()
