# project game main loop

import pygame as pg
import random, math
from settings import *
from classes import *
from os import path

# make floor and a ceiling that randomly change height
# game class
class Game(pg.sprite.Sprite):
    # Define the constructor
    def __init__(self):
        # Call the sprite constructor
        pg.sprite.Sprite.__init__(self)
        pg.init() # initialise pygame   
        self.font = FONT 
        self.clock = pg.time.Clock()
        self.running = True
        
        self.highscore = self.readfile(HSFILE)
        self.coin_total = self.readfile(COINFILE)
        self.hs_name = self.readfile(hsname, True)
        self.play_music() # play music        
        self.sprite_groups() # create sprite groups
        self.block_size = 20 # block width (size)

        #create text boxes
        self.input_box = InputBox(SCREEN_WIDTH/2 - 100, 50, 140, 30)
        self.endtime = 0
    
    # make sound effects
    def play_music(self):
        song_q = ['Music/dontworry.mp3', 'Music/jinglebells.mp3', 'Music/chainsmokers.mp3']
        pygame.mixer.music.load(random.choice(song_q)) # load random song
        #pg.mixer.music.play() # play random song from list

    def readfile(self, name, string = False):
        with open(name, 'r') as file: # open file if it exists
            try: # runs if possible
                if not string:
                    return int(file.read())
                else:
                    return file.read()
            except:
                return 0
            
    def writefiles(self, file_name, var):
        with open(file_name, 'w') as file: # open text file
            file.write(str(var)) # save new value in text file

    # Screen width in blocks
    def screen_width(self):
        return int(SCREEN_WIDTH / self.block_size)

    # Screen height in blocks
    def screen_height(self):
        return int(SCREEN_HEIGHT / self.block_size)
        
    def randomize_spawn(self):
        self.block_randx = random.randrange(0, self.screen_width())
        self.block_randy = random.randrange(0, self.screen_height())
        self.coin_rand = random.randrange(0, self.screen_height())
        self.live_rand = random.randrange(0, self.screen_height())

    def create_map(self):
        # create 2D array (map) with all sprites 
        self.game_map = [] # initialize 2D array  
        self.new_row = [] # initialize rows
        self.randomize_spawn()

        # random spawn positions
        for i in range (0, self.screen_height()):
            for j in range (0, self.screen_width()):
                if j == 3 and i == self.screen_height()/2:
                    self.new_row.append(4) # 4 indicates enemy
                elif j == self.coin_rand and i == self.coin_rand:
                    self.new_row.append(3) # 3 indicates coin
                elif j == self.live_rand and i == self.live_rand:
                    self.new_row.append(2) # 2 indicates life
                elif j == self.block_randx or i == self.block_randy:
                    self.new_row.append(1) # 1 indicates obstacle
                    self.randomize_spawn()
                else:
                    self.new_row.append(0) # 0 indicates background
            self.game_map.append(self.new_row) # put new row into map list
            self.new_row = [] # create new empty row
    
        # tbd - display obstacles randomly
        # display map - if depending on number in array, instantiate a sprite
        for y in range(0, self.screen_height()): # y-axis of the map  
            for x in range(0, self.screen_width()): # x-axis of the map
                if self.game_map[y][x] == 1: # if contents is 1, draw block
                    z = random.randint(0, 4)
                    if z == 1: # only around 1/4 of blocks are made to oscillate
                        self.block = Block(self, BLUE, x, y, self.block_size, True)
                    else:
                        self.block = Block(self, BLUE, x, y, self.block_size)
                    self.map_group.add(self.block)
                if self.game_map[y][x] == 2: 
                    self.extra_life = Lives(GREEN, x, y, self.block_size) 
                    self.life_group.add(self.extra_life)
                if self.game_map[y][x] == 3:
                    self.coins = Coins(YELLOW, x, y, self.block_size)
                    self.coin_group.add(self.coins)
                if self.game_map[y][x] == 4:
                    self.enemy = Enemy(RED, x, y, self.block_size, self)
                    self.enemy_group.add(self.enemy)
                else:
                    continue


        # TBD - background                  
        # add sprites to all sprites group
        self.all_sprites_group.add(self.enemy_group, self.life_group, self.coin_group, self.map_group)
        
    def new_game(self):# start a new game
        self.score = 0
        self.lives = 5 #player starts with 5 lives

        self.create_map() # create game map
        
        for i in range(0, self.player.body_len): # add player body to sprite groups
            self.player_group.add(self.player.body[i]) # add body to player group
        self.all_sprites_group.add(self.player_group) # add player to all sprites group
        
        self.run()

    def run(self):
        # run game loop
        self.playing = True
        while self.playing:
            self.clock.tick(60) #frames per second
            self.events()
            self.update()
            self.draw()
        
    def update(self):
        
        # game loop update function
        self.all_sprites_group.update() # update all sprites
        for s in self.all_sprites_group:
            if s.rect.x < -50: # respawn sprite if they go off screen
                s.kill()
            # respawn obstacles and bonuses
            if len(self.life_group) + len(self.coin_group) + len(self.map_group) <= 100:
                self.create_map()
        
        #abbreviations
        pl = self.player.sprite 
        en = self.enemy
        
        # collsions
        for b in pygame.sprite.groupcollide(self.player_group, self.map_group, False, True):
             # if there's a collision decrease lives
            self.lives -= 1
        for b in pygame.sprite.groupcollide(self.player_group, self.life_group, False, True):
             # if there's a collision increase lives
            self.lives += 1
        for c in pygame.sprite.groupcollide(self.player_group, self.coin_group, False, True):
            # if there's a collision add coins to player
            self.coin_total += 1
            self.writefiles(COINFILE, self.coin_total)
            
       # check for collision with bullets and enemy
        pygame.sprite.groupcollide(self.bullet_group, self.enemy_group, True, True)
            
        # check for collision with enemy and player
        for b in pygame.sprite.groupcollide(self.player_group, self.enemy_group, False, True):
            self.lives -= 3
        
        # TBD - shortest path for enemy movement to track player
        if self.lives > 0:  # increase player score unless it has run out of lives
            self.score += 1

        if self.lives <= 0: #if lives run out, game over
            self.playing = False
            for s in self.all_sprites_group:
                s.kill() # remove all sprites from screen

        curr_time = pg.time.get_ticks() # get current time
        if curr_time - self.endtime > 75: # re-align player every x milliseconds
            self.player.straighten()
            self.endtime = curr_time

            
    def events(self):
        # keyboard events
        keys = pg.key.get_pressed()
        if keys[pg.K_UP] or keys[pg.K_DOWN]: # player moves up or down
            curr_time = pg.time.get_ticks() # get current time
            if curr_time - self.endtime > 50:
                self.endtime = curr_time
                self.player.move(False if keys[pg.K_DOWN] else True)  
        for event in pg.event.get():
            if event.type == pg.QUIT: # if user presses exit button, game ends
                self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                k = event.key      
                if k == pygame.K_SPACE: # player shoots a bullet
                    self.bullet = Bullets(WHITE, self.player.body[0].rect.x, self.player.body[0].rect.y)
                    self.all_sprites_group.add(self.bullet)
                    self.bullet_group.add(self.bullet)               
                if event.key == pg.K_p:   # pauses game until a key is pressed
                    self.navigation()           

                    
    def draw(self):
        # drawing on screen
        screen.fill(BLACK) # background
        self.all_sprites_group.draw(screen) # draw sprites onto screen
        draw_text(WHITE, 100, 50, 30, "SCORE: %d" % self.score) # display score
        draw_text(WHITE, 100, 80, 30, "LIVES: %d" % self.lives) if self.lives >= 0 else draw_text(WHITE, 100, 80, 30, "LIVES: 0")
        draw_text(WHITE, 100, 110, 30, "COINS: %d" % self.coin_total) # display coin total
        pg.display.flip() # after drawing everything, flip the display
        
    def sprite_groups(self):
        self.all_sprites_group = pg.sprite.Group()  
        self.map_group = pg.sprite.Group()
        self.bullet_group = pg.sprite.Group()
        self.player_group = pg.sprite.Group()
        self.enemy_group = pg.sprite.Group()
        self.life_group = pg.sprite.Group()
        self.coin_group = pg.sprite.Group()
        self.button_group = pg.sprite.Group()
        self.shop_group = pg.sprite.Group()
        
    def menu(self):
        self.sprite_groups() # create sprite groups
        self.player = Player(SCREEN_WIDTH/2, 200, self.block_size) # create a player head
        self.player_group.add(self.player.sprite) # add to player group
        self.all_sprites_group.add(self.player_group) # add player to all sprites group

        self.entered = False # hasn't entered shop yet
        self.waiting = True # 
        self.shop_button = Button(GREEN, SCREEN_WIDTH/2-50, SCREEN_HEIGHT/2, 100, 35, "Shop")
        self.button_group.add(self.shop_button)
        self.shop = Shop() # instantiate shop
        s = self.shop # abbreviate
        # add shop skins to shop group
        self.shop_group.add(s,s.skin1,s.skin2,s.skin3,s.skin4, s.skin5, s.skin6, s.skin7) 
        # show start screen
        screen.fill(BLUE) # menu background
        draw_text(GREEN, SCREEN_WIDTH/2, 20, 50, "Enter Name: ")
        draw_text(GREEN, 150, 50, 50, "Highscore: %d" % self.highscore)
        draw_text(GREEN, 150, 100, 50, "Coins: %d" % self.coin_total)
        draw_text(GREEN, SCREEN_WIDTH/2, SCREEN_HEIGHT/1.5, 50, "Press p to play")
        draw_text(GREEN, SCREEN_WIDTH/2, SCREEN_HEIGHT/1.2, 50, "Arrows to move, space to shoot")
        pg.display.flip()
        while self.waiting: # while menu is true repeat steps
            self.navigation() # wait for player to press a key            
            # create buttons
            self.button_group.draw(screen)
            self.button_group.update()

                
    def game_over(self):
        self.waiting = True
        if not self.running:
            pg.QUIT()
        screen.fill(BLUE) # game over screen background
        draw_text(GREEN, SCREEN_WIDTH/2, 50, 40, "Game over, press any key to play")
        draw_text(GREEN, SCREEN_WIDTH/2, 200, 40, "Score: %d" % self.score)
        if self.score > self.highscore: # new highscore
            self.highscore = self.score
            draw_text(GREEN, SCREEN_WIDTH/2, 300, 40, "NEW HIGHSCORE! " + self.hs_name)
            self.writefiles(HSFILE, self.highscore)
        else:
            draw_text(GREEN, SCREEN_WIDTH/2, 250, 40, ("Highscore: %d - " % self.highscore) + self.hs_name)
        # game over screen
        pg.display.flip()
        while self.waiting:
            self.shop_button = Button(GREEN, SCREEN_WIDTH/2-50, SCREEN_HEIGHT/3, 100, 35, "Shop")
            self.navigation()

    def navigation(self): # wait until player presses a key
        s = self.shop # abbreviate 
        ct = self.coin_total # abbreviate
        for event in pg.event.get():
            et = event.type # abbreviate
            self.input_box.handle_event(event)
            if et == pg.QUIT: # if quit key pressed, end game
                self.running = False
            # if any key is pressed and text box not in use game starts
            if et == pg.KEYUP and self.input_box.color == COLOR_INACTIVE: 
                self.waiting = False # waiting function stops
                self.entered = False # exit shop
                self.play_music() # play music
            # if shop button is pressed shop is created
            if et == pg.MOUSEBUTTONUP and self.shop_button.mouse_pos == True:
                self.entered = True
                self.button_group.remove(self.shop_button) # remove shop button from screen
                
            if self.entered: # create shop if shop button pressed
                self.shop_group.draw(screen)
                self.shop_group.update()
                self.all_sprites_group.draw(screen)
                self.all_sprites_group.update()

                pl = self.player # abbreviate
                # check for skins button presses
                # TBD sort out coins when purchasing skins
                s.skin_selection(et, s.skin1, pl, GREEN, ct)
                s.skin_selection(et, s.skin2, pl, YELLOW, ct)
                s.skin_selection(et, s.skin3, pl, BLUE, ct)
                s.skin_selection(et, s.skin4, pl, WHITE, ct)
                s.skin_selection(et, s.skin5, pl, RED, ct)
                s.skin_selection(et, s.skin6, pl, ORANGE, ct)
                s.skin_selection(et, s.skin7, pl, PURPLE, ct)
        
        self.input_box.update()
        self.input_box.draw(screen)
        
        pg.display.flip()
        self.clock.tick(100) # frame rate

            
game = Game()
game.menu()
while game.running:

    game.new_game()
    game.game_over()
    
pg.quit()
    
