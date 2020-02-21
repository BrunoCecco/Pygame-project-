# project game main loop

import pygame as pg
import random, math, pickle
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
        pg.mixer.init() # initialise mixer module for sound
        self.screen = pg.display.set_mode(size) # create screen 
        pg.display.set_caption("Project game")
        self.font = pg.font.match_font(FONT) 
        self.clock = pg.time.Clock()
        self.running = True
        self.textfiles()
        
    def textfiles(self):
        with open(HS_file, 'r') as file: # open hs file if it exists
            try: # runs if possible
                self.highscore = int(file.read())
            except: # if try fails, this runs instead
                self.highscore = 0

        with open(Coins_file, 'r') as file: # open coins file
            try:
                self.coin_total = int(file.read())
            except:
                self.coin_total = 0

                
    def new_game(self):
        # start a new game
        self.score = 0
        self.lives = 5 #player starts with 5 lives
        
        #create sprite groups
        self.all_sprites_group = pg.sprite.Group()        
        self.pillar_group = pg.sprite.Group()
        self.bullet_group = pg.sprite.Group()
        self.enemy_group = pg.sprite.Group()
        self.bonus_group = pg.sprite.Group()
        self.rocket_group = pg.sprite.Group()

        #create player
        self.player = Player()
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
            with open(Coins_file, 'w') as file: # open text file
                file.write(str(self.coin_total)) # save new coin total in text fil
                
        # extra lives collisions
        life_collision = pygame.sprite.collide_rect(pl, el) # if there's a collision, spawn new bonus
        if el.rect.x <= 0-el.width or life_collision == True: # create  new random spawn position for obstacle when they go off screen
            el.rect.x = random.randrange(1000, 6000) 
            el.rect.y = random.randrange(0, size[1] - el.height)
        if life_collision == True: # if there's a collision add a life
            self.lives += 1

        
        # TBD - shortest path for enemy movement to track player
        if pl.rect.x >= en.rect.x:
            en.rect.x += en.speed
        if pl.rect.y <= en.rect.y:
            en.rect.y -= en.speed
        elif pl.rect.y >= en.rect.y:
            en.rect.y += en.speed
            
       # check for collision with bullets and enemy
        for b in self.bullet_group:
            bullet_collision = pygame.sprite.spritecollide(self.bullet, self.enemy_group, True)
            for e in bullet_collision: #create new enemy if it dies
                en = Enemy(40, 40, pl)
                self.all_sprites_group.add(en)
                self.enemy_group.add(en)

        # check for collision with enemy and player
        enemy_collision = pygame.sprite.spritecollide(self.player, self.enemy_group, False)
        if enemy_collision: # deduct 3 lives if enemy catches player
            self.lives -= 3
            pg.time.delay(50)  
            enemy.kill() # remove the enemy 

        if self.lives > 0:  # increase player score unless it has run out of lives
            self.score += 1

        if self.lives <= 0: #if lives run out, game over
            self.playing = False
        
    def events(self):
        # keyboard events
        pos = pg.mouse.get_pos() # get position of mouse
        for event in pg.event.get():
            if event.type == pg.QUIT: # if user presses exit button, game ends
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                key = event.key
                if key == pg.K_UP: # player moves up
                    self.player.speed = -10 
                if key == pg.K_DOWN: # player moves down
                    self.player.speed = 10
                if key == pygame.K_SPACE: # player shoots a bullet
                    self.bullet = bullets(WHITE, self.player.rect.x, self.player.rect.y)
                    self.all_sprites_group.add(self.bullet)
                    self.bullet_group.add(self.bullet)               
            elif event.type == pg.KEYUP: # no movement if no keys are being pressed
                self.player.speed = 0
                if event.key == pg.K_p:   # pauses game until a key is pressed
                    self.press_to_play()
                    
    def draw(self):
        # drawing on screen
        self.screen.fill(BLACK) # background        
        self.all_sprites_group.draw(self.screen) # draw sprites onto screen
        self.draw_text(WHITE, 100, 50, 30, "SCORE: %d" % self.score) # display score
        if self.lives >= 0: # display lives if 0 or above
            self.draw_text(WHITE, 100, 80, 30, "LIVES: %d" % self.lives)
        else: # otherwise display 0 lives
            self.draw_text(WHITE, 100, 80, 30, "LIVES: 0")
        self.draw_text(WHITE, 100, 110, 30, "COINS: %d" % self.coin_total) # display coin total
        pg.display.flip() # after drawing everything, flip the display
        
    def menu(self):
        self.shop_g = pg.sprite.Group()
        # show start screen
        self.screen.fill(BLUE) # menu background
        self.draw_button(GREEN, size[0]/2, size[1]/3, 100, 50, "Shop") 
        self.draw_text(GREEN, 150, 50, 40, "Highscore: %d" % self.highscore)
        self.draw_text(GREEN, 150, 100, 40, "Coins: %d" % self.coin_total)
        self.draw_text(GREEN, size[0]/2, size[1]/1.5, 40, "Press any key to play")
        self.draw_text(GREEN, size[0]/2, size[1]/1.2, 40, "Arrows to move, space to shoot")
        self.shop = Shop()
        self.shop_g.add(self.shop)
        #if shop:
         #   self.shop_g.draw(self.screen)
        pg.display.flip()
        self.press_to_play() # wait for player to press a key

    def game_over(self):
        if not self.running:
            pg.QUIT()
        self.screen.fill(BLUE) # game over screen background
        self.draw_text(GREEN, size[0]/2, 50, 40, "Game over, press any key to play")
        self.draw_text(GREEN, size[0]/2, 150, 40, "Score: %d" % self.score)
        if self.score > self.highscore: # new highscore
            self.highscore = self.score 
            self.draw_text(GREEN, size[0]/2, 250, 40, "NEW HIGHSCORE!")
            with open(HS_file, 'w') as file: # open text file
                file.write(str(self.highscore)) # save new highscore in text fil
        else:
            self.draw_text(GREEN, size[0]/2, 250, 40, "Highscore: %d" % self.highscore)
        # game over screen
        pg.display.flip()
        self.press_to_play()

    def press_to_play(self): # wait until player presses a key
        waiting = True
        while waiting:
            self.clock.tick(20) # lower frame rate
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP: # if any key is pressed game starts
                    waiting = False
            
    def draw_text(self, col, x, y, size, text):
        #Draw text onto the screen
        font = pg.font.Font(self.font, size) # set font
        text_surface = font.render(text, True, col)
        textRect = text_surface.get_rect()
        textRect.midtop = (x, y) # set top middle of the text
        self.screen.blit(text_surface, textRect) # display text on screen
                
    def draw_button(col, x, y, w, h, text):
        mouse = pygame.mouse.get_pos()
        if x+w > mouse[0] > x and y+h > mouse[1] > y:
            pygame.draw.rect(self.screen, WHITE(x,y,w,h))
        else:
            pygame.draw.rect(self.screen, BLACK,(x,y,w,h))

        self.draw_text(GREEN, (x+(w/2)), y, 20, text )
    
game = Game()
game.menu()
while game.running:
    game.new_game()
    game.game_over()
    
pg.quit()
    
