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
        self.skin5 = Button(RED, 700, 50, 200, 30, "RED SKIN")
        self.skin6 = Button(ORANGE, 700, 150, 200, 30, "ORANGE SKIN")
        self.skin7 = Button(PURPLE, 700, 250, 200, 30, "PURPLE SKIN")

    def skin_selection(self, event, skin, player, colour, coin_total):
        if event == pygame.MOUSEBUTTONDOWN and skin.mouse_pos:
            player.update_col(colour)
            with open(COINFILE, 'w') as file: # open text file
                file.write(str(coin_total)) # save new value in text file
            
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

class MapObject(pygame.sprite.Sprite):
    # Define the constructor
    def __init__(self, color, x, y, w):
        # Call the sprite constructor
        super().__init__()
        # Set the position of the sprite
        self.image = pygame.Surface([w, w])
        self.image.fill(color) # fill sprite with the color
        self.rect = self.image.get_rect()
        self.rect.center = (w/2, w/2)
        self.rect.x = x * w + 1000 # set initial x coordinate
        self.rect.y = y * w # set initial y coordinate
        self.speed = game_speed # set speed
    
    def update(self):
        self.rect.x -= self.speed

class Enemy(MapObject):
    # Define the constructor
    def __init__(self, color, x, y, w, game):
        # Call the sprite constructor
        MapObject.__init__(self, color, x, y, w)
        # Set the position of the sprite
        self.rect.x = x * w - 50 # set initial x coordinate
        self.speed = 1 # set enemy speed
        self.game = game

    def update(self):
        pl = self.game.player.body[0]
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
        self.width = w
        self.x = x
        self.y = y
        self.body_len = 5 # number of blocks to be in the body
        self.body = [] # list of body blocks 
        for i in range(0, self.body_len):
            # append a sprite to the list of blocks 
            self.body.append(pygame.sprite.Sprite())            
            elem = self.body[i]        
            elem.image = pygame.Surface([w, w]) # surface of the sprite
            elem.image.fill(BLUE) # fill sprite with the color
            elem.rect = elem.image.get_rect()
            # each block's x coordinate decreases by one block on the map
            # this is so the blocks don't appear in the same spot
            elem.rect.x = x - i * w 
            elem.rect.y = y            
            elem.speed = 0
        # player head is the front block of the list         
        self.sprite = self.body[0]

    def move(self, up=True):
        # function to move like a snake 
        change = self.width * (-1 if up else 1)
        # up is passed in from main program and
        # changes depending on which arrow key is pressed
        self.body[0].rect.y += change # update y coordinate of the head        
        for i in range(1, self.body_len): # check each part of the player body
            # distance between each successive body part
            dist = self.body[i].rect.y - self.body[i-1].rect.y            
            # check if vertical distance from one block to the successive is above
            # the block width          
            if abs(dist) > abs(change): 
                # if so then make sure the previous block doesn't detach from the block in front 
                delta = -change
                self.body[i].rect.y = self.body[i-1].rect.y + delta
        # player can't go off the screen
        if self.sprite.rect.y >= SCREEN_HEIGHT: # floor            
            self.sprite.rect.y = SCREEN_HEIGHT - self.width
        if self.sprite.rect.y <= 0: # ceiling
            self.sprite.rect.y = 0

    def straighten(self): # re-align the body 
        for i in range(1, self.body_len):
            # direction to re-align in is up (negative) is the previous block 
            # is under the block in front and vice versa
            direction = -1 if self.body[i].rect.y > self.body[0].rect.y else 1
            # until each successive body part is in line, update their y direction 
            if self.body[i].rect.y != self.body[0].rect.y:
                self.body[i].rect.y += self.width * direction 
        
            
    def update_col(self, col):
        self.col = col
        for i in range(0, self.body_len):
            self.body[i].image.fill(self.col)

class Bullets(pygame.sprite.Sprite):
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

    def update(self):
        self.rect.x -= game_speed * 2 #bullets move left
        
class Block(MapObject):
    # Define the constructor
    def __init__(self, game, color, x, y, w, oscillating=False):
        # Call the sprite constructor
        MapObject.__init__(self, color, x, y, w)       
        # Create a sprite and fill it with colour
        self.game = game 
        self.osc_speed = oscillating_speed
        self.oscillating = oscillating
        pass

    def update(self):
        self.elapsed = pygame.time.get_ticks()
        self.rect.x -= game_speed
        if self.oscillating and self.game.score > 400:
            if self.rect.y >= SCREEN_HEIGHT - 20:
                self.osc_speed *= -1
            if self.rect.y <= 0:
                self.osc_speed *= -1
            self.rect.y += self.osc_speed
        
            
        
class Lives(MapObject):
    # Define the constructor
    def __init__(self, color, x, y, w):
        # Call the sprite constructor
        MapObject.__init__(self, color, x, y, w)
        # Create a sprite and fill it with colour
        pass
    pass

class Coins(MapObject):
    # Define the constructor
    def __init__(self, color, x, y, w):
        # Call the sprite constructor
        MapObject.__init__(self, color, x, y, w)
        # Create a sprite and fill it with colour
        pass
    pass

