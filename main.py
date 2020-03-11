# project game main loop

import pygame as pg
import random, math
from settings import *
from classes import *
from os import path

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
        self.readfiles()
        self.sprite_groups() # create sprite groups
        self.block_size = 20 # block width (size)

        #create text boxes
        self.input_box = InputBox(SCREEN_WIDTH/2 - 100, 50, 140, 30)
        self.endtime = 0
        
    def play_music(self):
        song_q = ['spongebob.mp3', 'dontworry.mp3', 'jinglebells.mp3', 'chainsmokers.mp3']
        pygame.mixer.music.load(random.choice(song_q)) # load random song
        #pg.mixer.music.play() # play random song from list


    # TBD - function to read files
    def readfiles(self):
        with open(HS_file, 'r') as file: # open file if it exists
            try: # runs if possible
                self.highscore = int(file.read())
            except: # if try fails, this runs instead
                self.highscore = 0
        with open(Coins_file, 'r') as file: # open file if it exists
            try: # runs if possible
                self.coin_total = int(file.read())
            except: # if try fails, this runs instead
                self.coin_total = 0
        with open(HS_name, 'r') as file: # open file if it exists
            try: # runs if possible
                self.hs_name = file.read()
            except: # if try fails, this runs instead
                self.hs_name = 'error'

                
    def writefiles(self, file_name, var):
        with open(file_name, 'w') as file: # open text file
            file.write(str(var)) # save new coin total in text file

    # Screen width in blocks
    def screen_width(self):
        return int(SCREEN_WIDTH / self.block_size)

    # Screen height in blocks
    def screen_height(self):
        return int(SCREEN_HEIGHT / self.block_size)
        
    def random_reset(self):
        self.block_rand = [random.sample(range(0, self.screen_width()), 2), random.sample(range(0, self.screen_height()), 2)]
        self.coin_rand = random.sample(range(0, self.screen_height()), 1)
        self.live_rand = random.sample(range(0, self.screen_height()), 1)

    def create_map(self):
        # create 2D array (map) with all sprites 
        self.game_map = [] # initialize 2D array  
        self.new_row = [] # initialize rows
        self.random_reset()

        # random spawn positions
        for i in range (0, self.screen_height()):
            for j in range (0, self.screen_width()):
                if j == 0 and i == 0:
                    self.new_row.append(4) # 4 indicates enemy
                elif j in self.coin_rand and i in self.coin_rand:
                    self.new_row.append(3) # 3 indicates coin
                elif j in self.live_rand and i in self.live_rand:
                    self.new_row.append(2) # 2 indicates life
                elif j in self.block_rand[0] and i in self.block_rand[1]:
                    self.new_row.append(1) # 1 indicates obstacle
                else:
                    self.new_row.append(0) # 0 indicates background
            self.game_map.append(self.new_row) # put new row into map list
            self.new_row = [] # create new empty row
    
        # display map - if depending on number in array, instantiate a sprite
        for y in range(0, self.screen_height()): # y-axis of the map  
            for x in range(0, self.screen_width()): # x-axis of the map
                if self.game_map[y][x] == 0: # if contents is 0, draw background
                    self.background = Background(x, y, self.block_size)
                    self.background_group.add(self.background)
                if self.game_map[y][x] == 1: # if contents is 1, draw block
                    self.block = Block(GREEN, x, y, self.block_size)
                    self.map_group.add(self.block)
                if self.game_map[y][x] == 2: 
                    self.extra_life = Lives(GREEN, x, y, self.block_size)
                    self.life_group.add(self.extra_life)
                if self.game_map[y][x] == 3:
                    self.coins = Coins(YELLOW, x, y, self.block_size)
                    self.coin_group.add(self.coins)
                if self.game_map[y][x] == 4:
                    self.enemy = Enemy(x, y, self.block_size)
                    self.enemy_group.add(self.enemy)

                    
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
        self.background_group.update()
        self.all_sprites_group.update() # update all sprites
        
        for s in self.all_sprites_group:
            if s.rect.x <= -50: # respawn sprite if they go off screen
                s.kill()
            # respawn obstacles and bonuses
            if len(self.life_group) + len(self.coin_group) + len(self.map_group) == 0:
                self.create_map()

        # enemy movement to track players
        self.enemy.move(self.player.body[0])
        
        #abbreviations
        pl = self.player.sprite 
        en = self.enemy
        
        # collsions
        for b in pygame.sprite.groupcollide(self.player_group, self.map_group, False, True):
            # if there's a collision decrease lives
            self.lives -= 1
        for l in pygame.sprite.groupcollide(self.player_group, self.life_group, False, True):
        # if there's a collision add life to player
            self.lives += 1   
        for c in pygame.sprite.groupcollide(self.player_group, self.coin_group, False, True):
            # if there's a collision add coins to player
            self.coin_total += 1
            self.writefiles(Coins_file, self.coin_total)
            
       # check for collision with bullets and enemy
        for b in pygame.sprite.groupcollide(self.bullet_group, self.enemy_group, True, True):
            self.coins = self.coins

        # check for collision with enemy and player
        for b in pygame.sprite.groupcollide(self.player_group, self.enemy_group, False, True):
            self.lives -= 3
        
        # TBD - shortest path for enemy movement to track player
        if self.lives > 0:  # increase player score unless it has run out of lives
            self.score += 1

        if self.lives <= 0: #if lives run out, game over
            self.playing = False

        curr_time = pg.time.get_ticks() # get current time
        if curr_time - self.endtime > 100: # re-align player every x milliseconds
            self.player.straighten()
            self.endtime = curr_time      
        
    def events(self):
        # keyboard events
        keys = pg.key.get_pressed()
        if keys[pg.K_UP] or keys[pg.K_DOWN]: # player moves up or down
            curr_time = pg.time.get_ticks() # get current time
            if curr_time - self.endtime > 30: # re-align player every x milliseconds
                self.endtime = curr_time
                self.player.move(False if keys[pg.K_DOWN] else True)  
        for event in pg.event.get():
            if event.type == pg.QUIT: # if user presses exit button, game ends
                self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                k = event.key      
                if k == pygame.K_SPACE: # player shoots a bullet
                    self.bullet = bullets(WHITE, self.player.body[0].rect.x, self.player.body[0].rect.y)
                    self.all_sprites_group.add(self.bullet)
                    self.bullet_group.add(self.bullet)               
                if event.key == pg.K_p:   # pauses game until a key is pressed
                    self.navigation()           

                    
    def draw(self):
        # drawing on screen
        screen.fill(BLACK) # background
        self.background_group.draw(screen)
        self.all_sprites_group.draw(screen) # draw sprites onto screen
        draw_text(WHITE, 100, 50, 30, "SCORE: %d" % self.score) # display score
        draw_text(WHITE, 100, 80, 30, "LIVES: %d" % self.lives) if self.lives >= 0 else draw_text(WHITE, 100, 80, 30, "LIVES: 0")
        draw_text(WHITE, 100, 110, 30, "COINS: %d" % self.coin_total) # display coin total
        pg.display.flip() # after drawing everything, flip the display
        
    def sprite_groups(self):
        self.all_sprites_group = pg.sprite.Group()  
        self.map_group = pg.sprite.Group()
        self.background_group = pg.sprite.Group()
        self.bullet_group = pg.sprite.Group()
        self.player_group = pg.sprite.Group()
        self.enemy_group = pg.sprite.Group()
        self.life_group = pg.sprite.Group()
        self.coin_group = pg.sprite.Group()
        self.butt_group = pg.sprite.Group()
        self.shop_group = pg.sprite.Group()
        
    def menu(self):
    
        self.sprite_groups() # create sprite groups
        self.player = Player(SCREEN_WIDTH/2, 200, self.block_size) # create a player head
        self.player_group.add(self.player.sprite) # add to player group
        self.all_sprites_group.add(self.player_group) # add player to all sprites group

        self.entered = False # hasn't entered shop yet
        self.waiting = True
        self.shop_butt = Button(GREEN, SCREEN_WIDTH/2-50, SCREEN_HEIGHT/2, 100, 35, "Shop")
        self.butt_group.add(self.shop_butt)
        self.shop = Shop() # instantiate shop
        s = self.shop # abbreviate
        # add shop skins to shop group
        self.shop_group.add(s,s.skin1,s.skin2,s.skin3,s.skin4) 
        # show start screen
        screen.fill(BLUE) # menu background
        draw_text(GREEN, SCREEN_WIDTH/2, 20, 40, "Enter Name: ")
        draw_text(GREEN, 150, 50, 40, "Highscore: %d" % self.highscore)
        draw_text(GREEN, 150, 100, 40, "Coins: %d" % self.coin_total)
        draw_text(GREEN, SCREEN_WIDTH/2, SCREEN_HEIGHT/1.5, 40, "Press p to play")
        draw_text(GREEN, SCREEN_WIDTH/2, SCREEN_HEIGHT/1.2, 40, "Arrows to move, space to shoot")
        pg.display.flip()
        while self.waiting: # while menu is true repeat steps
            self.navigation() # wait for player to press a key            
            # create buttons
            self.butt_group.draw(screen)
            self.butt_group.update()

                
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
            self.writefiles(HS_file, self.highscore)
        else:
            draw_text(GREEN, SCREEN_WIDTH/2, 250, 40, ("Highscore: %d - " % self.highscore) + self.hs_name)
        # game over screen
        pg.display.flip()
        while self.waiting:
            self.shop_butt = Button(GREEN, SCREEN_WIDTH/2-50, SCREEN_HEIGHT/3, 100, 35, "Shop")
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
            if et == pg.MOUSEBUTTONUP and self.shop_butt.mouse_pos == True:
                self.entered = True
                self.butt_group.remove(self.shop_butt) # remove shop button from screen
                
            if self.entered: # create shop if shop button pressed
                self.shop_group.draw(screen)
                self.shop_group.update()
                self.all_sprites_group.draw(screen)
                self.all_sprites_group.update()

                pl = self.player # abbreviate
                # check for skins button presses
                if et == pg.MOUSEBUTTONDOWN and s.skin1.mouse_pos:
                    pl.update_col(GREEN) # purchase green skin
                    ct -= 1 # take coins off
                    self.writefiles(Coins_file, ct)
                if et == pg.MOUSEBUTTONDOWN and s.skin2.mouse_pos: 
                    pl.update_col(YELLOW) # purchase skin
                    ct -= 1 # take coins off
                    self.writefiles(Coins_file, ct)
                if et == pg.MOUSEBUTTONDOWN and s.skin3.mouse_pos: 
                    pl.update_col(HOVER_COLOR) # purchase skin
                    ct -= 1 # take coins off
                    self.writefiles(Coins_file, ct)
                if et == pg.MOUSEBUTTONDOWN and s.skin4.mouse_pos: 
                    pl.update_col(WHITE) # purchase skin
                    ct -= 1 # take coins off
                    self.writefiles(Coins_file, ct)
        
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
    
