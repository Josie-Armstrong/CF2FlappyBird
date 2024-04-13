import pygame, sys, random, math
from pygame.locals import *

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position, pipe_gap):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('./Game Textures/Obstacles/level1.png')
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