'''
Settings of our game
'''
import pygame as pg
import os, random

from folders import *
from tools import *

# Screen Settings
WIDTH = 800
HEIGHT = 600
FPS = 60
GAME_TITLE = 'The Quest'

# Meteors Settings
MAX_METEORS = 6
METEORS_TO_DODGE = 40

# Ship Settings
SPEED = 8
STATES = {
    'ALIVE':'A',
    'EXPLODING':'E',
    'NOT ALIVE':'N',
    'ROTATING':'R',
    'PREPARED TO LAND':'PTL',
    'LANDING':'L',
    'LANDED':'LD',
    'HIDDEN':'HN',
    'DEAD':'D',
}
LIFES = 3

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GOLD = (255, 223, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
SILVER = (169, 169, 169)
BRONCE = (153, 101, 21)

# Fonts
SPACE2 = os.path.join(FONTS_FOLDER, 'Space_font2.ttf')
TITLE = os.path.join(FONTS_FOLDER, 'title-rayadoitalic2.otf')

pg.mixer.init()
# Sounds
TITLE_BG_SOUND = load_sound(SOUNDS_FOLDER, 'title-screen.wav')
GAME_BG_SOUND = load_sound(SOUNDS_FOLDER, 'background_sound.ogg')
EXPLOSION_SOUND = load_sound(SOUNDS_FOLDER, 'explosion.wav')
NEW_RECORD_SOUND = load_sound(SOUNDS_FOLDER, 'NewRecord.wav')
OPTION_SOUND = load_sound(SOUNDS_FOLDER, 'option.wav')
OPTION_SOUND.set_volume(0.02)
SELECTED_SOUND = load_sound(SOUNDS_FOLDER, 'option-selected.wav')
SELECTED_SOUND.set_volume(0.02)

# Sounds Settings
DEFAULT_VOL = 0.05

# Images
BACKGROUND = load_image(IMAGES_FOLDER, 'background.png')
TOP_LEVEL = load_image(IMAGES_FOLDER, 'score1.png')
JUPITER = load_image(IMAGES_FOLDER, 'JUPITER.png')
MARS = load_image(IMAGES_FOLDER, 'MARS.png')
PAUSE = load_image(IMAGES_FOLDER, 'pause-img.png')
SHIP_TITLE = load_image(SHIP_FOLDER, 'ship1-left.png')
SHIP = load_image(SHIP_FOLDER, 'ship1.png')

## HOW TO PLAY Images
UP_KEY = load_image(HOW_TO_FOLDER, 'up.png')
DOWN_KEY = load_image(HOW_TO_FOLDER, 'down.png')
SPACEBAR_KEY = load_image(HOW_TO_FOLDER, 'spacebar.png')
ESCAPE_KEY = load_image(HOW_TO_FOLDER, 'escape.png')
P_KEY = load_image(HOW_TO_FOLDER, 'P.png')

