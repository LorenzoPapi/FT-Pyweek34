import pygame

def clamp(v, maxv, minv):
    return min(max(v, minv), maxv)

def isOutsideSurface(window, point):
    h, w = window.get_height(), window.get_width()
    return (point[0] < 0 or point[0] > w) or (point[1] < 0 or point[1] > h)

# https://stackoverflow.com/questions/4183208/how-do-i-rotate-an-image-around-its-center-using-pygame
def rot_center(image, angle, center):
    rotated = pygame.transform.rotate(image, angle)
    return rotated, rotated.get_rect(center = image.get_rect(center = center).center)