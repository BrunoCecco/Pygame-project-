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
        self.image = pygame.Surface([SCREEN_WIDTH, SCREEN_HEIGHT])
        self.image.fill(BLUE) # fill sprite with the color
        self.rect = self.image.get_rect()
        self.rect.x = 0 
        self.rect.y = 0
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
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
    def __init__(self, x, y, w):
        # Call the sprite constructor
        super().__init__()
        # Set the position of the sprite
        self.image = pygame.Surface([w, w])
        self.image.fill(RED) # fill sprite with the color
        self.rect = self.image.get_rect()
        self.rect.x = x * w - 50 # set initial x coordinate
        self.rect.y = y * w # set initial y coordinate
        self.speed = 1 # set enemy speed

    def move(self,  pl):
        if pl.rect.x > self.rect.x:
            self.rect.x += self.speed
        if pl.rect.y < self.rect.y:
            self.rect.y -= self.speed
        elif pl.rect.y > self.rect.y:
            self.rect.y += self.speed
            
# tbd - sort out enemy spawning

class Player():
    # Define the constructor
    def __init__(self, x, y, w):
        self.speed = 0
        self.width = w
        self.body_len = 8
        self.body = []
        for i in range(0, self.body_len):
            self.body.append(pygame.sprite.Sprite())
            elem = self.body[i]
            elem.image = pygame.Surface([w, w])
            elem.image.fill(GREEN)
            elem.rect = elem.image.get_rect()
            elem.rect.x = x - i * w
            elem.rect.y = y
            elem.speed = 0
        self.sprite = self.body[0]

    def move(self, up=True):
        change = self.width * (-1 if up else 1)
        self.body[0].rect.y += change
        for i in range(1, self.body_len): # check each part of the player body
            dist = self.body[i].rect.y - self.body[i-1].rect.y
            if abs(dist) > abs(change): # re-align if not in line
                delta = -change
                self.body[i].rect.y = self.body[i-1].rect.y + delta
        if self.sprite.rect.y >= SCREEN_HEIGHT: #floor
            self.sprite.rect.y = SCREEN_HEIGHT - self.width
        if self.sprite.rect.y <= 0: #ceiling
            self.sprite.rect.y = 0

    def straighten(self): #re-align body 
        for i in range(1, self.body_len):
            direction = -1 if self.body[i].rect.y > self.body[0].rect.y else 1
            if self.body[i].rect.y != self.body[0].rect.y:
                self.body[i].rect.y += self.width * direction 
        
            
    def update_col(self, col):
        self.col = col
        for i in range(0, self.body_len):
            self.body[i].image.fill(self.col)

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
        
class Block(pygame.sprite.Sprite):
    # Define the constructor
    def __init__(self, color, x, y, w):
        # Call the sprite constructor
        super().__init__()
        # Create a sprite and fill it with colour
        self.image = pygame.Surface([w,w])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x * w + 1000
        self.rect.y = y * w

    def update(self):
        self.rect.x -= game_speed
        
class Lives(pygame.sprite.Sprite):
    # Define the constructor
    def __init__(self, color, x, y, w):
        # Call the sprite constructor
        super().__init__()
        # Create a sprite and fill it with colour
        self.image = pygame.Surface([w,w])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x*w + 1000
        self.rect.y = y*w
        self.speed = game_speed
        
    def update(self): # create illusion that player is moving right
        self.rect.x -= self.speed #move to the left

class Coins(pygame.sprite.Sprite):
    # Define the constructor
    def __init__(self, color, x, y, w):
        # Call the sprite constructor
        super().__init__()
        # Create a sprite and fill it with colour
        self.image = pygame.Surface([w,w])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x*w + 1000
        self.rect.y = y*w
        self.speed = game_speed
        
    def update(self): # create illusion that player is moving right
        self.rect.x -= self.speed #move to the left

class Background(pygame.sprite.Sprite):
    # Define the constructor
    def __init__(self, x, y, w):
        # Call the sprite constructor
        super().__init__()
        # Create a sprite and fill it with colour
        self.image = pygame.Surface([w,w])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x*w + 1000
        self.rect.y = y*w
        self.speed = game_speed
        
    def update(self): # create illusion that player is moving right
        self.rect.x -= self.speed #move to the left


