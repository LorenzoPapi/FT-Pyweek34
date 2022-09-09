from math import ceil, sin, cos, degrees, radians
from pygame.locals import DOUBLEBUF
from random import randint, random
import pygame
import os

SCREEN_RES = 4/3
SCREEN_HEIGHT = 900
SCREEN_WIDTH = ceil(SCREEN_RES * SCREEN_HEIGHT) - 1
SCREEN_CENTER = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2); SCREEN_CENTERX = SCREEN_CENTER[0]; SCREEN_CENTERY = SCREEN_CENTER[1]

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), DOUBLEBUF, 16)
FPS = 30

def load_texture(*args):
    return pygame.image.load(asset_path("textures", *args)).convert_alpha()


def clamp(v, maxv, minv):
    return min(max(v, minv), maxv)


def is_outside_surface(surf: pygame.Surface, point):
    h, w = surf.get_height(), surf.get_width()
    return (point[0] < 0 or point[0] > w) or (point[1] < 0 or point[1] > h)

# https://stackoverflow.com/questions/4183208/how-do-i-rotate-an-image-around-its-center-using-pygame

def blit_rotate_center(surf : pygame.Surface, image : pygame.Surface, topleft, angle):
    rotated_image = pygame.transform.rotate(image, angle).convert_alpha()
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)

    surf.blit(rotated_image, new_rect)

def asset_path(*argv):
    p = os.path.join(".", "assets")
    for f in argv:
        p = os.path.join(p, f)
    return p


def flip_list(lst: list):
    old = lst.copy()
    lst.clear()
    lst.extend([pygame.transform.flip(s, True, False) for s in old])

class ScaledSprite(pygame.sprite.Sprite):
    def __init__(self, *sprites : pygame.Surface):
        super().__init__()
        self.sprites = [(pygame.transform.scale(s, (s.get_width() / SCREEN_RES, s.get_height() / SCREEN_RES))) for s in sprites]
        self.image = self.sprites[0]

class Fader(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image : pygame.Surface = load_texture("pixel.png")
        self.image.fill((0, 0, 0))
        self.image = pygame.transform.scale(self.image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.rect = self.image.get_rect(topleft = (0, 0))
        self.timer = 0
        self.total = 0
        self.fading = None

    def start(self, sec, fade=True):
        if (self.timer == 0):
            self.timer = self.total = sec * FPS
            self.fading = fade
        
    def update(self):
        if (self.timer > 0): 
            self.timer -= 1
            alpha = 255 * self.timer / self.total
            self.image.set_alpha(alpha if self.fading else 255 - alpha)
        elif self.fading:
            self.total = 0
        SCREEN.blit(self.image, self.rect)
    
    def has_ended(self):
        return self.timer == 0

class ParallaxBG(pygame.sprite.Sprite):
    def __init__(self, image : pygame.Surface):
        super().__init__()
        self.image = image.convert_alpha()
        self.width = self.image.get_width()
        self.rect = self.image.get_rect()
        self.scrollx = 0
    
    def draw(self):
        for i in range(0, ceil(SCREEN_WIDTH / self.width) + 1):
            self.rect.x = i * self.width + self.scrollx
            SCREEN.blit(self.image, self.rect)
        self.scrollx -= 3
        
        if (abs(self.scrollx) > self.width):
            self.scrollx = 0
        
class RotatingSprite(pygame.sprite.Sprite):
    def __init__(self, *args : pygame.Surface, **kargs):
        super().__init__()
        self.sprites = [s for s in args]
        self.origin = kargs.get("origin", (0, 0))
        self.start_pos = kargs.get("start_pos", (0, 0))
        self.speed = kargs.get("speed", 0)
        
        self.dir = kargs.get("dir", 1)  # -1 is left, 1 is right
        self.scale = kargs.get("scale", 1)
        self.angle = kargs.get("angle", 0)
        self.orig_image = self.sprites[0]     
        
        self._oldD = 1
        self._oldS = 1
        self._oldA = 0
        self._oldOI = None

        self.change_image()
        self.rect = self.image.get_rect(center=self.origin)
        self.change_rect()

        self.framea = 0
        self.index = 0

    def change_image(self):
        if (self.dir != self._oldD):
            flip_list(self.sprites)
            self.orig_image = self.sprites[0]
        if (self._oldS != self.scale or self._oldA != self.angle or self._oldOI != self.orig_image):
            self.image = pygame.transform.rotozoom(self.orig_image, degrees(-self.angle), self.scale)

    def draw(self):
        self.change_image()
        SCREEN.blit(self.image, self.rect)
        #pygame.draw.rect(SCREEN, (255, 64, 255), self.rect, 2)
        self._oldS = self.scale
        self._oldA = self.angle
        self._oldOI = self.orig_image
        self._oldD = self.dir

    def change_rect(self):
        self.rect = self.image.get_rect(center=((self.origin[0] + self.start_pos[0] * sin(self.angle), self.origin[1] - self.start_pos[1] * cos(self.angle))))

    def update(self):
        self.draw()
        if (not game.paused):
            self.change_image()
            self.change_rect()
            self.angle += self.dir * self.speed
    
    def animate(self):
        if (not game.paused):
            if (self.framea % 10 == 0):
                self.orig_image = self.sprites[self.index % len(self.sprites)]
                self.index += 1
            self.framea += 1


class DoubleSinSprite(RotatingSprite):
    def change_rect(self):
        self.rect = self.image.get_rect(center = (self.origin[0] + self.start_pos[0] * sin(self.angle), self.origin[1] - abs(self.start_pos[1] * sin(self.angle))))

    # def update(self):
    #     super().update()
    #     if (self.angle > 3.1):
    #         self.speed = -self.speed
    #         self.angle = 3.08
    #         print("A A")

class StraightLineSprite(RotatingSprite):
    def __init__(self, *args: pygame.Surface, **kargs):
        super().__init__(*args, **kargs)
        self.rect = self.image.get_rect(center=((self.origin[0], self.origin[1] - self.start_pos[1])))

    def change_rect(self):
        self.rect.x += self.speed

    def update(self):
        if (not game.paused):
            self.change_image()
            self.change_rect()
        self.draw()

class Game():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Catch the Ketchup!')
        self.clock = pygame.time.Clock()
        self.fader = Fader()
        self.player = None
        self.game_start = False
        self.paused = False
        self.running = 1
    
    def run(self):
        bg = ParallaxBG(load_texture("title", "bg.png"))
        planet = pygame.transform.scale(load_texture("red_planet.png"), (300, 300)).convert_alpha()
        title = ScaledSprite(load_texture("title", "title.png"))
        title2 = ScaledSprite(load_texture("title", "title2.png"))
        astronaut = pygame.image.load('assets/textures/title/a_1.png')
        angle = 0

        self.fader.start(3)
        while self.running:
            bg.draw()
            if self.game_start:
                self.player.update_player()
            else:
                SCREEN.blit(astronaut, (104, 450 + 5 * sin(1.5 + angle / 20)))
                blit_rotate_center(SCREEN, planet, (810, 470), angle)
                SCREEN.blit(title.image, (SCREEN_CENTERX - title.image.get_width() / 2, 230 - title.image.get_height() / 2 + 10 * sin(angle / 20)))
                SCREEN.blit(title2.image, (SCREEN_CENTERX - title2.image.get_width() / 2, SCREEN_HEIGHT - 100 - title2.image.get_height() / 2 + 5 * sin(1.5 + angle / 20)))
                angle += 0.5
    
            if (self.fader.fading == False and self.fader.has_ended() and not self.game_start):
                self.game_start = True
                self.fader.start(1)
            
            self.fader.update()
            self.event_handler()
            pygame.display.update()
            self.clock.tick(FPS)
        pygame.quit()
        exit(0)
    
    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = 0
            else:
                if self.game_start:
                    if self.fader.has_ended() and event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                        self.player.key_handler(event)
                elif self.fader.has_ended() and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.fader.start(3, False)

game = Game()