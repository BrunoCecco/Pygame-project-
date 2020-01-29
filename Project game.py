import pygame
import math
import random
import turtle

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
font = pygame.font.Font(None, 50)
            
def print_text(x_pos, y_pos, my_screen, text_string):
    #Draw text onto the screen
    text_map = font.render(str(text_string), True, RED)
    my_screen.blit(text_map, [x_pos, y_pos])
 
class Player(pygame.sprite.Sprite):
    # Define the constructor for invaders
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
        self.score = 0 #ordinary attribute
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
    # Define the constructor for invaders
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
        self.rect.x = self.rect.x + self.speed #bullets move right

#diagonal objects
class Obstacle1(pygame.sprite.Sprite):
    # Define the constructor for invaders
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
    # Define the constructor for invaders
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

        
    def change_spawnpos(self, val):
        self.spawnpos += val
        
    def change_speed(self, val):
        self.speed = val

    def update(self):
        self.rect.x = self.rect.x - self.speed #obstacles move to the left
        if self.rect.x <= 0-self.width:
            self.rect.x = self.spawnpos
            self.rect.y = random.randrange(0, 200)

all_sprites_group = pygame.sprite.Group()
obstacle_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()

# create player 
player = Player(RED, 30, 30, 'invader_img.png')
all_sprites_group.add(player)

#create obstacles
x = 1000
y = 100
for o in range (3):
    obstacle = Obstacle(YELLOW, 100, 200, x, y, 'project_obstacle.png')     
    obstacle_group.add(obstacle)
    all_sprites_group.add(obstacle)
    x += random.randrange(100, 700) #obstacles created at random intervals
    y = random.randrange(0, 200) #obstacles appear at random heights

for r in range (2):
    rocket = Obstacle(RED, 50, 15, random.randrange(2500, 4000), random.randrange(0, 370), 'rocket.png')
    rocket.change_speed(10)
    rocket.change_spawnpos(2000)
    obstacle_group.add(rocket)
    all_sprites_group.add(rocket)

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
            if key == pygame.K_SPACE:
                bullet = bullets(WHITE, 20, 20, (player.rect.x+player.width), player.rect.y)
                all_sprites_group.add(bullet)
                bullet_group.add(bullet)
        elif event.type == pygame.KEYUP:
            player.player_move(0)
            
    player.increase_score(0.1)
                                
    #check for collisions
    obstacle_collision = pygame.sprite.spritecollide(player, obstacle_group, True)
    b_count = 0
    for b in bullet_group:
        bullet_collision = pygame.sprite.spritecollide(bullet, obstacle_group, True)
        
        
    #if player collides with obstacle, lives decrease
    for o in obstacle_collision:
        player.lives -= 1
        obstacle = Obstacle(YELLOW, 100, 200, random.randrange(1000, 1800), random.randrange(0, 200), 'project_obstacle.png')      
        obstacle_group.add(obstacle)
        all_sprites_group.add(obstacle)
        print_text(300, 50, screen, "HIT!")
        pygame.display.update()
        pygame.time.delay(50)
    
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
