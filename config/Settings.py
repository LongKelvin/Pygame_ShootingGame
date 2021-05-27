# game windows init


from os import path

WIDTH = 800
HEIGHT = 600
FPS = 60
FPS_SLOWING = 10
POWER_TIME = 5000

# define color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

GAME_TITLE = 'Shooting Game'

FONTNAME = "bahnschrift"

WIN_SCORE = 100000

GAME_SOUND_VOLUME = 0.4

GAME_BACKGROUND_MUSIC = 0.25

GAME_WINNING_TIME = 10000

GAME_DELAY_EVENT = 10000

FONT_SIZE_LARGE = 60
FONT_SIZE_MEDIUM = 40
FONT_SIZE_NORMAL = 32
FONT_SIZE_SMALL = 18

# set up assets folders
abs_folder = path.dirname(path.abspath(__file__))
# root_dir = path.dirname(path.abspath(abs_folder))
img_dir = path.join(path.dirname(abs_folder), 'img')
snd_dir = path.join(path.dirname(abs_folder), 'snd')
game_data_dir = path.join(path.dirname(abs_folder), 'game_data')
player_stat_dir = path.join(path.dirname(abs_folder), 'game_data\player_stat')
print('player state', player_stat_dir)

print(img_dir)

# print("load all game resources")
