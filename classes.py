# sprite classes for project game
import pygame
import random
import math
from settings import *

class Shop(pygame.sprite.Sprite):
    # Define the constructor
    def __init__(self):
        # Call the sprite constructor
        super().__init__()
        # Set the position of the sprite
        self.image = pygame.Surface([size[0], size[1]])
        self.image.fill(BLUE) # fill sprite with the color
        self.rect = self.image.get_rect()
        self.rect.x = 0 
        self.rect.y = 0
        self.width = size[0]
        self.height = size[1]
        
        
class Enemy(pygame.sprite.Sprite):
    # Define the constructor
    def __init__(self, width, height, player):
        # Call the sprite constructor
        super().__init__()
        # Set the position of the sprite
        self.image = pygame.Surface([width, height])
        self.image.fill(RED) # fill sprite with the color
        self.rect = self.image.get_rect()
        self.rect.x = -random.randrange(0, 1000) # set initial x coordinate
        self.rect.y = size[1]/2.3 # set initial y coordinate
        self.width = width
        self.height = height
        self.speed = 1 # set enemy speed
    
            
class Player(pygame.sprite.Sprite):
    # Define the constructor
    def __init__(self):
        # Call the sprite constructor
        pygame.sprite.Sprite.__init__(self)
        # Set the position of the sprite
        self.image = pygame.Surface([40, 40])
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = size[0]/2
        self.rect.y = size[1] - 40
        self.width = 40
        self.height = 40
        self.speed = 0
 
    def update(self):
        self.rect.y += self.speed #player move up or down            
        if self.rect.y <= size[1]-self.height:
            self.rect.y += 2 #gravitational effect
        if self.rect.y >= size[1]: #floor
            self.rect.y = size[1] - self.height
        if self.rect.y <= 0: #ceiling
            self.rect.y = 0


class bullets(pygame.sprite.Sprite):
    # Define the constructor 
    def __init__(self, color, plx, ply): # bullet uses player's x and y coordinates 
        # Call the sprite constructor
        super().__init__()
        # Create a sprite and fill it with colour
        self.image = pygame.Surface([10, 10])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        # bullet position is player's position
        self.rect.x = plx
        self.rect.y = ply 
        self.width = 10
        self.height = 10
        self.speed = game_speed * 2

    def update(self):
        self.rect.x = self.rect.x - self.speed #bullets move left


class Lives(pygame.sprite.Sprite):
    # Define the constructor
    def __init__(self, color, width, height):
        # Call the sprite constructor
        super().__init__()
        # Create a sprite and fill it with colour
        self.image = pygame.Surface([width,height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(1000, 6000)
        self.rect.y = random.randrange(0, size[1] - height)
        # Set the position of the sprite
        self.width = width
        self.height = height
        self.speed = game_speed
        
    def update(self): # create illusion that player is moving right
        self.rect.x = self.rect.x - self.speed #move to the left


class Coins(pygame.sprite.Sprite):
    # Define the constructor
    def __init__(self, color, width, height):
        # Call the sprite constructor
        super().__init__()
        # Create a sprite and fill it with colour
        self.image = pygame.Surface([width,height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(1000, 2000)
        self.rect.y = random.randrange(0, size[1] - height)
        # Set the position of the sprite
        self.width = width
        self.height = height
        self.speed = game_speed
        
    def update(self): # create illusion that player is moving right
        self.rect.x = self.rect.x - self.speed #move to the left


## -- Define the class invaders which is a sprite
class Obstacle(pygame.sprite.Sprite):
    # Define the constructor
    def __init__(self, width, height):
        # Call the sprite constructor
        super().__init__()
        # Create a sprite and fill it with colour
        self.width = width
        self.height = height
        self.color = RED
        self.image = pygame.Surface([width,height])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = -100 # spawn in a random position
        self.rect.y = -100
        # Set the position of the sprite


class Pillars(Obstacle):
    pass

    def update(self): # create illusion that player is moving right
        self.rect.x = self.rect.x - game_speed #obstacles move to the left
        if self.rect.x <= 0:
            self.rect.x = random.randrange(1000, 2000) # respawn if they go off the screen
            self.rect.y = random.randrange(0, size[1]-self.height) #respawn in a random position

class Rockets(Obstacle):
    pass

    def update(self): # create illusion that player is moving right
        self.rect.x = self.rect.x - game_speed*2 #obstacles move to the left
        if self.rect.x <= 0:
            self.rect.x = 3000 # respawn if they go off the screen
            self.rect.y = random.randrange(0, size[1]-self.height) #respawn in a random position

