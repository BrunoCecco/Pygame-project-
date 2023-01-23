# import pygame as "pg" to improve readability 
import pygame as pg # this allows me to call it by writing "pg" instead of pygame
import pygame
import random
import math
import itertools

pg.init() # initialize pygame so its functions can be used

# define key colours as rgb tuples 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
TURQUOISE = (64,224,208)
LIGHTGREY = (100, 100, 100)
DARKGREY = (40, 40, 40)
RED = (245, 50, 17)
ORANGE = (255,165,0)
DESERT_ORANGE = (200,142,70)
PURPLE = (148,0,211)
VIOLET = (238,130,238)
PINK = (255,192,203)

COLOR_INACTIVE = (0, 100, 0)
COLOR_ACTIVE = (0, 200, 0)

FONT = pg.font.Font(None, 32)

# define screen dimensions and create the screen with pygame's display function
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
BLOCK_SIZE = 20
screen = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT]) # create screen 

# define high score and coin files as strings
HSFILE = "Textfiles\highscore.txt"
HS_name = "Textfiles\hs_name.txt"
COINFILE = "Textfiles\coins.txt"
game_speed = 4 # define game speed (speed which obstacles will inherit)
oscillating_speed = 1

#################

def draw_text(col, x, y, size, text): #Draw text onto the screen    
    font = pg.font.Font(None, size) # define font 
    text_surface = font.render(text, True, col) # create surface for the text
    textRect = text_surface.get_rect() # make the surface rectangular
    textRect.midtop = (int(x), int(y)) # set top middle of the text
    screen.blit(text_surface, textRect) # display (blit) text onto the screen

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
        self.image.fill(BLACK) # fill sprite with the color
        self.rect = self.image.get_rect()
        self.rect.x = 0 # x coordinate 
        self.rect.y = 0 # y coordinate 
        self.width = SCREEN_WIDTH # takes up the whole screen
        self.height = SCREEN_HEIGHT
        # instantiate all the different skins as buttons 
        self.back_button = Button(WHITE, 50, 50, 200, 30, "BACK")
        self.skin1 = Button(GREEN, 50, 150, 200, 30, "GREEN SKIN")
        self.skin2 = Button(YELLOW, 50, 250, 200, 30, "YELLOW SKIN")
        self.skin3 = Button(BLUE, 50, 350, 200, 30, "BLUE SKIN")
        self.skin4 = Button(WHITE, 700, 50, 200, 30, "WHITE SKIN")
        self.skin5 = Button(RED, 700, 150, 200, 30, "RED SKIN")
        self.skin6 = Button(ORANGE, 700, 250, 200, 30, "ORANGE SKIN")
        self.skin7 = Button(PURPLE, 700, 350, 200, 30, "PURPLE SKIN")        
        self.skins_bought = []

    def skin_selection(self, event, skin, player, colour, coin_total):        
        # function to change the players' skin
        # if skin button clicked on
        if event == pygame.MOUSEBUTTONDOWN and skin.mouse_pos:
            if skin not in self.skins_bought: # if skin has not been bought yet
                self.skins_bought.append(skin) # add skin to bought skin array
                # if the user presses on a skin button             
                if coin_total > 50: # if player has enough coins 
                    player.update_col(colour) # update player's skin colour 
                    ct = coin_total - 50 # take of 10 coins
                    with open(COINFILE, 'w') as file: # open text file                
                        file.write(str(ct)) # save new value in text file  
            else: # if skin was already bought 
                player.update_col(colour) # update player's skin colour 

            
class Button(pygame.sprite.Sprite):
    # Define the constructor
    def __init__(self, col, x, y, w, h, text):
        super().__init__()
        self.image = pygame.Surface([w, h])
        self.image.fill(BLACK) # fill sprite with the color
        self.rect = self.image.get_rect()
        self.rect.x = int(x) # x coordinate
        self.rect.y = int(y) # y coordinate 
        self.width = w
        self.height = h
        self.init_col = col # initial button colour 
        self.col = col # colour when clicked 
        self.text = text # text on the button
        self.mouse_pos = False # mouse position is initially not on the button

    def update(self): # check mouse is in correct position
        mouse = pygame.mouse.get_pos() # get mouse position 
        # if the mouse position is within button's boundaries
        if self.rect.x+self.width > mouse[0] > self.rect.x and self.rect.y+self.height > mouse[1] > self.rect.y:
            self.col = WHITE # change colour of button text to show it is being hovered over
            self.mouse_pos = True # mouse is on the button
        else:
            self.mouse_pos = False
            self.col = self.init_col # change button text colour back to initial state   
        # draw text on button
        draw_text(self.col, (self.rect.x+(self.width/2)), self.rect.y, self.height+10, self.text) 

class MapObject(pygame.sprite.Sprite):
    # Define the constructor
    def __init__(self, x, y, w, image):
        # Call the sprite constructor
        super().__init__()
        # Set the position of the sprite
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x = x * w + 1000 # set initial x coordinate
        self.rect.y = y * w # set initial y coordinate
        self.speed = game_speed # set speed
    
    def update(self):
        self.rect.x -= self.speed  
        # if background object goes off the screen completely, reset its x coordinate
        if self.rect.x == -SCREEN_WIDTH:
            self.rect.x = 1000   

class Background(MapObject):
    # Define the constructor
    def __init__(self, x, y, w, image):
        # Call the sprite constructor
        MapObject.__init__(self, x, y, w, image)
        self.rect.x = x
        pass 
    pass


class Obstacle(MapObject):
    # Define the constructor
    def __init__(self, game, x, y, w, image, oscillating=False):
        # Call the sprite constructor
        MapObject.__init__(self, x, y, w, image)
        # Create a sprite and fill it with colour
        self.game = game 
        self.osc_speed = oscillating_speed # speed at which obstacles will move up and down
        self.oscillating = oscillating # boolean value false if obstacle will not oscillate        
        pass

    def update(self):
        self.rect.x -= game_speed # object moves left    
        # obstacles should only start oscillating when the game score is above 50
        if self.oscillating and self.game.score > 50:
            # reverse oscillating movement if the obstacle reaches the end of the screen             
            if self.rect.y >= SCREEN_HEIGHT - 20: 
                self.osc_speed *= -1  
            if self.rect.y <= 0:
                self.osc_speed *= -1             
            self.rect.y += self.osc_speed 

class Enemy(MapObject):
    # Define the constructor
    def __init__(self, x, y, w, image, game):
        # Call the sprite constructor
        MapObject.__init__(self, x, y, w, image)
        # Set the position of the sprite
        self.rect.x = x * w # set initial x coordinate 
        self.speed = 1 # set enemy speed to be slower than the map objects' speed
        self.game = game # passed in the game class 

    def update(self):
        pl = self.game.player.sprite # game class gives access to the player
        if pl.rect.x > self.rect.x: # if player is to the right of the enemy
            self.rect.x += self.speed # enemy should move right
        if pl.rect.y < self.rect.y: # if player is above enemy
            self.rect.y -= self.speed # enemy should move up
        elif pl.rect.y > self.rect.y: # if player is below enemy
            self.rect.y += self.speed # enemy should move down
            
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
            elem.image.fill(RED) # fill sprite with the color
            elem.rect = elem.image.get_rect()
            # each block's x coordinate decreases by one block on the map
            # this is so the blocks don't appear in the same spot
            elem.rect.x = round(x - i * w) 
            elem.rect.y = y      
            elem.speed = 0
        # player head is the front block of the list         
        self.sprite = self.body[0]
        self.sprite.image = pygame.image.load("images/snakehead.png")
        self.rect = self.sprite.image.get_rect() 


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
        for i in range(1, self.body_len):
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
            
class Lives(MapObject):
    # Define the constructor
    def __init__(self, x, y, w, image):
        # Call the sprite constructor
        MapObject.__init__(self, x, y, w, image)
        # Create a sprite and fill it with colour
        pass
    pass

class Coins(MapObject):
    # Define the constructor
    def __init__(self, x, y, w, image):
        # Call the sprite constructor
        MapObject.__init__(self, x, y, w, image)
        pass
        # Create a sprite
    pass

################

# game class
class Game(pg.sprite.Sprite):
    # Define the constructor
    def __init__(self):
        # Call the sprite constructor
        pg.sprite.Sprite.__init__(self)
        pg.init() # initialise pygame   
        self.font = FONT # define font type
        self.clock = pg.time.Clock() # initialize pygame clock to keep track of time
        # clock will be used to define the frame rate of the game
        # define boolean variable that determines whether the game is running or not
        self.running = True 
        self.coin_total = self.readfile(COINFILE)
        self.highscore = self.readfile(HSFILE) # read the highscore from the text file
        self.pause = False 
        self.play_music() # play music        
        # define sound effects 
        # obstacle_collision = pygame.mixer.Sound('Music\obstacle_collision.wav')
        # coin_collision = pygame.mixer.Sound('Music\coin_collision.wav')
        # life_collision = pygame.mixer.Sound('Music\life_collision.wav')
        # enemy_collision = pygame.mixer.Sound('Music\enemy_collision.wav')
        self.player = Player(SCREEN_WIDTH/2, 200, BLOCK_SIZE) # create a player head   
        self.endtime = 0
        
        # instantiate input box
        self.input_box = InputBox(SCREEN_WIDTH//2 - 100, 50, 140, 30)
        self.hs_name = self.readfile(HS_name, True) # read the highscore name from the file

    def readfile(self, name, string = False):
        with open(name, 'r') as file: # open file if it exists
            try: # runs if possible
                return (int(file.read()) if not string else str(file.read()))
            except:
                return 0
            
    def writefiles(self, name, var):
        with open(name, 'w') as file: # open text file
            file.write(str(var)) # save new value in text file

    def play_music(self): # function to play background music
        song_q = ['Music\dontworry.mp3', 'Music\jinglebells.mp3', 'Music\chainsmokers.mp3']
        pygame.mixer.music.load(random.choice(song_q)) # load random song
        #pg.mixer.music.play() # play random song from list

    def screen_width(self): # Function to define screen width in blocks
        return int(SCREEN_WIDTH // BLOCK_SIZE)

    def screen_height(self): # Function to define screen height in blocks
        return int(SCREEN_HEIGHT // BLOCK_SIZE)

    def create_groups(self):
        # function to create the sprite groups
        self.player_group = pg.sprite.Group()
        self.all_sprites_group = pg.sprite.Group()  # create a sprite group to contain all sprites        
        self.obstacle_group = pg.sprite.Group()
        self.coin_group = pg.sprite.Group() 
        self.life_group = pg.sprite.Group()
        self.enemy_group = pg.sprite.Group()
        self.bullet_group = pg.sprite.Group()
        self.button_group = pg.sprite.Group()
        self.shop_group = pg.sprite.Group()
        self.background_group = pg.sprite.Group()

    def create_map(self):
        # create 2D array (map) with all sprites 
        self.game_map = [] # initialize 2D array  
        self.new_row = [] # initialize rows

        # randomize obstacle x and y coordinates
        self.obstacle_randx = random.randrange(0, self.screen_width())
        self.obstacle_randy = random.randrange(0, self.screen_height())        
        # randomize coin x and y coordinates
        self.coin_rand = random.randrange(0, self.screen_height())
        # randomize life x and y coordinates
        self.life_rand = random.randrange(0, self.screen_height())
        # create sprite group for all map objects        
        # two for loops to loop through x and y axis of the screen
        for i in range (0, self.screen_height()): # y axis
            for j in range (0, self.screen_width()): # x axis
                # if random obstacle coordinates are the current counter                
                if j == self.obstacle_randx or i == self.obstacle_randy:
                    self.new_row.append(1) # 1 indicates obstacle
                    # randomize coords again so obstacles don't spawn in the same place
                    self.obstacle_randx = random.randrange(0, self.screen_width())
                    self.obstacle_randy = random.randrange(0, self.screen_height())
                if j == self.coin_rand and i == self.coin_rand:
                    self.new_row.append(2) # 2 indicates coin    
                    # randomize coords again so obstacles don't spawn in the same place
                    self.coin_rand = random.randrange(0, self.screen_height())                
                if j == 3 and i == 1: # enemy starts in the top left
                    self.new_row.append(3) # 3 indicates enemy
                if j == self.life_rand and i == self.life_rand:
                    self.new_row.append(4) # 4 indicates life power up
                else: # if the current counter isn't equal to random coordinates, append 0
                    self.new_row.append(0) # 0 indicates background
            self.game_map.append(self.new_row) # put new row into map list
            self.new_row = [] # create new empty row
            
        # display map - depending on number in the array, instantiate a sprite
        for y in range(0, self.screen_height()): # y-axis of the map  
            for x in range(0, self.screen_width()): # x-axis of the map
                if self.game_map[y][x] == 1: # if value is 1, instantiate an obstacle
                    z = random.randint(0, 4)
                    images = ["Images/rock1.png", "Images/rock2.png", "Images/rock3.png"]
                    if z == 0: # only around 1/5 of blocks are made to oscillate
                        self.obstacle = Obstacle(self, x, y, BLOCK_SIZE, "Images/tumbleweed.png", True)
                    else:
                        self.obstacle = Obstacle(self, x, y, BLOCK_SIZE, random.choice(images))  
                    self.obstacle_group.add(self.obstacle) # add obstacle to map group
                elif self.game_map[y][x] == 2:
                    self.coins = Coins(x, y, BLOCK_SIZE, "Images/coin.png")
                    self.coin_group.add(self.coins)                                    
                elif self.game_map[y][x] == 3:
                    self.enemy = Enemy(x, y, BLOCK_SIZE, "Images/enemy.png", self)
                    self.enemy_group.add(self.enemy)
                elif self.game_map[y][x] == 4:
                     # instantiate life power up
                    self.life = Lives(x, y, BLOCK_SIZE, "Images/life.png")
                    self.life_group.add(self.life) # add it to the life group                     
                else: # if it's 0, do nothing
                    continue # backgrounds do not need to be instantiated            

        self.all_sprites_group.add(self.life_group, self.enemy_group, self.obstacle_group, self.coin_group) # add sprites to all sprites group
    
        # compare each sprite on the map with each other, and if they overlap, remove one of the sprites.
        # this will prevent overlapping objects on the screen 
        for sprite1, sprite2 in itertools.combinations(self.all_sprites_group, 2):
            if sprite1.rect.colliderect(sprite2.rect): # if they collide 
                sprite2.kill() # remove sprite 2 from the all sprites group
    

    def new_game(self):# start a new game                
    
        self.score = 0 # player starts with 0 score
        self.lives = 5 # player starts with 5 lives
        self.create_map()

        # instantiate two (alternating) backgrounds 
        self.bg = Background(0, 0, BLOCK_SIZE, "./Images/desert_background.jpg") # first background which appears first
        self.bg2 = Background(1000, 0, BLOCK_SIZE, "./Images/desert_background.jpg") # second background which appears after the first
        self.background_group.add(self.bg, self.bg2) # add backgrounds to background group

        self.player_group.add(self.player.sprite) # add to player group
        self.all_sprites_group.add(self.player_group) # add player to all sprites group

        self.run() # call run function

    def run(self):
        # run game loop
        self.playing = True
        while self.playing: 
            self.clock.tick(60) # define frames per second
            self.events() 
            self.update()
            self.draw()
        
    def update(self):
        # game loop update function
        self.all_sprites_group.update() # update all sprites
        self.background_group.update() # update background group

        for s in self.all_sprites_group:
            if s.rect.x < -50: # if the sprite goes off the screen
                s.kill() # remove the sprite from ll groups so it doesn't exist anymore
            # respawn obstacles by creating the map again with new random positions
            if len(self.obstacle_group) < 30: # if there are only some obstacles on the screen
                self.create_map() # create the map again so obstacles respawn
        
        for c in pygame.sprite.groupcollide(self.player_group, self.coin_group, False, True):
            # if there's a collision add coins to player
            self.coin_total += 1
            self.writefiles(COINFILE, self.coin_total)      
            #self.coin_collision.play()

       # check for collision with bullets and enemy
        pygame.sprite.groupcollide(self.bullet_group, self.enemy_group, False, True)   

        # check for collision between player and obstacles 
        for i in pygame.sprite.groupcollide(self.player_group, self.obstacle_group, False, True):
            # if there's a collision decrease lives and delete obstacle from map
            self.lives -= 1       
            #self.obstacle_collision.play()   

        # check for collision with life objects and player
        for b in pygame.sprite.groupcollide(self.player_group, self.life_group, False, True):
             # if there's a collision increase lives
            self.lives += 1     
            #self.life_collision.play()             

        # check for collision with enemy and player
        for i in pygame.sprite.groupcollide(self.player_group, self.enemy_group, False, True):
            # if there's a collision remove 3 lives and remove enemy from the map
            self.lives -= 3
            #self.enemy_collision.play()


        curr_time = pg.time.get_ticks() # get current time
        if curr_time - self.endtime > 75: # re-align player every x milliseconds
            self.player.straighten()
            self.endtime = curr_time

        if self.lives <= 0: # if lives run out, game over            
            self.playing = False     
            for s in self.all_sprites_group:
                s.kill() # remove all sprites from screen
            for b in self.background_group:
                b.kill() # remove all sprites from screen
        
        self.score += 1


    def events(self):
        # keyboard events
        keys = pg.key.get_pressed()

        while self.pause == True: # while paused
            for event in pg.event.get():
                if event.type==pg.KEYUP: # wait for key to be pressed
                    if event.key==pg.K_p: # if key "p" is pressed, resume the game
                        self.pause = False

        if keys[pg.K_UP] or keys[pg.K_DOWN]: # player moves up or down
            curr_time = pg.time.get_ticks() # get current time
            if curr_time - self.endtime > 20:
                self.endtime = curr_time
                self.player.move(False if keys[pg.K_DOWN] else True)  
        
        for event in pg.event.get():
            if event.type == pg.QUIT: # if user presses exit button, game ends
                self.playing = False
                self.running = False
            if event.type == pg.KEYUP:# if the user presses a key
                if event.key == pg.K_p: # if key pressed is p
                    self.pause = True # pause the game
                if event.key == pygame.K_SPACE: # player shoots a bullet
                    self.bullet = Bullets(WHITE, self.player.body[0].rect.x, self.player.body[0].rect.y)
                    self.all_sprites_group.add(self.bullet)
                    self.bullet_group.add(self.bullet)                      
                    
    def draw(self):
        # drawing on screen
        screen.fill(BLACK) # set background to blacks
        self.background_group.draw(screen) # draw background onto screen before anything
        self.all_sprites_group.draw(screen) # draw sprites onto screen        
        draw_text(RED, 100, 50, 50, "SCORE: %d" % self.score) # display score
        draw_text(RED, 100, 110, 50, "COINS: %d" % self.coin_total) # display coin total        
        draw_text(RED, 100, 170, 50, "LIVES: %d" % self.lives) # display lives
        pg.display.flip() # after drawing everything, flip the display so it updates

    def menu(self): # menu to be displayed before game starts
        self.create_groups()
        self.player = Player(SCREEN_WIDTH/2, 200, BLOCK_SIZE) # create a player head
        for i in range(0, self.player.body_len): # add player body to sprite groups
            self.player_group.add(self.player.body[i]) # add body to player group
        self.all_sprites_group.add(self.player_group) # add player to all sprites group

        self.player_group.add(self.player.sprite) # add to player group
        self.all_sprites_group.add(self.player_group) # add player to all sprites group        
        self.waiting = True # game does not start until waiting is false
        # show start screen
        screen.fill(BLUE) # menu background is blue 
        self.entered = False # hasn't entered shop yet
        # display a shop button on the menu 
        self.shop_button = Button(GREEN, SCREEN_WIDTH/2-50, SCREEN_HEIGHT/2, 100, 35, "Shop")
        self.button_group.add(self.shop_button) # add the button to the button sprite group
        self.shop = Shop() # instantiate shop  
        s = self.shop # abbreviate so the skins can be added easily   
        # add all skins and the shop to the shop group
        self.shop_group.add(s,s.back_button,s.skin1,s.skin2,s.skin3,s.skin4, s.skin5, s.skin6, s.skin7) 
        # text to be displayed on menu       
        draw_text(GREEN, SCREEN_WIDTH/2, SCREEN_HEIGHT/3, 50, "Highscore: %d" % self.highscore)
        draw_text(GREEN, SCREEN_WIDTH/2, SCREEN_HEIGHT/1.5, 50, "Press p to play")
        draw_text(GREEN, SCREEN_WIDTH/2, SCREEN_HEIGHT/1.2, 50, "Arrows to move, space to shoot")
        while self.waiting: # while menu is true
            self.menu_events() # wait for player to press a key    
            self.button_group.draw(screen)
            self.button_group.update()
            pg.display.flip()  # update menu screen

    def menu_events(self): # when player presses a key start the game
        # read coin file to see for updates from skin purchases, and update coin total
        self.coin_total = self.readfile(COINFILE) 
        for event in pg.event.get():
            self.input_box.handle_event(event)
            if event.type == pg.QUIT: # if quit key pressed, end game
                self.running = False          
            if event.type == pg.KEYUP and self.input_box.color == COLOR_INACTIVE: # if a key is pressed 
                if event.key == pg.K_p: # check if the key pressed is p, if so start the game
                    self.waiting = False # waiting is false so menu_events function stops 
                    self.entered = False # leave shop if the shop button has been clicked
                    for i in range(0, self.player.body_len): # add player body to sprite groups
                        self.player_group.add(self.player.body[i]) # add body to player group
                    self.all_sprites_group.add(self.player_group) # add player to all sprites group                         
                    
            if event.type == pg.MOUSEBUTTONUP and self.shop_button.mouse_pos:
                self.shop_button.mouse_pos = False
                # if the user clicks the shop button 
                self.entered = True # enter shop
                self.button_group.remove(self.shop_button) # remove shop button from screen
            if event.type == pg.MOUSEBUTTONUP:
                if self.shop.back_button.mouse_pos and self.entered:                     
                    for s in self.shop_group:
                        s.kill()
                    self.entered = False
                    self.menu()                
                
            if self.entered: # create shop if shop button pressed                           
                self.shop_group.draw(screen) # draw shop on the screen
                self.shop_group.update()
                self.player_group.draw(screen)
                self.player_group.update()
                # draw coin total and cost of coins onto the screen
                draw_text(YELLOW, SCREEN_WIDTH/2, 50, 50, "COINS: %d" % self.coin_total) 
                draw_text(YELLOW, SCREEN_WIDTH/2, 100, 30, "(All skins cost 50 coins)") 
                pg.display.flip()        
                pl = self.player # abbreviate
                ct = self.coin_total # abbreviate
                et = event.type # abbreviate
                s = self.shop
                # check for skins button presses
                s.skin_selection(et, s.skin1, pl, GREEN, ct)
                s.skin_selection(et, s.skin2, pl, YELLOW, ct)
                s.skin_selection(et, s.skin3, pl, BLUE, ct)
                s.skin_selection(et, s.skin4, pl, WHITE, ct)
                s.skin_selection(et, s.skin5, pl, RED, ct)
                s.skin_selection(et, s.skin6, pl, ORANGE, ct)
                s.skin_selection(et, s.skin7, pl, PURPLE, ct) 
             
        self.input_box.update()
        self.input_box.draw(screen)

    def game_over(self): # game over function 
        self.waiting = True 
        screen.fill(BLUE) # game over screen background
        if self.score > self.highscore: # new highscore
            self.highscore = self.score
            draw_text(GREEN, SCREEN_WIDTH/2, SCREEN_HEIGHT/3, 50, "NEW HIGHSCORE! - " + str(self.highscore) + " by " + self.hs_name)
            self.writefiles(HSFILE, self.highscore)
        else:
            draw_text(GREEN, SCREEN_WIDTH/2, SCREEN_HEIGHT/3, 50, "Highscore: - " + str(self.highscore) + " by " +self.hs_name)
        draw_text(GREEN, SCREEN_WIDTH/2, SCREEN_HEIGHT/1.5, 50, "Game over, press any key to play")
        draw_text(GREEN, SCREEN_WIDTH/2, SCREEN_HEIGHT/1.2, 50, "Score: %d" % self.score)
        # game over screen
        pg.display.flip()
        while self.waiting:
            self.shop_button = Button(GREEN, SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 100, 35, "Shop")
            self.menu_events()                                                        
            
game = Game() # instantiate game class
game.menu() # run menu before game starts
while game.running: # while running variable is true
    game.new_game() # call new game method
    game.game_over() # when the player runs out of lives, call the game over function
pg.quit()
    
##################


###################



