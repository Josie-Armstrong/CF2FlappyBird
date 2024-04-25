import pygame,sys, random, math
from pygame.locals import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('./Game Textures/Sprites/Projectile.png').convert_alpha()  # Load enemy image
        self.rect = self.image.get_rect(center=(x, y))  # Set initial position
        self.speed = speed  # Speed of the enemy

    def update(self):
        self.rect.x -= self.speed  # Move the enemy towards the left
enemy_speed = 10  # Adjust as needed

# Define variables for enemy spawn control
last_enemy_spawn = pygame.time.get_ticks()  # Initialize to current time
enemy_spawn_frequency = 1000  # Adjust as needed, 1000 milliseconds = 1 seconds
