'''
Settings of our game
'''
import pygame as pg
import os, random

from folders import *
from tools import *

pg.mixer.init()

# Screen Settings
WIDTH = 800
HEIGHT = 600
FPS = 60
GAME_TITLE = 'The Quest'

# Meteors Settings
MAX_METEORS = 6
METEORS_DATA = {
    'meteor1':{
        'height':38,
        'points':50,
    },
    'meteor2':{
        'height':41,
        'points':50,
    },
    'meteor3':{
        'height':71,
        'points':250,
    },
    'meteor4':{
        'height':66,
        'points':250,
    },
    'meteor5':{
        'height':111,
        'points':500,
    },
    'meteor6':{
        'height':101,
        'points':500,
    },
}
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
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
GOLD = (255, 223, 0)
GOLD2 = (212, 175, 55)
SILVER = (169, 169, 169)
SILVER2 = (128, 128, 128)
BRONCE = (153, 101, 21)

# Fonts
SPACE = os.path.join(FONTS_FOLDER, 'Space_font.ttf')
SPACE2 = os.path.join(FONTS_FOLDER, 'Space_font2.ttf')
TITLE = os.path.join(FONTS_FOLDER, 'title-rayadoitalic2.otf')

# Sounds
OPTION_SOUND = load_sound(SOUNDS_FOLDER, 'option.wav')
OPTION_SOUND.set_volume(0.02)
SELECTED_SOUND = load_sound(SOUNDS_FOLDER, 'option-selected.wav')
SELECTED_SOUND.set_volume(0.02)

# Sounds Settings
BACKGROUND_VOL = 0.1
