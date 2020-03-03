# sprite classes for project game
import pygame
import random
import math
from settings import *


def draw_text(col, x, y, size, text):
    #Draw text onto the screen
    font = pg.font.Font(None, size) # set font
    text_surface = font.render(text, True, col)
    textRect = text_surface.get_rect()
    textRect.midtop = (x, y) # set top middle of the text
    screen.blit(text_surface, textRect) # display text on screen

class InputBox:
    # text box to enter name
    def __init__(self, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = True
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    print(self.text)
                    self.name = self.text
                    self.text = ''
                    with open(HS_name, 'w') as file: # open text file
                        file.write(self.name) # save new name in text file
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                    
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)

        
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
        self.skin1 = Button(GREEN, 50, 50, 200, 30, "GREEN SKIN")
        self.skin2 = Button(YELLOW, 50, 150, 200, 30, "YELLOW SKIN")
        self.skin3 = Button(BLUE, 50, 250, 200, 30, "BLUE SKIN")
        self.skin4 = Button(WHITE, 50, 350, 200, 30, "WHITE SKIN")

                
class Button(pygame.sprite.Sprite):
    # Define the constructor
    def __init__(self, col, x, y, w, h, text):
        super().__init__()
        self.image = pygame.Surface([w, h])
        self.image.fill(BLACK) # fill sprite with the color
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = w
        self.height = h
        self.init_col = col
        self.col = col
        self.text = text
        self.mouse_pos = False

    def update(self): # check mouse is in correct position
        mouse = pygame.mouse.get_pos()
        if self.rect.x+self.width > mouse[0] > self.rect.x and self.rect.y+self.height > mouse[1] > self.rect.y:
            self.col = WHITE # change colour of button text
            self.mouse_pos = True # mouse is on the button
        else:
            self.mouse_pos = False
            self.col = self.init_col # change button text colour back to initial state   
        draw_text(self.col, (self.rect.x+(self.width/2)), self.rect.y, self.height+10, self.text) # draw text on button


class Enemy(pygame.sprite.Sprite):
    # Define the constructor
    def __init__(self, width, height, player):
        # Call the sprite constructor
        super().__init__()
        # Set the position of the sprite
        self.image = pygame.Surface([width, height])
        self.image.fill(RED) # fill sprite with the color
        self.rect = self.image.get_rect()
        self.rect.x = -(random.randrange(0, 1000)) # set initial x coordinate
        self.rect.y = 0 # set initial y coordinate
        self.width = width
        self.height = height
        self.speed = 3 # set enemy speed

    
class Player(pygame.sprite.Sprite):
    # Define the constructor
    def __init__(self):
        # Call the sprite constructor
        pygame.sprite.Sprite.__init__(self)
        # Set the position of the sprite
        self.image = pygame.Surface([40, 40])
        self.image.fill(GREEN)
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
            
    def update_col(self, col):
        self.col = col
        self.image.fill(self.col)


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
        self.rect.x -= self.speed #bullets move left


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
        self.rect.x -= self.speed #move to the left


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
        self.rect.x -= self.speed #move to the left


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
        self.rect.x -= game_speed #obstacles move to the left
        if self.rect.x <= 0:
            self.rect.x = random.randrange(1000, 2000) # respawn if they go off the screen
            self.rect.y = random.randrange(0, size[1]-self.height) #respawn in a random position

class Rockets(Obstacle):
    pass

    def update(self): # create illusion that player is moving right
        self.rect.x -= game_speed*2 #obstacles move to the left
        if self.rect.x <= 0:
            self.rect.x = 3000 # respawn if they go off the screen
            self.rect.y = random.randrange(0, size[1]-self.height) #respawn in a random position

