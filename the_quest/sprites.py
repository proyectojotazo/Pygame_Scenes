import pygame as pg
from pygame.locals import *

import random

import os

from folders import *
from tools import *
from config import *

class Ship(pg.sprite.Sprite):

    EXPLOSION = [load_image(EXPLOSION_FOLDER, f'explosion_{x}.png') for x in range(8)]

    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        self.image = SHIP 
        self.rect = self.image.get_rect(x=0, y=276)

        self.selected_expl_img = 0
        self.speed_explosion = 0
        self.explosion_sound = EXPLOSION_SOUND

        self.lifes = LIFES

        self.state = STATES['ALIVE']

        self.angle = 0

        self.vy = 0

    def update(self):
        '''
        Update method ship
        '''
        self.rect.y += self.vy
        
        if self.state == STATES['EXPLODING']:
            self.image = self._explosion()

        if self.state == STATES['ROTATING']:
            self._rotate()

        if self.state == STATES['LANDING']:
            self._landing()

        if self.state == STATES['LANDED']:
            self._hiding()

        if self.lifes == 0:
            self.state = STATES['DEAD']

        if self.rect.top <= 50:
            self.rect.top = 50

        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT

        self._moving_ship()

    def _moving_ship(self):
        '''
        Moving method ship
        '''
        if self.state == STATES['ALIVE'] or self.state == STATES['PREPARED TO LAND']:
            key_pressed = pg.key.get_pressed()

            if key_pressed[K_UP]:
                self.vy = -SPEED
            elif key_pressed[K_DOWN]:
                self.vy = SPEED
            else:
                self.vy = 0
        else:
            self.vy = 0

    def _explosion(self):
        '''
        Explosion animation method.
        It returns the image of the explosion. When we reach the last image, we return the original
        image of the ship, restart the selected_expl_img to 0, we remove 1 life from our
        ship, and change the state to 'NOT ALIVE'
        '''

        if self.selected_expl_img >= 8:
            img = SHIP
            self.selected_expl_img = 0
            self.lifes -= 1
            self.state = STATES['NOT ALIVE']

        else:
            img = self.EXPLOSION[self.selected_expl_img]
            if self.speed_explosion % 4 == 0:
                self.selected_expl_img += 1

        self.speed_explosion += 1
        
        return img

    def _rotate(self):
        '''
        Method who makes the ship rotation
        '''
        if self.angle <= 180:
            rotated_img = pg.transform.rotozoom(SHIP, self.angle, 1)
            rect_rotated_img = rotated_img.get_rect(center=(self.rect.centerx, self.rect.centery))
            self.image = rotated_img
            self.rect = rect_rotated_img
            self.angle += 1
        else:
            self.state = STATES['PREPARED TO LAND']

    def _landing(self):
        '''
        Method that makes ship land automatic
        '''
        self.rect.right += 2

        if self.rect.right >= 600:
            self.state = STATES['LANDED']

    def _hiding(self):
        '''
        Method that makes ship hide with the planet
        '''
        self.rect.right += 2

        if self.rect.left >= WIDTH:
            self.state = STATES['HIDDEN']

    def _prepare_ship(self):
        '''
        Prepare the ship for next level
        '''
        self.rect.x = 2
        self.image = SHIP
        self.angle = 0

class Meteor(pg.sprite.Sprite):
    METEORS_IMG = [load_image(METEORS_FOLDER, f'meteor{x}.png') for x in range(1,7)]

    METEORS_DATA = {
        'meteor1':{
            'img':METEORS_IMG[0],
            'height':38,
            'points':50,
        },
        'meteor2':{
            'img':METEORS_IMG[1],
            'height':41,
            'points':50,
        },
        'meteor3':{
            'img':METEORS_IMG[2],
            'height':71,
            'points':250,
        },
        'meteor4':{
            'img':METEORS_IMG[3],
            'height':66,
            'points':250,
        },
        'meteor5':{
            'img':METEORS_IMG[4],
            'height':111,
            'points':500,
        },
        'meteor6':{
            'img':METEORS_IMG[5],
            'height':101,
            'points':500,
        },
    }

    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        self.random_meteor = random.randrange(1,6)

        self.image = self.METEORS_DATA[f'meteor{self.random_meteor}']['img']

        self.rect = self.image.get_rect(
            x=WIDTH, 
            y=random.randrange(50, HEIGHT-self.METEORS_DATA[f'meteor{self.random_meteor}']['height'])
            )

        self.points = self.METEORS_DATA[f'meteor{self.random_meteor}']['points']

        self.vx = random.randint(5, 8)

        self.angle = 0

    def update(self):
        '''
        Update meteor method
        '''
        self.rect.x -= self.vx