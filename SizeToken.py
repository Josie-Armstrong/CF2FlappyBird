import pygame, sys, random, math
from pygame.locals import *

class Token(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        pygame.sprite.Sprite.__init__(self)
        self.type = ""

        if type == 1:
            self.image = pygame.image.load('./Game Textures/Tokens/largeToken.png').convert_alpha()
            self.type = "large"
        else:
            self.image = pygame.image.load('./Game Textures/Tokens/smallToken.png').convert_alpha()
            self.type = "small"

        self.image = pygame.transform.scale_by(self.image, 1.5)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    
    def update(self, scroll_speed):
        self.rect.x -= scroll_speed
        if self.rect.right < 0: #gets rid of pipes that are offscreen to save memory
            self.kill()

