import pygame, sys, random, math
from pygame.locals import *

class ShopButton():
    def __init__(self, x, y, image, screen):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.screen = screen
    
    def draw(self):
        #draw button
        self.screen.blit(self.image, (self.rect.x, self.rect.y))

    def check_pressed(self):

        action = False
        #get mouse position
        pos = pygame.mouse.get_pos()

        #check if mouse is over button
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1: #mouse presssed use index values for left, right, middle click
                action = True

        return action