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
LIGHTGREY = (100, 100, 100)
DARKGREY = (40, 40, 40)
RED = (245, 50, 17)
ORANGE = (255,165,0)
PURPLE = (148,0,211)

# project game settings/options

SCREEN_WIDTH = 1020
SCREEN_HEIGHT = 420
FONT = pg.font.Font(None, 32)

hsfile = "Textfiles\highscore.txt"
hsname = "Textfiles\hs_name.txt"
coinfile = "Textfiles\coins.txt"
game_speed = 4
oscillating_speed = 1


screen = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT]) # create screen 
pg.display.set_caption("Project game")



