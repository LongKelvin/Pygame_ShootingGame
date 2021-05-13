# game windows init


from os import path

WIDTH = 800
HEIGHT = 600
FPS = 60
POWER_TIME = 5000

# define color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

GAME_TITLE = 'Shooting Game'
# font for game
# font_name = pygame.font.SysFont(None, 20)
# FONTNAME = "arial"
FONTNAME = "bahnschrift"

WIN_SCORE = 1000

GAME_SOUND_VOLUME = 0.4

GAME_BACKGROUND_MUSIC = 0.25

# set up assets folders
img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')
game_data_dir = path.join(path.dirname(__file__), 'game_data')

# print("load all game resources")
