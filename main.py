# project game main loop

import pygame as pg
import random
import math
from settings import *
from classes import *
from os import path

# game class
class Game(pg.sprite.Sprite):
    # Define the constructor
    def __init__(self):
        # Call the sprite constructor
        pg.sprite.Sprite.__init__(self)
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode(size)
        pg.display.set_caption("Project game")
        self.font = pg.font.match_font(FONT)
        self.clock = pg.time.Clock()
        self.running = True
        self.load_data()
        
    def load_data(self):
        #load all data e.g. graphics, sound, hs, coins
        self.dir = path.dirname(__file__) # create path directory
        with open(path.join(self.dir, HS_file), 'w') as f: # open file if it exists
            try: # runs if possible
                self.highscore = int(f.read())
            except: # if try fails, this runs instead
                self.highscore = 0

                
    def new_game(self):
        # start a new game
        self.score = 0
        self.lives = 5
        self.coin_total = 0
        
        self.all_sprites_group = pg.sprite.Group()
        self.obstacle_group = pg.sprite.Group()
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
        for o in range (3):
            self.obstacle = Obstacle(RED, 20, 200)     
            self.obstacle_group.add(self.obstacle)
            self.all_sprites_group.add(self.obstacle)

        # create rockets
        for r in range (2):
            self.rocket = Rocket(RED, 50, 20)
            self.rocket_group.add(self.rocket)
            self.all_sprites_group.add(self.rocket)

        
        self.run()


    def run(self):
        # run game loop
        self.playing = True
        while self.playing:
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw()
        
    def update(self):
        # game loop update function
        self.all_sprites_group.update()

        ob = self.obstacle
        pl = self.player
        en = self.enemy
        ro = self.rocket
        co = self.coins
        el = self.extra_life
        
        # obstacle collisions
        ob_collision = pygame.sprite.spritecollide(pl, self.obstacle_group, True) # if there's a collision, spawn new obstacle
        for o in ob_collision: # if there's a collision deduct a life
            self.lives -= 1
            ob = Obstacle(RED, 20, 200)
            self.all_sprites_group.add(ob)
            self.obstacle_group.add(ob)
            
        #rocket collisions
        rocket_collision = pygame.sprite.spritecollide(pl, self.rocket_group, True)
        for r in rocket_collision: # if there's a collision deduct 2 lives
            self.lives -= 2
            ro = Rocket(RED, 50, 20)
            self.all_sprites_group.add(ro)
            self.rocket_group.add(ro)
            
        # coin collsions
        coin_collision = pygame.sprite.collide_rect(pl, co) # if there's a collision, spawn new bonus
        if co.rect.x <= 0-co.width or coin_collision == True: # create  new random spawn position for obstacle when they go off screen
            co.rect.x = random.randrange(1000, 2000) 
            co.rect.y = random.randrange(0, size[1] - co.height)
        if coin_collision == True: # if there's a collision add coins to player.coins
            self.coin_total += 5

        # extra lives collisions
        life_collision = pygame.sprite.collide_rect(pl, el) # if there's a collision, spawn new bonus
        if el.rect.x <= 0-el.width or life_collision == True: # create  new random spawn position for obstacle when they go off screen
            el.rect.x = random.randrange(1000, 6000) 
            el.rect.y = random.randrange(0, size[1] - el.height)
        if life_collision == True: # if there's a collision add a life
            self.lives += 1

        
        # enemy movement to track player
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

        #check for collision with enemy and player
        enemy_collision = pygame.sprite.spritecollide(self.player, self.enemy_group, True)
        if enemy_collision: #deduct 3 lives if enemy catches player
            self.lives -= 3

        if self.lives > 0:  # increase player score unless it's run out of lives
            self.score += 0.05

        if self.lives <= 0: #if lives run out, game over
            self.playing = False

        
    def events(self):
        # keyboard events
        pos = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                key = event.key
                if key == pg.K_UP:
                    self.player.speed = -10 # player moves up
                if key == pg.K_DOWN:
                    self.player.speed = 10 # player moves down
                if key == pygame.K_SPACE: # player shoots a bullet
                    self.bullet = bullets(WHITE, self.player.rect.x, self.player.rect.y)
                    self.all_sprites_group.add(self.bullet)
                    self.bullet_group.add(self.bullet)               
            elif event.type == pg.KEYUP:
                self.player.speed = 0
                if event.key == pg.K_p:   # pause function
                    self.press_to_play()
                    
    def draw(self):
        # drawing on screen
        self.screen.fill(BLACK)
        self.all_sprites_group.draw(self.screen)
        self.draw_text(WHITE, 100, 50, 30, "SCORE: %d" % self.score)
        self.draw_text(WHITE, 100, 80, 30, "LIVES: %d" % self.lives)
        self.draw_text(WHITE, 100, 110, 30, "COINS: %d" % self.coin_total)
        # after drawing everything, flip the display
        pg.display.flip()
        
    def menu(self):
        # show start screen
        self.screen.fill(BLUE)
        self.draw_text(WHITE, size[0]/2, 150, 40, "SHOP")
        self.draw_text(GREEN, 150, 40, 40, "HIGSCORE: %d" % self.highscore)
        self.draw_text(WHITE, size[0]/2, 300, 40, "press any key to play")
        self.draw_text(WHITE, size[0]/2, 350, 40, "arrows to move, space to shoot")
        pg.display.flip()
        self.press_to_play() # wait for player to press a key

    def game_over(self):
        if not self.running:
            pg.QUIT()

        if self.score > self.highscore: # new highscore
            self.highscore = self.score
            self.draw_text(WHITE, size[0]/2, 250, 40, "NEW HIGHSCORE!")
            with open(path.join(self.dir, HS_file), 'w') as file: # open text file
                file.write(str(self.score)) # save new highscore in text file
        else:
            self.draw_text(WHITE, size[0]/2, 250, 40, "HIGHSCORE: %d" % self.highscore)
        # game over screen
        self.screen.fill(BLUE)
        self.draw_text(WHITE, size[0]/2, 50, 40, "GAME OVER, PRESS ANY KEY TO PLAY")
        self.draw_text(WHITE, size[0]/2, 150, 40, "SCORE: %d" % self.score)
        pg.display.flip()
        self.press_to_play()

    def press_to_play(self): # wait until player presses a key
        waiting = True
        while waiting:
            self.clock.tick(20)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP: # if any key is pressed game starts
                    waiting = False
            
    def draw_text(self, col, x, y, size, text):
        #Draw text onto the screen
        font = pg.font.Font(self.font, size)
        text_surface = font.render(text, True, col)
        textRect = text_surface.get_rect()
        textRect.midtop = (x, y)
        self.screen.blit(text_surface, textRect)

    
game = Game()
game.menu()
while game.running:
    game.new_game()
    game.game_over()
    
pg.quit()
    
