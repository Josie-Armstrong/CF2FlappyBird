import pygame, sys, random, math
from pygame.locals import *

class HeartShield(pygame.sprite.Sprite):
    def __init__(self, type, num, screen_height, screen):
        self.screen = screen
        self.y = 0
        
        if type == 'h':
            self.image = pygame.image.load('./Game Textures/Shop/heart.png').convert_alpha()
            self.y = (screen_height - 40)
        elif type == 's':
            self.image = pygame.image.load('./Game Textures/Shop/shield.png').convert_alpha()
            self.y = (screen_height - 75)
        
        self.image = pygame.transform.scale_by(self.image, 2)

        self.num = num
        self.x = 10 + (num * (32 + 3))

        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
    
    def draw(self):
        self.screen.blit(self.image,self.rect.center)