import pygame as pg

import os, sys

from tools import *
from config import *

class BlackScreen:

    def __init__(self):
        self.start = False
        self.ship_img, self.ship_rect = load_image(SHIP_FOLDER, 'ship1.png')
        self.ticks = 0

    def on_black(self, screen, level, lifes):
        '''
        Mainloop for black screen
        '''
        while not self.start:
            self.ticks += pg.time.Clock().tick(FPS)
            self._handle_events()
            self._update_screen(screen, level, lifes)
        self.start = False
        self.ticks = 0

    def _handle_events(self):
        '''
        Handling events
        '''
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.start = True

    def _update_screen(self, screen, level, lifes):
        '''
        Method that draws and update the black screen
        '''
        screen.fill(BLACK)

        create_draw_text(screen, SPACE2, 48, f'Level - {level}', WHITE, position='closecenterup')
        create_draw_text(screen, SPACE2, 24, 'Lifes - ', WHITE, position='closecenterleft')

        x_pos_lifes = 5
        for life in range(lifes):
            screen.blit(self.ship_img, ((WIDTH/2-(self.ship_rect.w/2))+x_pos_lifes, HEIGHT/2-(self.ship_rect.w/2)))
            x_pos_lifes += self.ship_rect.w

        if self.ticks <= 500:
            create_draw_text(screen, SPACE2, 24, 'Press < SPACE > to start', WHITE, position='bottomcenter')
        elif self.ticks <= 1000:
            pass
        else:
            self.ticks = 0

        pg.display.flip()

class PauseScreen:
    
    def __init__(self):

        self.option = 0
        self.paused = True
        self.reset = False
        self.main_menu = False

    def on_pause(self, screen):
        '''
        Mainloop of Pause
        We use self.reset to pass if we want to reset to the initial parameters.
        If self reset == False, we continue the game 
        Else, we reset lifes and score as same we start the level
        '''
        
        while self.paused:
            self._handle_events()
            self._draw_paused_menu(self.option, screen)
        self.paused = True
        self.option = 0
        return self.reset, self.main_menu

    def _handle_events(self):
        '''
        Handling events
        '''
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                self._keydown_events(event)

    def _keydown_events(self, event):
        '''
        Handling keydown events
        '''
        if event.key == pg.K_ESCAPE:
            self.paused = False
        if event.key == pg.K_DOWN:
            if self.option < 3:
                OPTION_SOUND.play()
                self.option += 1
        if event.key == pg.K_UP:
            if self.option > 0:
                OPTION_SOUND.play()
                self.option -= 1
        if event.key == pg.K_SPACE:
            SELECTED_SOUND.play()
            self._check_op(self.option)

    def _check_op(self, option):
        '''
        Method that checks the option selected
        Selected Continue -> option = 0
        Selected Restart -> option = 1
        Selected Quit -> option = 2
        '''
        if option == 0:
            self.paused = False
        if option == 1:
            self.paused = False
            self.reset = True
        if option == 2:
            self.paused = False
            self.main_menu = True
        if option == 3:
            pg.quit()
            sys.exit()

    def _draw_paused_menu(self, option, screen):
        '''
        Method that draws the Pause menu
        Draws with red color the selected option
        '''

        load_and_draw_image(screen, IMAGES_FOLDER, 'pause-img.png', x=200, y=170)
        create_draw_text(screen, SPACE2, 48, 'PAUSE', WHITE, position='closecenterup')

        colors = [(RED, WHITE, WHITE, WHITE), (WHITE, RED, WHITE, WHITE), (WHITE, WHITE, RED, WHITE), (WHITE, WHITE, WHITE, RED)]

        for pos in range(4):
            if pos == option:
                create_draw_text(screen, SPACE2, 32, 'Continue', colors[pos][0], position='center')
                create_draw_text(screen, SPACE2, 32, 'Restart', colors[pos][1], position="closecenterbottom")
                create_draw_text(screen, SPACE2, 32, 'Return to Main Menu', colors[pos][2], position="closecenterbottom2")
                create_draw_text(screen, SPACE2, 32, 'Quit', colors[pos][3], position="closecenterbottom3")    

        pg.display.flip()
