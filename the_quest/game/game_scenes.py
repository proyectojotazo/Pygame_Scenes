import pygame as pg

import sys, os

from folders import *
from tools import *
from config import *
from scene import Scene

from the_quest.game.sprites import *
from the_quest.game.optional_screens import *

class StartingGame(Scene):

    def __init__(self):
        Scene.__init__(self)
        self.ship_img, self.ship_rect = load_image(SHIP_FOLDER, 'ship.xcf')
        self.ix_pos = -50
        self.ticks = 0

    def handle_events(self, screen):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.terminateScene()
            if event.type == pg.KEYDOWN:
                self._keydown_events(event, screen)

    def _keydown_events(self, event, screen):
        if event.key == pg.K_SPACE and self.ix_pos == 0:
            self.switchToScene(RunningGame())

    def update(self, screen, dt):
        
        self.ticks += dt

        load_and_draw_image(screen, IMAGES_FOLDER, 'background.xcf')
        load_and_draw_image(screen, IMAGES_FOLDER, 'score1.png', y=self.ix_pos)
        create_draw_text(screen, SPACE, 16, f'Lifes - {LIFES}', WHITE, pos_x=50, pos_y=self.ix_pos+15)
        create_draw_text(screen, SPACE, 16, 'Meteors Dodged - 0' , WHITE, pos_x=240, pos_y=self.ix_pos+15)
        create_draw_text(screen, SPACE, 16, 'Score - 0', WHITE, pos_x=590, pos_y=self.ix_pos+15)
        screen.blit(self.ship_img, (self.ix_pos, 276))

        if self.ix_pos == 0:
            create_draw_text(screen, SPACE2, 54, 'READY?', WHITE, position='closecenterup', width=WIDTH, height=HEIGHT)
            if self.ticks <= 1000:
                create_draw_text(screen, SPACE, 16, 'Press < SPACE > to start', WHITE, position='center', width=WIDTH, height=HEIGHT)
            elif self.ticks <= 1500:
                pass
            else:
                self.ticks = 0

        if self.ix_pos != 0:
            if self.ticks >= 85:
                self.ix_pos += 1
                self.ticks = 0

        pg.display.flip()

class RunningGame(Scene):

    def __init__(self):
        Scene.__init__(self)
        self.bg_sound = load_sound(SOUNDS_FOLDER, 'background_sound.ogg')
        self.bg_sound.set_volume(BACKGROUND_VOL)
        self.bg_sound.play()

        # Background img
        self.background = load_image(IMAGES_FOLDER, 'background.xcf', rect=False)
        self.background_x = 0 # For moving_background

        self.meteors_timer = 0 # For adding meteors

        self.meteors = pg.sprite.Group()
        self.ship = Ship()
        self.black_screen = BlackScreen()
        self.pause_screen = PauseScreen()

        self.planet, self.rect_planet = load_image(IMAGES_FOLDER, 'jupiter.png', x=WIDTH, y=50)
        self.planet_x = 0 # For moving planet

        self.ticks = 0

        # Vars top level
        self.score = 0
        self.meteors_dodged = 30

    def handle_events(self, screen):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.terminateScene()
            if event.type == pg.KEYDOWN:
                self._keydown_events(event, screen)

    def _keydown_events(self, event, screen):
        if event.key == pg.K_SPACE: 
            if self.ship.state == STATES['ALIVE']\
            and self.meteors_dodged >= METEORS_TO_DODGE\
            and self.planet_x == 272:
                self.ship.state = STATES['ROTATING']
            if self.ship.state == STATES['PREPARED TO LAND']:
                self.ship.state = STATES['LANDING']
            if self.ship.state == STATES['HIDDEN']:
                # Level Finished
                self.switchToScene(None) # <- Scene Next Level
        if event.key == pg.K_p:
            # Pause Menu
            reset = self.pause_screen.on_pause(screen)
            if reset:
                self._reset(all_data=True)
                self.switchToScene(StartingGame())

    def update(self, screen, dt):
        
        self._add_meteors(dt)

        self._move_background(screen)
        self._top_level_menu(screen)
        self._draw_planet(screen, dt)
        screen.blit(self.ship.image, (self.ship.rect.x, self.ship.rect.y))
        self.meteors.draw(screen)
        self._end_level_msg(screen, dt)

        self._update_sprites()

        self._collition()
        
        self._remove_meteors()

        if self.ship.state == STATES['NOT ALIVE']:
            self.black_screen.on_black(screen, self.ship.lifes)
            self._reset()
            self.bg_sound.play()

        pg.display.flip()

    def _update_sprites(self):

        self.ship.update()
        self.meteors.update()

    def _add_meteors(self, dt):
        '''
        Adding meteors, when we reach the maximum meteors dodged we stop
        to add meteors, else, we continue adding meteors
        '''
        if self.meteors_dodged < METEORS_TO_DODGE:
            self.meteors_timer += dt
            if self.meteors_timer >= 85:
                if len(self.meteors) <= MAX_METEORS:
                    self.meteors.add(Meteor())
                self.meteors_timer = 0

    def _remove_meteors(self):
        '''
        Removing meteors.
        If we reach the maximum meteors dodged we stop to add meteors dodged and score
        '''
        for meteor in self.meteors:
            if meteor.rect.right <= 0:
                self.meteors.remove(meteor)
                if self.meteors_dodged < METEORS_TO_DODGE:
                    self.score += meteor.points
                    self.meteors_dodged += 1

    def _collition(self):
        '''
        Collitions method.
        We check the collitions if the state of our ship is 'ALIVE'.
        Then we change the state to 'EXPLODING' and makes the explosion
        sound
        '''
        if self.ship.state == STATES['ALIVE']:
            if pg.sprite.spritecollide(self.ship, self.meteors, True):
                self.ship.state = STATES['EXPLODING']
                self.bg_sound.stop()
                self.ship.explosion_sound.set_volume(0.02)
                self.ship.explosion_sound.play()

    def _move_background(self, screen):
        x_rel = self.background_x % WIDTH
        screen.blit(self.background, (x_rel - WIDTH ,0))
        if x_rel < WIDTH:
            screen.blit(self.background, (x_rel,0))
        self.background_x -= 1

    def _top_level_menu(self, screen):
        top_level_img, top_level_img_rect = load_image(IMAGES_FOLDER, 'score1.png')

        create_draw_text(screen, SPACE, 16, f'Lifes - {self.ship.lifes}', WHITE, pos_x=50, pos_y=15)
        create_draw_text(screen, SPACE, 16, f'Meteors Dodged - {self.meteors_dodged}', WHITE, pos_x=240, pos_y=15)
        create_draw_text(screen, SPACE, 16, f'Score - {self.score}', WHITE, pos_x=590, pos_y=15)
        
        screen.blit(top_level_img, (0, 0))

    def _draw_planet(self, screen, dt):

        if self.meteors_dodged >= METEORS_TO_DODGE:
            if self.ship.state != STATES['LANDED'] and self.ship.state != STATES['HIDDEN']:
                self.ticks += dt
                if self.planet_x <= 270 and self.ticks >= 85:
                    self.planet_x += 2
            else:
                if self.planet_x >= 0:
                    self.planet_x -= 2

            screen.blit(self.planet, (self.rect_planet.x-self.planet_x, self.rect_planet.y))

    def _end_level_msg(self, screen, dt):

        if self.planet_x >= 270:
            if self.ship.state == STATES['ALIVE']:
                create_draw_text(screen, SPACE, 16, 'Press < SPACE > to rotate the ship', WHITE, position='topcenter', width=WIDTH)
            if self.ship.state == STATES['ROTATING']:
                create_draw_text(screen, SPACE, 16, 'Rotating ship, please, wait...', WHITE, position='topcenter', width=WIDTH)
            if self.ship.state == STATES['PREPARED TO LAND']:
                create_draw_text(screen, SPACE, 16, 'Press < SPACE > to land', WHITE, position='topcenter', width=WIDTH)
            if self.ship.state == STATES['LANDING']:
                create_draw_text(screen, SPACE, 16, 'Landing, please, wait...', WHITE, position='topcenter', width=WIDTH)
        else:
            if self.ship.state == STATES['LANDED']:
                create_draw_text(screen, SPACE, 26, 'SUCCESSFULLY LANDED!', WHITE, position='topcenter', width=WIDTH)
            if self.ship.state == STATES['HIDDEN']:
                create_draw_text(screen, SPACE2, 54, 'JUPITER CONQUERED!', WHITE, position='center', width=WIDTH, height=HEIGHT)

                self.ticks += dt

                if self.ticks <= 500:
                    create_draw_text(screen, SPACE, 16, 'Press < SPACE > to continue', WHITE, position='bottomcenter', width=WIDTH, height=HEIGHT)
                elif self.ticks <= 1000:
                    pass
                else:
                    self.ticks = 0

    def _reset(self, all_data=False):
        self.meteors.empty()
        self.ship.state = STATES['ALIVE']
        self.ship.rect.y = 276
        self.background_x = 0
        self.planet_x = 0
        self.meteors_dodged = 0
        self.score = 0
        self.ticks = 0

        if all_data:
            self.ship.lifes = LIFES
