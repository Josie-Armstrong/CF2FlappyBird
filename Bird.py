import pygame, sys, random, math
from pygame.locals import *

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images =[]
        self.index = 0
        self.counter = 0
        for num in range(1,4):
            img = pygame.image.load(f'./Game Textures/Sprites/Birds L1/coolbird{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.vel = 0 #bird's velocity
        self.jumped = False
        self.mid_air = False
    
    #for the size change level, changes size of bird and rect
    def sizeChange(self, scale, reset = False):
        if reset == True:
            for i in range(len(self.images)):
                self.images[i] = pygame.image.load(f'./Game Textures/Sprites/Birds L1/coolbird{i + 1}.png')
                self.images[i] = pygame.transform.scale(self.images[i], (51,37))
        else:
            for i in range(len(self.images)):
                    self.images[i] = pygame.transform.scale_by(self.images[i], scale)
        
        centerx = self.rect.centerx
        centery = self.rect.centery

        self.rect = self.images[0].get_rect()
        self.rect.center = [centerx, centery]
        print(self.rect.width, self.rect.height)

    def update(self, flying, game_over, drinkMe = False):


        #gravity
        if flying == True:
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 618: #if bird is above the ground (inc y means moving down)
                self.rect.y += int(self.vel)

                
        if game_over == False:
        #jumping
            self.mid_air = True
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped == False and self.mid_air == True:
                self.jumped = True
                self.vel = -10

            if key[pygame.K_SPACE] == False:
                self.jumped = False




            #handle animation
            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            #rotate the bird
            self.image = pygame.transform.rotate(self.images[self.index], self.vel*-2)
