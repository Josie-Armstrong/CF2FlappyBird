import pygame, sys, random, math
import ShopButton
from pygame.locals import *

class Shop(pygame.sprite.Sprite):

    def __init__(self, screen, screen_width, screen_height):
        # defining the background and the screen
        self.bg = pygame.image.load('./Game Textures/Shop/shop_bg.png').convert()
        self.bg = pygame.transform.scale(self.bg, (664, 736))
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height

        # making the ShopButton objects to buy shields and hearts
        buy_btn_img = pygame.image.load('./Game Textures/Shop/buy_btn.png').convert()
        buy_btn_img = pygame.transform.scale_by(buy_btn_img, 6)
        self.shield_buy_btn = ShopButton.ShopButton(90, 420, buy_btn_img, self.screen)
        self.heart_buy_btn = ShopButton.ShopButton(390, 420, buy_btn_img, self.screen)

        # making the back button object
        back_img = pygame.image.load('./Game Textures/Shop/back_btn.png').convert()
        back_img = pygame.transform.scale_by(back_img, 6)
        self.back_btn = ShopButton.ShopButton((self.screen_width - 180), self.screen_height - 100, back_img, self.screen)
    
    def draw(self):

        # draw background and buttons
        self.screen.blit(self.bg, (0,0))
        self.shield_buy_btn.draw()
        self.heart_buy_btn.draw()
        self.back_btn.draw()

        action = -1

        # check for button presses
        if self.back_btn.check_pressed() == True:
            action = 0
        elif self.shield_buy_btn.check_pressed() == True:
            action = 1
        elif self.heart_buy_btn.check_pressed() == True:
            action = 2
        
        return action