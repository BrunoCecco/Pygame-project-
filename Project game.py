import pygame
import math
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
HOVER_COLOR = (50, 50, 255)
YELLOW = (255, 255, 0)
RED = (245, 50, 17)
#initialize pygame
pygame.init()
#set screen size
size = (1000, 400)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Project game")
font = pygame.font.Font(None, 50)
clock = pygame.time.Clock()
done = True
menu = True

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

def pause():
    paused = True

    while paused: # while paused is true
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                key = event.key
                if key == pygame.K_c: # if c pressed, game continues
                    paused = False
                if key == pygame.K_q:
                    pygame.quit()
                    
        screen.fill(WHITE)
        print_text(RED, size[0]/4, size[1]/2.5, screen, "Press c to continue or q to quit")
        pygame.display.update()
        clock.tick(5)
        
    
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

def print_text(col, x_pos, y_pos, my_screen, text_string):
    #Draw text onto the screen
    global textRect
    text_map = font.render(str(text_string), True, col)
    textRect = text_map.get_rect()
    textRect.centerx = text_map.get_rect().centerx
    textRect.centery = text_map.get_rect().centery
    textRect.x = x_pos
    textRect.y = y_pos
    screen.blit(text_map, textRect)

class Enemy(pygame.sprite.Sprite):
    # Define the constructor
    def __init__(self, color, width, height, filename, player):
        # Call the sprite constructor
        super().__init__()
        # Set the position of the sprite
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect()
        self.rect.x = -random.randrange(0, 1000)
        self.rect.y = size[1]/2.3
        self.rect.topleft = self.rect.x, self.rect.y
        self.width = width
        self.height = height
        self.speed = 1
    
    def update(self): #if player is above or below enemy, enemy moves accordingly to catch player
        if player.rect.x >= self.rect.x:
            self.rect.x += self.speed
        if player.rect.y <= self.rect.y:
            self.rect.y -= self.speed
        elif player.rect.y >= self.rect.y:
            self.rect.y += self.speed
    
            
class Player(pygame.sprite.Sprite):
    # Define the constructor
    def __init__(self, color, width, height, filename):
        # Call the sprite constructor
        super().__init__()
        # Set the position of the sprite
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect()
        self.rect.x = size[0]/2
        self.rect.y = size[1] - 100
        self.rect.topleft = self.rect.x, self.rect.y
        self.width = width
        self.height = height
        self.speed = 0
        self.score = 0
        self.lives = 5

    def increase_score(self, val):
        self.score += val
        
    def player_move(self, val):
        self.speed = val

    def update(self):
        self.rect.y += self.speed
        if self.rect.y <= size[1]-self.height:
            self.rect.y += 2 #gravitational effect
        if self.rect.y >= size[1]: #floor
            self.rect.y = size[1] - self.height
        if self.rect.y <= 0: #ceiling
            self.rect.y = 0
 
class bullets(pygame.sprite.Sprite):
    # Define the constructor 
    def __init__(self, color, width, height, x, y):
        # Call the sprite constructor
        super().__init__()
        # Create a sprite and fill it with colour
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x
        self.rect.y = player.rect.y
        # Set the position of the sprite
        self.width = width
        self.height = height
        self.speed = 4
        self.spawnpos = size[0]

    def update(self):
        self.rect.x = self.rect.x - self.speed #bullets move right

#diagonal objects
class Obstacle1(pygame.sprite.Sprite):
    # Define the constructor
    def __init__(self, color, width, pos1, pos2):
        # Call the sprite constructor
        super().__init__()
        # Create a sprite and fill it with colour
        self.image = pygame.draw.line(screen, color, pos1, pos2, width)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = pos1[0]
        self.rect.y = pos2[1]
        # Set the position of the sprite
        self.width = width
        self.speed = 4

    def update(self):
        self.rect.x = self.rect.x - self.speed #bullets move right
    
## -- Define the class invaders which is a sprite
class Obstacle(pygame.sprite.Sprite):
    # Define the constructor
    def __init__(self, color, width, height, x, y, filename):
        # Call the sprite constructor
        super().__init__()
        # Create a sprite and fill it with colour
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # Set the position of the sprite
        self.width = width
        self.height = height
        self.speed = 4
        self.spawnpos = size[0]

        
    def change_spawnpos(self, val): # change spawn position of rockets as they're less frequent
        self.spawnpos += val
        
    def change_speed(self, val): # change speed of rockets as they're faster
        self.speed = val

    def update(self): # create illusion that player is moving right
        self.rect.x = self.rect.x - self.speed #obstacles move to the left
        if self.rect.x <= 0-self.width:
            self.rect.x = self.spawnpos
            self.rect.y = random.randrange(0, 200)
            

all_sprites_group = pygame.sprite.Group()
obstacle_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

# create player 
player = Player(RED, 40, 40, 'pacman.jpg')
all_sprites_group.add(player)

#create enemy
enemy = Enemy(RED, 40, 40, 'pacman.jpg', player)
all_sprites_group.add(enemy)
enemy_group.add(enemy)

#create obstacles
x = 1000
y = 100
for o in range (3):
    obstacle = Obstacle(YELLOW, 100, 200, x, y, 'obstacle.jpg')     
    obstacle_group.add(obstacle)
    all_sprites_group.add(obstacle)
    x += random.randrange(100, 700) #obstacles created at random intervals
    y = random.randrange(0, 200) #obstacles appear at random heights

# create rockets
for r in range (2):
    rocket = Obstacle(RED, 100, 40, random.randrange(2500, 4000), random.randrange(0, 370), 'project_obstacle.png')
    rocket.change_speed(8)
    rocket.change_spawnpos(2000)
    obstacle_group.add(rocket)
    all_sprites_group.add(rocket)

main_menu = game_intro()
            
while main_menu == True:
    screen.fill(BLACK)
    # -- flip display to reveal new position of objects
    pygame.display.flip()
    # - The clock ticks over
    clock.tick(60)


while main_menu == False and done == True:
#-user input and controls
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = False
        elif event.type == pygame.KEYDOWN:
            key = event.key
            if key == pygame.K_UP:
                player.player_move(-10)
            if key == pygame.K_DOWN:
                player.player_move(10)
            if key == pygame.K_SPACE:
                bullet = bullets(WHITE, 20, 20, (player.rect.x+player.width), player.rect.y)
                all_sprites_group.add(bullet)
                bullet_group.add(bullet)
            if key == pygame.K_p:   # pause function
                pause()                
        elif event.type == pygame.KEYUP:
            player.player_move(0)
    if player.lives > 0:  
        player.increase_score(0.1)
                                    
    #check for collisions
    obstacle_collision = pygame.sprite.spritecollide(player, obstacle_group, True)
    for b in bullet_group:
        bullet_collision = pygame.sprite.spritecollide(bullet, enemy_group, True)
        for e in bullet_collision: #create new enemy if it dies
            enemy = Enemy(RED, 40, 40, 'pacman.jpg', player)
            all_sprites_group.add(enemy)
            enemy_group.add(enemy)
            
    #if player collides with obstacle, lives decrease
    for o in obstacle_collision:
        player.lives -= 1
        random_pos = random.randrange(1000, 1800) # create a new random pos for each obstacle
        #create new obstacle if there's a collision        
        obstacle = Obstacle(YELLOW, 100, 200, random.randrange(1000, 1800), random.randrange(0, 200), 'obstacle.jpg') 
        obstacle_group.add(obstacle)
        all_sprites_group.add(obstacle)
        print_text(RED, 300, 50, screen, "HIT!")
        pygame.display.update()
        pygame.time.delay(50)

    if player.lives == 0: #if lives 0, stop game and display final score
        screen.fill(WHITE)
        print_text(RED, size[0]/4, size[1]/2.5, screen, "Final Score: %d" % player.score)
        pygame.display.update()
        pygame.time.delay(1000)
        
    # -- Game logic goes in here
    all_sprites_group.update()
    # -- Screen background is BLACK
    screen.fill(BLACK)
    # -- Drawing code goes here
    all_sprites_group.draw(screen)
    
    print_text(RED, 20, 20, screen, "Lives: %d" % player.lives) # display lives 
    print_text(RED, 20, 50, screen, "Score: %d" % player.score) # display score
    # -- flip display to reveal new position of objects
    pygame.display.flip()
    # - The clock ticks over
    clock.tick(60)

#End While - End of game loop
pygame.quit()
