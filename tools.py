'''
Tools for help to load and draw some stuff
'''

import pygame as pg

import os
# pg.init()
# IMAGES TOOLS

def load_image(path, img, x=0, y=0, rect=True):
    '''
    Function that returns image and rect.
    path = It's a "os" folder
    img = name of the image that we want to load
    x,y = If we don't change it's equals to 0, it works when we need to choose a different x,y for our rect
    rect = The rect parameter works:
        - If we want the rect of the image, we use as default True
        - If we only need to take the image, we use rect=False, then, only returns the image
    '''

    if rect:
        img = pg.image.load(os.path.join(path, img))
        rect = img.get_rect(x=x, y=y)

        return img, rect

    else:
        img = pg.image.load(os.path.join(path, img))

        return img

def load_and_draw_image(screen, path, img, x=0, y=0):
    '''
    Method that loads and draws the image at same time
    '''
    img = pg.image.load(os.path.join(path, img))
    rect = img.get_rect()

    screen.blit(img, (x, y))

# TEXT TOOLS

def create_draw_text(screen, font, size, text, color, position='', pos_x=0, pos_y=0, width=0, height=0, antialias=True):
    '''
    Function that draws text on the screen
    screen = the surface where we want to draw the text
    font = path where we have the font and the font name
    size = size for the text
    color = color for the text
    ---default params---
    position:
        If we want an specific position for the text we have to
        indicate in 'position' arg as:
            topcenter= takes the center of text size and puts centered in width
                        and top of the screen
            center = puts the text on the center of the screen
            closecenterup = takes the center of text size and puts centered in width
                        and centered in height but more closer to top
            closecenterleft = puts the text shifted a little bit to left
            closecenterbottom = takes the center of text size and puts centered in width
                        and centered in height but more closer to bottom
            closecenterbottom2 = same as closecenterbottom but a little bit lower
            closecenterbottom3 = same as closecenterbottom2 but a little bit lower
            bottomcenter = puts the text centered on width and closer to bottom
                        margin of the screen
        If we choose to add position param, we must to use also width and height
        width and height are the params we use to specify the width and height of our screen
        pos_x and pos_y are the initial pos that we want to draw our text    
    '''
    
    msg_font = pg.font.Font(font, size)
    msg_txt = msg_font.render(text, antialias, color)

    positions = {
        'topcenter':{
            'x':width/2-(msg_txt.get_size()[0]//2),
            'y':75,
        },
        'center':{
            'x':width/2-(msg_txt.get_size()[0]//2),
            'y':height/2-(msg_txt.get_size()[1]//2),
        },
        'closecenterup':{
            'x':width/2-(msg_txt.get_size()[0]//2),
            'y':(height/2)//1.5,
        },
        'closecenterleft':{
            'x':width/2-(msg_txt.get_size()[0]//0.8),
            'y':height/2-(msg_txt.get_size()[1]//2),
        },
        'closecenterbottom':{
            'x':width/2-(msg_txt.get_size()[0]//2),
            'y':height//1.7-(msg_txt.get_size()[1]//2),
        },
        'closecenterbottom2':{
            'x':width/2-(msg_txt.get_size()[0]//2),
            'y':height//1.49-(msg_txt.get_size()[1]//2),
        },
        'closecenterbottom3':{
            'x':width/2-(msg_txt.get_size()[0]//2),
            'y':height//1.32-(msg_txt.get_size()[1]//2),
        },
        'bottomcenter':{
            'x':width/2-(msg_txt.get_size()[0]//2),
            'y':height/1.2-(msg_txt.get_size()[1]//2),
        },
    }

    if position:         
        screen.blit(msg_txt, (positions[position]['x'], positions[position]['y']))
    else:
        screen.blit(msg_txt, (pos_x, pos_y))

# SOUNDS TOOLS
    
def load_sound(path, sound):
    '''
    Function that returns a sound loaded.
    path = It's the path of the sound
    sound = name of the sound that we want to load. Ex: 'sound.wav'
    '''

    sound = pg.mixer.Sound(os.path.join(path, sound))

    return sound

