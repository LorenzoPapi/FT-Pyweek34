import pygame

window = pygame.display.set_mode((1200, 900))

def clamp(v, maxv, minv):
    return min(max(v, minv), maxv)

def isOutsideSurface(window, point):
    h, w = window.get_height(), window.get_width()
    return (point[0] < 0 or point[0] > w) or (point[1] < 0 or point[1] > h)

# https://stackoverflow.com/questions/4183208/how-do-i-rotate-an-image-around-its-center-using-pygame
def rot_center(image, angle, center):
    rotated = pygame.transform.rotate(image, angle)
    return rotated, rotated.get_rect(center = image.get_rect(center = center).center)

class SuperSprite(pygame.sprite.Sprite):
    def __init__(self, window, image):
        super().__init__()
        self.window = window
        self.image = image
        self.orig_image = image
        self.rect = self.image.get_rect()
        self.angle = 0
        self.scale = 1
    
    def update(self):
        self.image = pygame.transform.rotozoom(self.orig_image, self.angle, self.scale)
        self.window.blit(self.image, self.rect)
        pygame.draw.rect(self.window, (255, 64, 255), self.rect, 2)