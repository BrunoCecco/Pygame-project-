# sprite classes for project game
import pygame
import random
import math
from settings import *

'''
text1 = font.render("START", True, WHITE)
text2 = font.render("OPTIONS", True, WHITE)
text3 = font.render("ABOUT", True, WHITE)
rect1 = pygame.Rect(size[0]/2.5,size[1]/2.5,115,40)
rect2 = pygame.Rect(300,400,115,40)
rect3 = pygame.Rect(300,500,115,40)
# The buttons consist of a text surface, a rect and a color.
buttons = [
    [text1, rect1, BLACK],
    #[text2, rect2, BLACK],
    #[text3, rect3, BLACK],
    ]
'''
       
    
def game_intro():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return False
            elif event.type == pygame.MOUSEMOTION:
                for button in buttons:  # button[1] is the rect. Use its collidepoint method to detect collision
                    if button[1].collidepoint(event.pos): # Set the button's color to the hover color.
                        button[2] = HOVER_COLOR
                    else:
                        # Otherwise reset the color to black.
                        button[2] = BLACK
            elif event.type == pygame.MOUSEBUTTONDOWN: #if start button clicked, exit game_intro and start game
                for button in buttons:
                    if button[1].collidepoint(event.pos):
                        return False # game intro is false so game loop begins

        screen.fill(WHITE)

        # Draw the buttons with their current colors at their rects.
        for text, rect, color in buttons:
            pygame.draw.rect(screen, color, rect)
            screen.blit(text, rect)

        pygame.display.flip()
        clock.tick(15)

class Enemy(pygame.sprite.Sprite):
    # Define the constructor
    def __init__(self, width, height, player):
        # Call the sprite constructor
        super().__init__()
        # Set the position of the sprite
        self.image = pygame.Surface([width, height])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = -random.randrange(0, 1000)
        self.rect.y = size[1]/2.3
        self.rect.topleft = self.rect.x, self.rect.y
        self.width = width
        self.height = height
        self.speed = 1
    
            
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
        self.rect.topleft = self.rect.x, self.rect.y
        self.width = 40
        self.height = 40
        self.speed = 0
        #self.bullet = bullet
 
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
    def __init__(self, color, plx, ply):
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
        self.rect.x = self.rect.x - self.speed #bullets move right


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
        self.rect.x = self.rect.x - self.speed #obstacles move to the left


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
        self.rect.x = self.rect.x - self.speed #obstacles move to the left

## -- Define the class invaders which is a sprite
class Obstacle(pygame.sprite.Sprite):
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
        self.rect.x = self.rect.x - self.speed #obstacles move to the left
        if self.rect.x <= 0:
            self.rect.x = random.randrange(1000, 2000)
            self.rect.y = random.randrange(0, size[1]-self.height)


class Rocket(pygame.sprite.Sprite): 
    def __init__(self, color, width, height):
        # Call the sprite constructor
        super().__init__()
        self.image = pygame.Surface([width,height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        # Set the position of the sprite
        self.width = width
        self.height = height
        self.speed = game_speed * 2
        self.rect.x = random.randrange(2000, 2500)
        self.rect.y = random.randrange(0, size[1]-self.height)

    def update(self):
        self.rect.x = self.rect.x - self.speed #obstacles move to the left
        if self.rect.x <= 0:
            self.rect.x = random.randrange(2000, 2500)
            self.rect.y = random.randrange(0, size[1]-self.height)

