import pygame as pg

pg.init()

# define colours

COLOR_INACTIVE = (0, 100, 0)
COLOR_ACTIVE = (0, 200, 0)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
HOVER_COLOR = (50, 50, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
TURQUOISE = (64,224,208)
LIGHTGREY = (100, 100, 100)
DARKGREY = (40, 40, 40)
RED = (245, 50, 17)
ORANGE = (255,165,0)
PURPLE = (148,0,211)
VIOLET = (238,130,238)
PINK = (255,192,203)

# project game settings/options

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
FONT = pg.font.Font(None, 32)

HSFILE = "./Textfiles/highscore.txt"
hsname = "./Textfiles/hs_name.txt"
COINFILE = "./Textfiles/coins.txt"
SPRITESHEET = "shooter_ss.png"
game_speed = 4
oscillating_speed = 1


screen = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT]) # create screen 
pg.display.set_caption("Project game")



