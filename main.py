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
        #create text boxes
        self.input_box = InputBox(size[0]/2 - 100, 50, 140, 32)
        
    def play_music(self):
        song_q = ['spongebob.mp3', 'dontworry.mp3', 'babyshark.mp3', 'jinglebells.mp3', 'chainsmokers.mp3']
        pygame.mixer.music.load(random.choice(song_q)) # load random song
        pg.mixer.music.play() # play random song


    def readfiles(self):
        with open(HS_file, 'r') as file: # open hs file if it exists
            try: # runs if possible
                self.highscore = int(file.read())
            except: # if try fails, this runs instead
                self.highscore = 0
        with open(Coins_file, 'r') as file: # open hs file if it exists
            try: # runs if possible
                self.coin_total = int(file.read())
            except: # if try fails, this runs instead
                self.coin_total = 0
        with open(HS_name, 'r') as file: # open hs file if it exists
            try: # runs if possible
                self.hs_name = file.read()
            except: # if try fails, this runs instead
                self.hs_name = 'error'

                
    def writefiles(self, file_name, var):
        with open(file_name, 'w') as file: # open text file
            file.write(str(var)) # save new coin total in text file
        
                
    def new_game(self):
    
        # start a new game
        self.score = 0
        self.lives = 5 #player starts with 5 lives
        
        #create sprite groups
        self.sprite_groups()
        
        #create player        
        self.all_sprites_group.add(self.player)
        #create enemy
        self.enemy = Enemy(40, 40, self.player)
        self.all_sprites_group.add(self.enemy)
        self.enemy_group.add(self.enemy)
        #create bonuses 
        self.extra_life = Lives(GREEN, 30, 30)
        self.bonus_group.add(self.extra_life)
        self.all_sprites_group.add(self.extra_life)

        self.coins = Coins(YELLOW, 20, 20)
        self.bonus_group.add(self.coins)
        self.all_sprites_group.add(self.coins)
        
        #create obstacles
        self.spawn_obstacles(3, Pillars, self.pillar_group, 20, 200)
        
        # create rockets
        self.spawn_obstacles(2, Rockets, self.rocket_group, 50, 20)

        self.run()

    def spawn_obstacles(self, num, class_name, group, w, h):
        for o in range(num):
            self.ob = class_name(w, h) #colour, width and height
            group.add(self.ob)
            self.all_sprites_group.add(self.ob)


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
        self.all_sprites_group.update() # update all sprites groups

        #abbreviations
        pl = self.player 
        en = self.enemy
        co = self.coins
        el = self.extra_life
        
        # obstacle collisions
        p_collision = pygame.sprite.spritecollide(pl, self.pillar_group, True) # if there's a collision, spawn new obstacle
        for p in p_collision: # if there's a collision deduct a life
            self.lives -= 1
            self.spawn_obstacles(1, Pillars, self.pillar_group, 20, 200)# respawn obstacles

        r_collision = pygame.sprite.spritecollide(pl, self.rocket_group, True) # if there's a collision, spawn new obstacle
        for r in r_collision: # if there's a collision deduct a life
            self.lives -= 2
            self.spawn_obstacles(1, Rockets, self.rocket_group, 50, 20)# respawn obstacles

        # coin collsions
        coin_collision = pygame.sprite.collide_rect(pl, co) # if there's a collision, spawn new bonus
        if co.rect.x <= 0-co.width or coin_collision == True: # create  new random spawn position for obstacle when they go off screen
            co.rect.x = random.randrange(1000, 2000) 
            co.rect.y = random.randrange(0, size[1] - co.height)
        if coin_collision == True: # if there's a collision add coins to player.coins
            self.coin_total += 1
            self.writefiles(Coins_file, self.coin_total)
        #TBD - method to write in files

                
        # extra lives collisions
        life_collision = pygame.sprite.collide_rect(pl, el) # if there's a collision, spawn new bonus
        if el.rect.x <= 0-el.width or life_collision == True: # create  new random spawn position for obstacle when they go off screen
            el.rect.x = random.randrange(1000, 6000) 
            el.rect.y = random.randrange(0, size[1] - el.height)
        if life_collision == True: # if there's a collision add a life
            self.lives += 1

        
        # TBD - shortest path for enemy movement to track player
        if pl.rect.x > en.rect.x:
            en.rect.x += en.speed
        if pl.rect.y < en.rect.y:
            en.rect.y -= en.speed
        elif pl.rect.y > en.rect.y:
            en.rect.y += en.speed
            
       # check for collision with bullets and enemy
        for b in self.bullet_group:
            bullet_collision = pygame.sprite.spritecollide(self.bullet, self.enemy_group, True)
            if bullet_collision: #create new enemy if it dies
                b.kill()
                en = Enemy(40, 40, pl)
                self.enemy_group.add(en)
                self.all_sprites_group.add(en)
                

        # check for collision with enemy and player
        enemy_collision = pygame.sprite.spritecollide(self.player, self.enemy_group, True)
        if enemy_collision: # deduct 3 lives if enemy catches player
            self.lives -= 3
            pg.time.delay(50)
            en = Enemy(40, 40, pl)
            self.enemy_group.add(en)
            self.all_sprites_group.add(en)

        if self.lives > 0:  # increase player score unless it has run out of lives
            self.score += 1

        if self.lives <= 0: #if lives run out, game over
            self.playing = False
        
    def events(self):
        # keyboard events
        for event in pg.event.get():
            if event.type == pg.QUIT: # if user presses exit button, game ends
                self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                k = event.key 
                if k == pg.K_UP: # player moves up
                    self.player.speed = -10 
                if k == pg.K_DOWN: # player moves down
                    self.player.speed = 10
                if k == pygame.K_SPACE: # player shoots a bullet
                    self.bullet = bullets(WHITE, self.player.rect.x, self.player.rect.y)
                    self.all_sprites_group.add(self.bullet)
                    self.bullet_group.add(self.bullet)               
            elif event.type == pg.KEYUP: # no movement if no keys are being pressed
                self.player.speed = 0
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
        self.pillar_group = pg.sprite.Group()
        self.bullet_group = pg.sprite.Group()
        self.enemy_group = pg.sprite.Group()
        self.bonus_group = pg.sprite.Group()
        self.rocket_group = pg.sprite.Group()
        self.butt_group = pg.sprite.Group()
        self.shop_group = pg.sprite.Group()
        
    def menu(self):
        self.entered = False # hasn't entered shop yet
        self.waiting = True
        self.shop_butt = Button(GREEN, size[0]/2-50, size[1]/2, 100, 35, "Shop")
        self.butt_group.add(self.shop_butt)
        self.player = Player() # create player
        self.all_sprites_group.add(self.player)
        self.shop = Shop() # instantiate shop
        s = self.shop # abbreviate
        # add shop skins to shop group
        self.shop_group.add(s,s.skin1,s.skin2,s.skin3,s.skin4) 
        # show start screen
        screen.fill(BLUE) # menu background
        draw_text(GREEN, size[0]/2, 20, 40, "Enter Name: ")
        draw_text(GREEN, 150, 50, 40, "Highscore: %d" % self.highscore)
        draw_text(GREEN, 150, 100, 40, "Coins: %d" % self.coin_total)
        draw_text(GREEN, size[0]/2, size[1]/1.5, 40, "Press p to play")
        draw_text(GREEN, size[0]/2, size[1]/1.2, 40, "Arrows to move, space to shoot")
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
        draw_text(GREEN, size[0]/2, 50, 40, "Game over, press any key to play")
        draw_text(GREEN, size[0]/2, 200, 40, "Score: %d" % self.score)
        
        if self.score > self.highscore: # new highscore
            self.highscore = self.score
            draw_text(GREEN, size[0]/2, 300, 40, "NEW HIGHSCORE! " + self.hs_name)
            self.writefiles(HS_file, self.highscore)
        else:
            draw_text(GREEN, size[0]/2, 250, 40, ("Highscore: %d - " % self.highscore) + self.hs_name)
        # game over screen
        pg.display.flip()
        while self.waiting:
            self.shop_butt = Button(GREEN, size[0]/2-50, size[1]/3, 100, 35, "Shop")
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
                   
                # check for skins button presses
                if et == pg.MOUSEBUTTONDOWN and s.skin1.mouse_pos:
                    self.player.update_col(GREEN) # purchase green skin
                    ct -= 1 # take coins off 
                if et == pg.MOUSEBUTTONDOWN and s.skin2.mouse_pos: 
                    self.player.update_col(YELLOW) # purchase skin
                    ct -= 1 # take coins off
                if et == pg.MOUSEBUTTONDOWN and s.skin3.mouse_pos: 
                    self.player.update_col(HOVER_COLOR) # purchase skin
                    ct -= 1 # take coins off
                if et == pg.MOUSEBUTTONDOWN and s.skin4.mouse_pos: 
                    self.player.update_col(WHITE) # purchase skin
                    ct -= 1 # take coins off                    
        
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
    
