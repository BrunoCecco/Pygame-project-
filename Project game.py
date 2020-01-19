import pygame
import math
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 50, 255)
YELLOW = (255, 255, 0)
RED = (245, 50, 17)
pygame.init()
size = (1000, 400)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Project game")
done = False
font = pygame.font.Font(None, 30)
            
def print_text(x_pos, y_pos, my_screen, text_string):
    #Draw text onto the screen
    text_map = font.render(str(text_string), True, WHITE)
    my_screen.blit(text_map, [x_pos, y_pos])
    #y_pos += line_height
 
class Player(pygame.sprite.Sprite):
    # Define the constructor for invaders
    def __init__(self, color, width, height):
        
        # Call the sprite constructor
        super().__init__()
        # Create a sprite and fill it with colour
        self.image = pygame.Surface([width,height])
        self.image.fill(color)
        # Set the position of the sprite
        self.rect = self.image.get_rect()
        self.rect.x = size[0]/2
        self.rect.y = size[1] - 100
        self.rect.topleft = self.rect.x, self.rect.y
        self.width = width
        self.height = height
        self.speed = 0
        self.score = 0 # ordinary attribute
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
 

## -- Define the class invaders which is a sprite
class Road(pygame.sprite.Sprite):
    # Define the constructor for invaders
    def __init__(self, color, width, height, x, y):
        # Call the sprite constructor
        super().__init__()
        # Create a sprite and fill it with colour
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # Set the position of the sprite
        self.width = width
        self.height = height
        
    def update(self):
        self.rect.x = self.rect.x - 3 #roads move to the left
        if self.rect.x <= 0:
            self.rect.x = size[0]

all_sprites_group = pygame.sprite.Group()
road_group = pygame.sprite.Group()

# create player 
player = Player(RED, 30, 30)
all_sprites_group.add(player)

#create roads
x = 1000
y = 100
for r in range (5):
    road = Road(YELLOW, 30, 200, x, y)      
    road_group.add(road)
    all_sprites_group.add(road)
    x += random.randrange(100, 500) #roads created at random intervals
    y = random.randrange(-200, 200) #roads appear at random heights


clock = pygame.time.Clock()

while not done and player.lives > 0:
#-user input and controls
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            key = event.key
            if key == pygame.K_UP:
                player.player_move(-10)
            if key == pygame.K_DOWN:
                player.player_move(10)
        elif event.type == pygame.KEYUP:
            player.player_move(0)
            
    player.increase_score(0.1)
    
    # -- Game logic goes in here
    all_sprites_group.update()
    # -- Screen background is BLACK
    screen.fill(BLACK)
    # -- Drawing code goes here
    all_sprites_group.draw(screen)
    
    print_text(20, 20, screen, "Lives: %d" % player.lives)
    print_text(20, 50, screen, "Score: %d" % player.score)
    # -- flip display to reveal new position of objects
    pygame.display.flip()
    # - The clock ticks over
    clock.tick(60)


#End While - End of game loop
pygame.quit()
