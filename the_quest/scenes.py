import pygame as pg

import sys, os

from scene import *
from tools import *
from folders import *
from config import *
from BBDD import BBDD

from the_quest.sprites import *
from the_quest.optional_screens import *

class InitialAnimation(Scene):

    def __init__(self):
        Scene.__init__(self)

        self.x_pos_ship = 800
        self.y_pos_ship = 110
        self.x_pos_title = 848
        self.y_pos_title = 75

        self.ticks = 0

    def update(self, screen, dt):
        screen.fill(BLACK)

        self.ticks += dt
       
        load_and_draw_image(screen, SHIP_FOLDER, 'ship-title.png', x=self.x_pos_ship, y=self.y_pos_ship)
        create_draw_text(screen, TITLE, 120, 'THE QUEST', WHITE, pos_x=self.x_pos_title, pos_y=self.y_pos_title)

        
        self.x_pos_ship -= 5
        if self.x_pos_title > 68.0:
            self.x_pos_title -= 5
        if self.x_pos_ship <= -60:
            self.switchToScene(TitleScene())
        
        pg.display.flip()

class TitleScene(Scene):
    def __init__(self):
        Scene.__init__(self)

        self.option = 0

        self.title_sound = load_sound(SOUNDS_FOLDER, 'title-screen.wav')
        self.title_sound.set_volume(BACKGROUND_VOL)
        self.title_sound.play()

    def _keydown_events(self, event, screen):
        Scene._keydown_events(self, event, screen)
        if event.key == pg.K_DOWN:
            if self.option < 3:
                self.option += 1
                OPTION_SOUND.play()
        if event.key == pg.K_UP:
            if self.option > 0:
                self.option -= 1
                OPTION_SOUND.play()
        if event.key == pg.K_SPACE:
            SELECTED_SOUND.play()
            self._check_op()

    def _check_op(self):
        if self.option == 0:
            # Start New Game
            self.title_sound.stop()
            self.switchToScene(Fade())
        elif self.option == 1:
            # How To Play Screen
            self.title_sound.stop()
            self.switchToScene(HowToPlay())
            pass        
        elif self.option == 2:
            self.title_sound.stop()
            self.switchToScene(Records(5))
        else:
            # Exit Game
            self.terminateScene()

    def update(self, screen, dt):
        screen.fill(BLACK)
        create_draw_text(screen, TITLE, 120, 'THE QUEST', WHITE, position='topcenter', width=WIDTH, height=HEIGHT)
        self._draw_options(screen)

        pg.display.flip()

    def _draw_options(self, screen):
        
        text = ['New Game', 'How To Play', 'Records', 'Exit']
        pos = ['center', 'closecenterbottom', 'closecenterbottom2', 'closecenterbottom3']

        for x in range(4):
            if x == self.option:
                create_draw_text(screen, SPACE, 24, text[x], RED, position=pos[x], width=WIDTH, height=HEIGHT)
            else:
                create_draw_text(screen, SPACE, 24, text[x], WHITE, position=pos[x], width=WIDTH, height=HEIGHT)

class HowToPlay(Scene):
    def __init__(self):
        Scene.__init__(self)

    def _keydown_events(self, event, screen):
        Scene._keydown_events(self, event, screen)
        if event.key == pg.K_SPACE:
            self.switchToScene(TitleScene())

    def update(self, screen, dt):
        # TODO: for-loop?
        self.ticks += dt

        screen.fill(BLACK)
        create_draw_text(screen, SPACE2, 54, 'HOW TO PLAY', WHITE, position='topcenter', width=WIDTH, height=HEIGHT)
        create_draw_text(screen, SPACE, 20, 'Keys to use:', WHITE, position='closecenterup', width=WIDTH, height=HEIGHT)

        load_and_draw_image(screen, HOW_TO_FOLDER, 'up.png', 40, 280)
        load_and_draw_image(screen, HOW_TO_FOLDER, 'down.png', 40, 360)
        load_and_draw_image(screen, HOW_TO_FOLDER, 'spacebar.png', 390, 280)
        load_and_draw_image(screen, HOW_TO_FOLDER, 'escape.png', 390, 360)

        create_draw_text(screen, SPACE, 16, 'Moves ship up', WHITE, pos_x=120, pos_y=300)
        create_draw_text(screen, SPACE, 16, 'Moves ship down', WHITE, pos_x=120, pos_y=380)
        create_draw_text(screen, SPACE, 16, 'Action/Accept Key', WHITE, pos_x=520, pos_y=300)
        create_draw_text(screen, SPACE, 16, 'Quit the game', WHITE, pos_x=480, pos_y=380)
        
        self._blink_message(screen, SPACE, 16, 'Press < SPACE > to go Main Menu', WHITE, position='bottomcenter')

        pg.display.update()

class HowToPlay2(Scene):
    #TODO: Explain the landing positions
    pass

class Records(Scene):

    def __init__(self, score):
        Scene.__init__(self)

        self.score = score
        BBDD()._set_records_to_five()

    def _keydown_events(self, event, screen):
        Scene._keydown_events(self, event, screen)
        if event.key == pg.K_SPACE:
            self.switchToScene(TitleScene())
        if event.key == pg.K_r:
            BBDD().reset_records()

    def update(self, screen, dt):
        self.ticks += dt
        screen.fill(BLACK)
        # Draws static text
        create_draw_text(screen, SPACE, 12, 'Press R to reset records', WHITE, pos_x=10, pos_y=10)
        create_draw_text(screen, SPACE2, 54, 'RECORDS', WHITE, position='topcenter', width=WIDTH, height=HEIGHT)
        create_draw_text(screen, SPACE, 20, 'RANK', WHITE, pos_x=150, pos_y=180)
        create_draw_text(screen, SPACE, 20, 'SCORE', WHITE, pos_x=340, pos_y=180)
        create_draw_text(screen, SPACE, 20, 'NAME', WHITE, pos_x=550, pos_y=180)

        records = BBDD().get_dict_records(BBDD()._select_records())

        # Draws records
        rank_y=230
        for x in range(1,6):
            create_draw_text(screen, SPACE, 16, records[f'record{x}']['rank'], records[f'record{x}']['color'], pos_x=190, pos_y=rank_y)
            create_draw_text(screen, SPACE, 16, str(records[f'record{x}']['score']), records[f'record{x}']['color'], pos_x=350, pos_y=rank_y)
            create_draw_text(screen, SPACE, 16, records[f'record{x}']['name'], records[f'record{x}']['color'], pos_x=560, pos_y=rank_y)
            rank_y += 40

        self._blink_message(screen, SPACE, 16, 'Press < SPACE > to go Main Menu', WHITE, position='bottomcenter')

        pg.display.flip()

class Fade(Scene):
    # TODO: Class Fade for fade into more levels
    def __init__(self):
        Scene.__init__(self)
        self.fade = pg.Surface((WIDTH, HEIGHT))
        self.fade.fill((BLACK))
        self.bg_img = load_image(IMAGES_FOLDER, 'background.png', rect=False)

    def update(self, screen, dt):
        
        self._fade_out(screen)
        self._fade_in(screen)
        self.switchToScene(StartingGame())

    def _fade_out(self, screen):
        for alpha in range(0, 255):
            self.fade.set_alpha(alpha)            
            screen.blit(self.fade, (0,0))
            pg.display.flip()
            pg.time.delay(5)

    def _fade_in(self, screen):
        for alpha in range(255, 0, -1):
            self.fade.set_alpha(alpha)
            screen.blit(self.bg_img, (0,0))
            screen.blit(self.fade, (0,0))
            pg.display.flip()
            pg.time.delay(5)

class StartingGame(Scene):

    def __init__(self):
        Scene.__init__(self)
        self.ship_img, self.ship_rect = load_image(SHIP_FOLDER, 'ship.png')
        self.ix_pos = -50

    def _keydown_events(self, event, screen):
        Scene._keydown_events(self, event, screen)
        if event.key == pg.K_SPACE and self.ix_pos == 0:
            self.switchToScene(Level1('JUPITER', 1, GameOver()))

    def update(self, screen, dt):
        
        self.ticks += dt

        load_and_draw_image(screen, IMAGES_FOLDER, 'background.png')
        load_and_draw_image(screen, IMAGES_FOLDER, 'score1.png', y=self.ix_pos)
        create_draw_text(screen, SPACE, 16, f'Lifes - {LIFES}', WHITE, pos_x=50, pos_y=self.ix_pos+15)
        create_draw_text(screen, SPACE, 16, 'Meteors Dodged - 0' , WHITE, pos_x=240, pos_y=self.ix_pos+15)
        create_draw_text(screen, SPACE, 16, 'Score - 0', WHITE, pos_x=580, pos_y=self.ix_pos+15)
        screen.blit(self.ship_img, (self.ix_pos, 276))

        if self.ix_pos == 0:
            create_draw_text(screen, SPACE2, 54, 'READY?', WHITE, position='closecenterup', width=WIDTH, height=HEIGHT)
            self._blink_message(screen, SPACE, 16, 'Press < SPACE > to start', WHITE, position='center')

        if self.ix_pos != 0:
            if self.ticks >= 85:
                self.ix_pos += 1
                self.ticks = 0

        pg.display.flip()

class Level1(LevelScene):

    def __init__(self, planet_name, level, go_scene):
        LevelScene.__init__(self, planet_name, level, go_scene)

    def _keydown_events(self, event, screen):
        LevelScene._keydown_events(self, event, screen)
        # Click for finish level
        if self.ship.state == STATES['HIDDEN']:
            # Level Finished
            self.ship._prepare_ship()
            self._end_update_score()
            self.bg_sound.stop()
            self.switchToScene(Level2('MARS', 2, GameOver(), self.score, self.ship.lifes))
        if event.key == pg.K_p:
            # Pause Menu
            reset = self.pause_screen.on_pause(screen)
            if reset:
                self._reset(all_data=True)
                self.switchToScene(StartingGame())
    
    def _reset(self, all_data=False):
        LevelScene._reset(self)
        self.score = 0
        if all_data:
            self.ship.lifes = LIFES

class Level2(AdvancedLevelScene):

    def __init__(self, planet_img, level, go_scene, score, lifes):
        AdvancedLevelScene.__init__(self, planet_img, level, go_scene, score, lifes)

    def _keydown_events(self, event, screen):
        LevelScene._keydown_events(self, event, screen)
        # Click for finish level
        if self.ship.state == STATES['HIDDEN']:
            # Level Finished
            self.ship._prepare_ship()
            self._end_update_score()
            self.bg_sound.stop()
            if BBDD().check_new_record(self.score):
                self.switchToScene(NewRecord(self.score)) # <- Scene Next Level/Records
            else:
                self.switchToScene(TitleScene())
        if event.key == pg.K_p:
            # Pause Menu
            reset = self.pause_screen.on_pause(screen)
            if reset:
                self._reset(all_data=True)
                self.switchToScene(Level2('MARS', 2, GameOver(), self.score, self.ship.lifes))
    
    def _reset(self, all_data=False):
        AdvancedLevelScene._reset(self)
        if all_data:
            self.ship.lifes = self.remaining_lifes

class BlackScene(Scene):
    # TODO: Finish and implements in game
    def __init__(self, last_scene, level_playing, lifes):
        Scene.__init__(self)
        self.last_scene = last_scene
        self.ship_img, self.ship_rect = load_image(SHIP_FOLDER, 'ship.png')
        self.level = level_playing
        self.remaining_lifes = lifes

    def update(self, screen, dt):
        screen.fill(BLACK)

        create_draw_text(screen, SPACE2, 32, f'Level - {self.level}', WHITE, position='closecenterup', width=WIDTH, height=HEIGHT)
        create_draw_text(screen, SPACE, 16, 'Lifes - ', WHITE, position='closecenterleft', width=WIDTH, height=HEIGHT)

        x_pos_lifes = 0
        for life in range(self.remaining_lifes):
            screen.blit(self.ship_img, ((WIDTH/2-(self.ship_rect.w/2))+x_pos_lifes, HEIGHT/2-(self.ship_rect.w/2)))
            x_pos_lifes += self.ship_rect.wç

        self._blink_message(screen, SPACE, 16, 'Press < SPACE > to start', WHITE, position='bottomcenter')

        pg.display.flip()

    def _keydown_events(self, event, screen):
        Scene._keydown_events(self, event, screen)
        if event.key == pg.K_SPACE:
            self.switchToScene(self.last_scene)

class GameOver(Scene):

    def __init__(self):
        Scene.__init__(self)

    def _keydown_events(self, event, screen):
        Scene._keydown_events(self, event, screen)
        if event.key == pg.K_SPACE:
            self.switchToScene(TitleScene())

    def update(self, screen, dt):
        screen.fill(BLACK)
        self.ticks += dt
        
        create_draw_text(screen, SPACE2, 64, 'GAME OVER', WHITE, position='center', width=WIDTH, height=HEIGHT)
        
        self._blink_message(screen, SPACE, 16, 'Press < SPACE > to Main Menu', WHITE, position='bottomcenter')
        
        pg.display.flip()

class NewRecord(Scene):

    def __init__(self, score):
        Scene.__init__(self)

        n = [x for x in range(1,27)]
        l = [x for x in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ']
        self.options = dict(zip(n, l))

        self.sel_option = 1
        self.l = []

        self.record = score
        self.recorded = False

    def _keydown_events(self, event, screen):
        Scene._keydown_events(self, event, screen)
        if event.key == pg.K_UP and self.sel_option > 1:
            self.sel_option -= 1
        if event.key == pg.K_DOWN and self.sel_option < 26:
            self.sel_option += 1
        if event.key == pg.K_SPACE: 
            if len(self.l) != 3:
                self.l.append(self.options[self.sel_option])
                self.sel_option = 1
            else:
                if not self.recorded:
                    name = ''.join(self.l)
                    BBDD().insert_new_record((self.record, name))
                    self.recorded = True
                else:
                    self.switchToScene(TitleScene())


    def update(self, screen, dt):
        self.ticks += dt
        screen.fill(BLACK)

        create_draw_text(screen, SPACE2, 54, 'NEW RECORD!', WHITE, position='topcenter', width=WIDTH, height=HEIGHT)
        create_draw_text(screen, SPACE2, 42, 'SCORE :', WHITE, pos_x=220, pos_y=220)
        create_draw_text(screen, SPACE2, 42, str(self.record), WHITE, pos_x=400, pos_y=220)
        create_draw_text(screen, SPACE2, 32, 'INSERT YOUR NAME HERE :', WHITE, pos_x=180, pos_y=320)

        self._draw_name(screen)

        pg.display.flip()

    def _draw_name(self, screen):
        
        x = 590 # x position for letters

        if not self.l: # No letters yet
            create_draw_text(screen, SPACE2, 26, self.options[self.sel_option], WHITE, pos_x=x, pos_y=325)

        else: # if letters writted
            for element in self.l:
                create_draw_text(screen, SPACE2, 26, element, WHITE, pos_x=x, pos_y=325)
                x += 30

            if len(self.l) < 3: # Not all letters writted
                create_draw_text(screen, SPACE2, 26, self.options[self.sel_option], WHITE, pos_x=x, pos_y=325)

            else: # All letters writted

                if not self.recorded: # Record no saved yet
                    self._blink_message(screen, SPACE2, 26, 'Press < SPACE > to enter your record', WHITE, position='bottomcenter')

                else: # Record saved
                    self._blink_message(screen, SPACE2, 26, 'Press < SPACE > to go to main menu', WHITE, position='bottomcenter')