import os
from math import ceil, cos, degrees, pi, radians, sin
from random import randint, random

import pygame
from pygame.locals import DOUBLEBUF

pygame.init()
S_INFO = {}

def clamp(v, maxv, minv):
    return min(max(v, minv), maxv)

def update_screen_info():
    info = pygame.display.Info()
    S_INFO["w"] = clamp(info.current_w, 1280, 640)
    S_INFO["h"] = clamp(info.current_h, 960, 480)
    S_INFO["r"] = S_INFO["w"] / S_INFO["h"]
    S_INFO["c"] = (S_INFO["w"] / 2, S_INFO["h"] / 2); 
    S_INFO["cx"] = S_INFO["c"][0]; S_INFO["cy"] = S_INFO["c"][1]
    S_INFO["sw"] = S_INFO["w"] / 1200; S_INFO["sh"] = S_INFO["h"] / 900
    
update_screen_info()
SCREEN = pygame.display.set_mode((S_INFO["w"], S_INFO["h"]), DOUBLEBUF)
FPS = 30

def draw_middle(tex):
    b = TEXTURES[tex]
    SCREEN.blit(b, (S_INFO["cx"] - b.get_width() / 2, S_INFO["cy"] - b.get_height() / 2))

def asset_path(*argv):
    p = os.path.join(".", "assets")
    for f in argv:
        p = os.path.join(p, f)
    return p

def load_all_textures(dir):
    for i in sorted(os.listdir(asset_path("textures", dir))):
        if (i.endswith(".png")):
            orig = pygame.image.load(asset_path("textures", dir, i)).convert_alpha()
            name = dir + "\\" + i if dir != "" else i
            if (orig.get_width() > 10):
                TEXTURES[name] = pygame.transform.scale(orig, (orig.get_width() * (S_INFO["sw"] if (orig.get_width() != orig.get_height()) else S_INFO["sh"]), orig.get_height() * S_INFO["sh"]))
            else:
                TEXTURES[name] = orig
        else:
            load_all_textures(i)

TEXTURES = {}
SOUNDS = {}
FONTS = {}
load_all_textures("")

for i in sorted(os.listdir(asset_path("sounds"))):
    SOUNDS[i] = pygame.mixer.Sound(asset_path("sounds", i))

for i in sorted(os.listdir(asset_path("fonts"))):
    if (i.endswith(".ttf")):
        a = i.split("_s")
        FONTS[a[0]] = pygame.font.Font(asset_path("fonts", i), ceil(int(a[1].split(".")[0]) * S_INFO["sh"]))

def is_outside_surface(surf: pygame.Surface, point):
    h, w = surf.get_height(), surf.get_width()
    return (point[0] < 0 or point[0] > w) or (point[1] < 0 or point[1] > h)

def flip_list(lst: list):
    old = lst.copy()
    lst.clear()
    lst.extend([pygame.transform.flip(s, True, False) for s in old])

class Fader(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image : pygame.Surface = TEXTURES["pixel.png"]
        self.image.fill((0, 0, 0))
        self.image = pygame.transform.scale(self.image, (S_INFO["w"], S_INFO["h"]))
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
        for i in range(0, ceil(S_INFO["w"] / self.width) + 1):
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
        
        self.dir = kargs.get("dir", 1)  
        self.scale = kargs.get("scale", 1)
        self.angle = kargs.get("angle", 0)
        self.orig_image = self.sprites[0]     
        
        self._oldD = 1
        self._oldS = 1
        self._oldA = 0
        self._oldOI = None

        self.rect = self.orig_image.get_rect(center=self.origin)
        self.change_image()
        self._oldS = self.scale
        self._oldA = self.angle
        self._oldOI = self.orig_image
        self._oldD = self.dir
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
            self.angle += self.dir * self.speed * (1 if not hasattr(self, "mul") else self.mul) * (S_INFO["r"] * 3 / 4)
    
    def animate(self):
        if (not game.paused):
            if (self.framea % ceil(10 / (1 if not hasattr(self, "mul") else self.mul)) == 0):
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
        pygame.display.set_icon(TEXTURES["red_planet.png"])
        self.clock = pygame.time.Clock()
        self.fader = Fader()
        self.player = None
        self.is_playing = False
        self.paused = False
        self.running = 1
        self.max_score = self.score = 0
        try:
            data = open(os.path.join(".", "score.txt"), "r")
            self.max_score = int(data.read())
            data.close()
        except:
            print("Previous score not found!")
    
    def run(self):
        bg = ParallaxBG(TEXTURES["title\\bg.png"])
        planet = pygame.transform.scale(TEXTURES["red_planet.png"], (300  * S_INFO["sh"], 300 * S_INFO["sh"]))
        planet_cache = [(pygame.transform.rotate(planet, a)) for a in range (0, 360, 2)]
        title = TEXTURES["title\\title.png"]
        title2 = TEXTURES["title\\title2.png"]
        astronaut = pygame.transform.scale(TEXTURES["player0.png"], (145 * S_INFO["sw"], 333 * S_INFO["sh"]))
        angle = 0

        self.fader.start(3)
        SOUNDS["main_menu.wav"].play(loops=-1, fade_ms = 3000)
        while self.running:
            update_screen_info()
            
            bg.draw()
            if self.is_playing:
                if self.player.game_over:
                    max_score = FONTS["Cave-Story"].render(f"Highest score: {self.max_score}", False, (255, 0, 0))
                    SCREEN.blit(max_score, (S_INFO["cx"] - max_score.get_width() / 2, S_INFO["cy"] - max_score.get_height() / 2 + 100 * S_INFO["sh"]))
                self.player.update_player()
                score = FONTS["Cave-Story"].render(f"Score: {self.score}", False, (255, 0, 0))
                SCREEN.blit(score, (S_INFO["cx"] - score.get_width() / 2, S_INFO["cy"] - score.get_height() / 2 - 100 * S_INFO["sh"] if self.player.game_over else 20))
                for i in range (1, 4):
                    tex = TEXTURES["empty_h.png"]
                    SCREEN.blit(tex, (S_INFO["w"] - tex.get_width()*i - 3*i, 18))
                for i in range (1, self.player.lives+1):
                    tex = TEXTURES["heart.png"]
                    SCREEN.blit(tex, (S_INFO["w"] - tex.get_width()*i - 3*i, 18))
                if self.fader.has_ended:
                    if self.paused and self.fader.image.get_alpha() != 127:
                        self.fader.image.set_alpha(127)
                    elif not self.paused and self.fader.image.get_alpha() != 0:
                        self.fader.image.set_alpha(0)
                if self.score > self.max_score:
                    self.max_score = self.score
                    data = open(os.path.join(".", "score.txt"), "w")
                    data.write(str(self.max_score))
                    data.close()
            else:
                SCREEN.blit(astronaut, (104 * (S_INFO["w"] / 1200), (450 + 10 * sin(3 + angle / 20)) * S_INFO["sh"]))
                SCREEN.blit(planet_cache[round(angle / 2) % len(planet_cache)], planet_cache[round(angle / 2) % len(planet_cache)].get_rect(center = planet.get_rect(topleft = (810 * S_INFO["sw"], 470 * S_INFO["sh"])).center))
                SCREEN.blit(title, (S_INFO["cx"] - title.get_width() / 2, 230 - title.get_height() / 2 + 10 * sin(angle / 20)))
                SCREEN.blit(title2, (S_INFO["cx"] - title2.get_width() / 2, S_INFO["h"] - 100 - title2.get_height() / 2 + 5 * sin(1.5 + angle / 20)))
                angle += 2
    
            if (self.fader.fading == False and self.fader.has_ended() and not self.is_playing):
                self.is_playing = True
                self.fader.start(1)
                SOUNDS["battle.mp3"].play(loops=-1, fade_ms=1000)
                
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
                    SOUNDS["main_menu.wav"].fadeout(3000)
                    
game = Game()
