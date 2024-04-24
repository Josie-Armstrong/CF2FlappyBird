import pygame, sys, random, math
from pygame.locals import *

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position, pipe_gap, level = 1):
        pygame.sprite.Sprite.__init__(self)

        # Pipe image is determined by the level
        if level == 1:
            self.image = pygame.image.load('./Game Textures/Obstacles/level1.png').convert_alpha()
        elif level == 2:
            self.image = pygame.image.load('./Game Textures/Obstacles/bubbles.png').convert_alpha()
        elif level == 3:
            self.image = pygame.image.load('./Game Textures/Obstacles/level1.png').convert_alpha()
        else:
            self.image = pygame.image.load('./Game Textures/Obstacles/level1.png').convert_alpha()

        self.image = pygame.transform.scale(self.image, (78, 560))
        self.rect = self.image.get_rect()
        #position 1 is from top, -1 is from bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True) #False = x-axis, True = y-axis
            self.rect.bottomleft = [x,y - int(pipe_gap / 2)]
        if position == -1: 
            self.rect.topleft = [x,y + int(pipe_gap / 2)]

    def update(self, scroll_speed):
        self.rect.x -= scroll_speed
        if self.rect.right < 0: #gets rid of pipes that are offscreen to save memory
            self.kill()