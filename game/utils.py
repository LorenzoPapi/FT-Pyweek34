from math import ceil, sin, cos, degrees, radians
from pygame.locals import DOUBLEBUF
from random import randint, random
import pygame
import os

pygame.init()

SCREEN_RES = 4/3
SCREEN_HEIGHT = 900
SCREEN_WIDTH = ceil(SCREEN_RES * SCREEN_HEIGHT) - 1
SCREEN_CENTER = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2); SCREEN_CENTERX = SCREEN_CENTER[0]; SCREEN_CENTERY = SCREEN_CENTER[1]

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), DOUBLEBUF, 16)
FPS = 30

def draw_middle(tex):
    b = TEXTURES[tex]
    SCREEN.blit(b, (SCREEN_CENTERX - b.get_width() / 2, SCREEN_CENTERY - b.get_height() / 2))

def asset_path(*argv):
    p = os.path.join(".", "assets")
    for f in argv:
        p = os.path.join(p, f)
    return p

def load_all_textures(dir):
    for i in sorted(os.listdir(asset_path("textures", dir))):
        if (i.endswith(".png")):
            TEXTURES[dir + "\\" + i if dir != "" else i] = pygame.image.load(asset_path("textures", dir, i)).convert_alpha()
        else:
            load_all_textures(i)

def load_all_fonts(dir):
    for i in sorted(os.listdir(asset_path("fonts", dir))):
        if (i.endswith(".ttf")):
            a = i.split("_s")
            FONTS[dir + "\\" + a[0] if dir != "" else a[0]] = pygame.font.Font(asset_path("fonts", dir, i), int(a[1].split(".")[0]))
        else:
            load_all_fonts(i)

TEXTURES = {}
SOUNDS = {}
FONTS = {}
load_all_textures("")
load_all_fonts("")

# def floatRange(start, end, step):
#     values = []
#     step = decimal.Decimal(str(step))
#     while start < end:
#         values.append(float(start))
#         start += step
        
#     return values

def clamp(v, maxv, minv):
    return min(max(v, minv), maxv)

def is_outside_surface(surf: pygame.Surface, point):
    h, w = surf.get_height(), surf.get_width()
    return (point[0] < 0 or point[0] > w) or (point[1] < 0 or point[1] > h)

# https://stackoverflow.com/questions/4183208/how-do-i-rotate-an-image-around-its-center-using-pygame

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
        self.image : pygame.Surface = TEXTURES["pixel.png"]
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
        if not game.paused: self.scrollx -= 3
        
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
        pygame.display.set_caption('Catch the Ketchup!')
        self.clock = pygame.time.Clock()
        self.fader = Fader()
        self.player = None
        self.is_playing = False
        self.paused = False
        self.running = 1
        self.score = 0
    
    def run(self):
        bg = ParallaxBG(TEXTURES["title\\bg.png"])
        planet = pygame.transform.scale(TEXTURES["red_planet.png"], (300, 300))
        planet_cache = [(pygame.transform.rotate(planet, a)) for a in range (0, 360)]
        title = ScaledSprite(TEXTURES["title\\title.png"])
        title2 = ScaledSprite(TEXTURES["title\\title2.png"])
        astronaut = ScaledSprite(TEXTURES["title\\a_1.png"])
        angle = 0

        self.fader.start(3)
        while self.running:
            bg.draw()
            if self.is_playing:
                self.player.update_player()
                score = FONTS["Cave-Story"].render(f"SCORE: {self.score}", False, (255, 0, 0))
                SCREEN.blit(score, (SCREEN_CENTERX - score.get_width() / 2, SCREEN_CENTERY - score.get_height() / 2 if self.player.game_over else 20))
                if self.fader.has_ended:
                    if self.paused and self.fader.image.get_alpha() != 127:
                        self.fader.image.set_alpha(127)
                    elif not self.paused and self.fader.image.get_alpha() != 0:
                        self.fader.image.set_alpha(0)
            else:
                SCREEN.blit(astronaut.image, (104, 450 + 10 * sin(3 + angle / 20)))
                SCREEN.blit(planet_cache[ceil(angle) % 360 - 1], planet_cache[ceil(angle) % 360 - 1].get_rect(center = planet.get_rect(topleft = (810, 470)).center))
                SCREEN.blit(title.image, (SCREEN_CENTERX - title.image.get_width() / 2, 230 - title.image.get_height() / 2 + 10 * sin(angle / 20)))
                SCREEN.blit(title2.image, (SCREEN_CENTERX - title2.image.get_width() / 2, SCREEN_HEIGHT - 100 - title2.image.get_height() / 2 + 5 * sin(1.5 + angle / 20)))
                angle += 0.5
    
            if (self.fader.fading == False and self.fader.has_ended() and not self.is_playing):
                self.is_playing = True
                self.fader.start(1)
                
            self.event_handler()
            self.fader.update()
            pygame.display.update()
            self.clock.tick(FPS)
        pygame.quit()
        exit(0)
    
    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = 0
            else:
                if self.is_playing:
                    if self.fader.has_ended():
                        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                            self.player.key_handler(event)
                        if (event.type == pygame.KEYDOWN and event.key == pygame.K_p):
                            game.paused = not game.paused
                elif self.fader.has_ended() and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.fader.start(3, False)

game = Game()