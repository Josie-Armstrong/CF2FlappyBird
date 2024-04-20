import pygame, sys, random, math

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('./Game Textures/Coin/coin.png').convert_alpha()

        self.image = pygame.transform.scale_by(self.image, 3)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    
    def update(self, scroll_speed):
        self.rect.x -= scroll_speed
        if self.rect.right < 0: #gets rid of pipes that are offscreen to save memory
            self.kill()