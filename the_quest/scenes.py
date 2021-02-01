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
    '''
    Class for show initial animation of Title
    '''
    def __init__(self):
        Scene.__init__(self)

        self.x_pos_ship = 800 # For the movement of ship
        self.y_pos_ship = 110
        self.x_pos_title = 848 # For the movement of Title
        self.y_pos_title = 75

    def update(self, screen, dt):
        screen.fill(BLACK)

        load_and_draw_image(screen, SHIP_FOLDER, 'ship1-left.png', x=self.x_pos_ship, y=self.y_pos_ship)
        create_draw_text(screen, TITLE, 120, 'THE QUEST', WHITE, pos_x=self.x_pos_title, pos_y=self.y_pos_title)

        self.x_pos_ship -= 5
        if self.x_pos_title > 68.0:
            self.x_pos_title -= 5
        if self.x_pos_ship <= -60:
            # When title is on position we switch to TitleScene
            self.switchToScene(TitleScene())
        
        pg.display.flip()

class TitleScene(Scene):
    '''
    Class who draws the TitleScene
    '''
    def __init__(self):
        Scene.__init__(self)

        self.option = 0

        # Title Music
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
        '''
        Method to know which option was choosed.
        We switch to that Scene
        '''        
        if self.option == 0:
            # Start New Game
            self.title_sound.stop()
            self.switchToScene(Fade(load_image(IMAGES_FOLDER, 'background.png', rect=False), Transition(Level1('JUPITER', 1, GameOver()), 3, 0)))
        elif self.option == 1:
            # How To Play Screen
            self.title_sound.stop()
            self.switchToScene(HowToPlay())
        elif self.option == 2:
            self.title_sound.stop()
            self.switchToScene(Records())
        else:
            # Exit Game
            self.terminateScene()

    def update(self, screen, dt):
        screen.fill(BLACK)
        create_draw_text(screen, TITLE, 120, 'THE QUEST', WHITE, position='topcenter')
        
        self._draw_options(screen)

        pg.display.flip()

    def _draw_options(self, screen):
        
        text = ['New Game', 'How To Play', 'Records', 'Exit']
        pos = ['center', 'closecenterbottom', 'closecenterbottom2', 'closecenterbottom3']

        for x in range(4):
            if x == self.option:
                create_draw_text(screen, SPACE2, 36, text[x], RED, position=pos[x])
            else:
                create_draw_text(screen, SPACE2, 36, text[x], WHITE, position=pos[x])

class HowToPlay(Scene):
    '''
    Class To show How To Play page 1
    '''
    def __init__(self):
        Scene.__init__(self)

    def _keydown_events(self, event, screen):
        Scene._keydown_events(self, event, screen)
        if event.key == pg.K_SPACE:
            self.switchToScene(TitleScene())
        if event.key == pg.K_RIGHT:
            self.switchToScene(HowToPlay2())

    def update(self, screen, dt):
        self.ticks += dt
        screen.fill(BLACK)
        
        self._draw_main_text(screen)
        self._draw_keys(screen)
        self._draw_keys_text(screen)

        pg.display.update()

    def _draw_main_text(self, screen):
        create_draw_text(screen, SPACE2, 54, 'HOW TO PLAY', WHITE, position='topcenter')
        create_draw_text(screen, SPACE2, 36, 'Keys to use:', WHITE, position='closecenterup')
        self._blink_message(screen, SPACE2, 24, 'Press < SPACE > to go Main Menu', WHITE, position='bottomcenter')
        create_draw_text(screen, SPACE2, 16, 'Press <RIGHT> to next page', WHITE, pos_x=460, pos_y=552)
        create_draw_text(screen, SPACE2, 20, '1/3', WHITE, pos_x=720, pos_y=550)

    def _draw_keys(self, screen):
        load_and_draw_image(screen, HOW_TO_FOLDER, 'up.png', 40, 280)
        load_and_draw_image(screen, HOW_TO_FOLDER, 'down.png', 40, 360)
        load_and_draw_image(screen, HOW_TO_FOLDER, 'spacebar.png', 390, 280)
        load_and_draw_image(screen, HOW_TO_FOLDER, 'escape.png', 390, 360)

    def _draw_keys_text(self, screen):
        create_draw_text(screen, SPACE2, 24, 'Moves ship up', WHITE, pos_x=120, pos_y=300)
        create_draw_text(screen, SPACE2, 24, 'Moves ship down', WHITE, pos_x=120, pos_y=380)
        create_draw_text(screen, SPACE2, 24, 'Action/Accept Key', WHITE, pos_x=520, pos_y=300)
        create_draw_text(screen, SPACE2, 24, 'Quit the game', WHITE, pos_x=520, pos_y=380)

class HowToPlay2(Scene):
    '''
    Class To show How To Play page 2
    '''
    def __init__(self):
        Scene.__init__(self)
        self.bg_img = load_image(IMAGES_FOLDER, 'background.png', rect=False)
        self.ship_img, self.ship_rect = load_image(SHIP_FOLDER, 'ship1.png')
        self.planet = load_image(IMAGES_FOLDER, 'JUPITER.png', rect=False)

    def _keydown_events(self, event, screen):
        Scene._keydown_events(self, event, screen)
        if event.key == pg.K_SPACE:
            self.switchToScene(TitleScene())
        if event.key == pg.K_LEFT:
            self.switchToScene(HowToPlay())
        if event.key == pg.K_RIGHT:
            self.switchToScene(HowToPlay3())

    def update(self, screen, dt):
        screen.blit(self.bg_img, (0, 0))
        screen.blit(self.planet, (530, 50))
        screen.blit(self.ship_img, (2, (HEIGHT/2)-24))

        self._top_level_menu(screen)
        self._draw_main_text(screen)
        self._landing_lines(screen)
        self._landing_messages(screen)

        pg.display.flip()

    def _draw_main_text(self, screen):
        create_draw_text(screen, SPACE2, 50, 'POSITIONS TO LAND', WHITE, position='topcenter')
        create_draw_text(screen, SPACE2, 16, 'Press <LEFT> <RIGHT> to switch page', WHITE, pos_x=80, pos_y=552)
        create_draw_text(screen, SPACE2, 20, '2/3', WHITE, pos_x=20, pos_y=550)

    def _top_level_menu(self, screen):
        top_level_img, top_level_img_rect = load_image(IMAGES_FOLDER, 'score1.png')

        create_draw_text(screen, SPACE2, 24, f'Lifes - 3', WHITE, pos_x=50, pos_y=10)
        create_draw_text(screen, SPACE2, 24, f'Meteors Dodged - 0', WHITE, pos_x=240, pos_y=10)
        create_draw_text(screen, SPACE2, 24, f'Score - 0', WHITE, pos_x=580, pos_y=10)
        
        screen.blit(top_level_img, (0, 0))

    def _landing_lines(self, screen):

        # Rotating Zone
        pg.draw.line(screen, SILVER, (0, 70), (20, 70))
        pg.draw.line(screen, SILVER, (0, HEIGHT-20), (20, HEIGHT-20))

        # Perfect Landing
        pg.draw.line(screen, GREEN, (0, (HEIGHT/2)-40), (20, (HEIGHT/2)-40))
        pg.draw.line(screen, GREEN, (0, (HEIGHT/2)+40), (20, (HEIGHT/2)+40))

        # Succesfully Landing
        pg.draw.line(screen, ORANGE, (0, (HEIGHT/2)-80), (20, (HEIGHT/2)-80))
        pg.draw.line(screen, ORANGE, (0, (HEIGHT/2)+80), (20, (HEIGHT/2)+80))

        # Not Bad Landing
        pg.draw.line(screen, RED, (0, (HEIGHT/2)-120), (20, (HEIGHT/2)-120))
        pg.draw.line(screen, RED, (0, (HEIGHT/2)+120), (20, (HEIGHT/2)+120))

    def _landing_messages(self, screen):

        create_draw_text(screen, SPACE2, 16, 'ROTATING ZONE', SILVER, pos_x=25 ,pos_y=63)
        create_draw_text(screen, SPACE2, 16, 'PERFECT LANDING', GREEN, pos_x=25 ,pos_y=(HEIGHT/2)-47)
        create_draw_text(screen, SPACE2, 16, 'SUCCESSFULLY LANDING', ORANGE, pos_x=25 ,pos_y=(HEIGHT/2)-87)
        create_draw_text(screen, SPACE2, 16, 'NOT BAD LANDING', RED, pos_x=25 ,pos_y=(HEIGHT/2)-127)

class HowToPlay3(Scene):
    '''
    Class To show How To Play page 3
    '''
    def __init__(self):
        Scene.__init__(self)

    def _keydown_events(self, event, screen):
        Scene._keydown_events(self, event, screen)
        if event.key == pg.K_SPACE:
            self.switchToScene(TitleScene())
        if event.key == pg.K_LEFT:
            self.switchToScene(HowToPlay2())

    def update(self, screen, dt):
        self.ticks += dt
        screen.fill(BLACK)

        self._draw_main_text(screen)
        self._draw_landing_text(screen)
        self._draw_lifes_text(screen)

        pg.display.flip()

    def _draw_main_text(self, screen):
        create_draw_text(screen, SPACE2, 50, 'ADDITIONAL BONUS', WHITE, position='topcenter')
        create_draw_text(screen, SPACE2, 20, '- At the end of each level we can get a bonus based on:', WHITE, pos_x=100, pos_y=150)
        create_draw_text(screen, SPACE2, 16, 'Press <LEFT> to previous page', WHITE, pos_x=80, pos_y=552)
        create_draw_text(screen, SPACE2, 20, '3/3', WHITE, pos_x=20, pos_y=550)
        self._blink_message(screen, SPACE2, 24, 'Press < SPACE > to go Main Menu', WHITE, position='bottomcenter')
    
    def _draw_landing_text(self, screen):
        create_draw_text(screen, SPACE2, 20, '- Landing:', WHITE, pos_x=200, pos_y=200)
        create_draw_text(screen, SPACE2, 20, 'PERFECT = 1000 pts', GREEN, pos_x=330, pos_y=200)
        create_draw_text(screen, SPACE2, 20, 'SUCCESSFULLY = 500 pts', ORANGE, pos_x=330, pos_y=240)
        create_draw_text(screen, SPACE2, 20, 'NOT BAD = 250 pts', RED, pos_x=330, pos_y=280)

    def _draw_lifes_text(self, screen):
        create_draw_text(screen, SPACE2, 20, '- Lifes:', WHITE, pos_x=200, pos_y=330)
        create_draw_text(screen, SPACE2, 20, '3 LIFES = 1000 pts', GREEN, pos_x=330, pos_y=330)
        create_draw_text(screen, SPACE2, 20, '2 LIFES = 500 pts', ORANGE, pos_x=330, pos_y=370)
        create_draw_text(screen, SPACE2, 20, '1 LIFE = 250 pts', RED, pos_x=330, pos_y=410)

class Records(Scene):
    '''
    Class To show Records
    '''
    def __init__(self):
        Scene.__init__(self)

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
        create_draw_text(screen, SPACE2, 20, 'Press R to reset records', WHITE, pos_x=10, pos_y=10)
        create_draw_text(screen, SPACE2, 54, 'RECORDS', WHITE, position='topcenter')
        create_draw_text(screen, SPACE2, 28, 'RANK', WHITE, pos_x=150, pos_y=180)
        create_draw_text(screen, SPACE2, 28, 'SCORE', WHITE, pos_x=340, pos_y=180)
        create_draw_text(screen, SPACE2, 28, 'NAME', WHITE, pos_x=550, pos_y=180)

        # Records stored in our database
        records = BBDD().get_dict_records(BBDD()._select_records())

        # Draws records
        rank_y=230
        for x in range(1,6):
            create_draw_text(screen, SPACE2, 24, records[f'record{x}']['rank'], records[f'record{x}']['color'], pos_x=190, pos_y=rank_y)
            create_draw_text(screen, SPACE2, 24, str(records[f'record{x}']['score']), records[f'record{x}']['color'], pos_x=350, pos_y=rank_y)
            create_draw_text(screen, SPACE2, 24, records[f'record{x}']['name'], records[f'record{x}']['color'], pos_x=560, pos_y=rank_y)
            rank_y += 40

        self._blink_message(screen, SPACE2, 24, 'Press < SPACE > to go Main Menu', WHITE, position='bottomcenter')

        pg.display.flip()

class Fade(Scene):
    '''
    Class to makes the fade from one scene to another
    next_level_bg = we indicate the background of next level
    to make a soft fade, only if its a fade to a level game, 
    else, we indicate as None and we use fade surface
    next_scene = to indicate the next scene after the fade
    effect
    '''
    def __init__(self, next_level_bg, next_scene):
        Scene.__init__(self)
        self.fade = pg.Surface((WIDTH, HEIGHT))
        self.fade.fill(BLACK)
        self.nxt_lvl_bg = next_level_bg
        self.next_scene = next_scene

    def update(self, screen, dt):
        
        self._fade_out(screen)
        self._fade_in(screen)
        self.switchToScene(self.next_scene)

    def _fade_out(self, screen):
        for alpha in range(0, 255):
            self.fade.set_alpha(alpha)            
            screen.blit(self.fade, (0,0))
            pg.display.flip()
            pg.time.delay(5)

    def _fade_in(self, screen):
        for alpha in range(255, 0, -1):
            self.fade.set_alpha(alpha)
            if self.nxt_lvl_bg:
                screen.blit(self.nxt_lvl_bg, (0,0))
            else:
                screen.blit(self.fade, (0,0))
            screen.blit(self.fade, (0,0))
            pg.display.flip()
            pg.time.delay(5)

class Transition(Scene):
    '''
    Class who makes the animation of top level and ship appears
    at same time
    next_level = indicates the next level to start
    lifes = to show in top level the remaining lifes if isn't the
    first level
    score = same as lifes
    '''
    def __init__(self, next_level, lifes, score):
        Scene.__init__(self)
        self.ship_img, self.ship_rect = load_image(SHIP_FOLDER, 'ship1.png')
        self.ix_pos = -50
        self.next_level = next_level
        self.lifes = lifes
        self.score = score

    def _keydown_events(self, event, screen):
        Scene._keydown_events(self, event, screen)
        if event.key == pg.K_SPACE and self.ix_pos == 0:
            self.switchToScene(self.next_level)

    def update(self, screen, dt):
        self.ticks += dt

        load_and_draw_image(screen, IMAGES_FOLDER, 'background.png')
        load_and_draw_image(screen, IMAGES_FOLDER, 'score1.png', y=self.ix_pos)
        create_draw_text(screen, SPACE2, 24, f'Lifes - {self.lifes}', WHITE, pos_x=50, pos_y=self.ix_pos+10)
        create_draw_text(screen, SPACE2, 24, 'Meteors Dodged - 0' , WHITE, pos_x=240, pos_y=self.ix_pos+10)
        create_draw_text(screen, SPACE2, 24, f'Score - {self.score}', WHITE, pos_x=580, pos_y=self.ix_pos+10)
        screen.blit(self.ship_img, (self.ix_pos, 276))

        if self.ix_pos == 0:
            create_draw_text(screen, SPACE2, 54, 'READY?', WHITE, position='closecenterup')
            self._blink_message(screen, SPACE2, 24, 'Press < SPACE > to start', WHITE, position='center')

        if self.ix_pos != 0:
            if self.ticks >= 85:
                self.ix_pos += 1
                self.ticks = 0

        pg.display.flip()

class Level1(LevelScene):
    '''
    Class for first level of game
    planet_name = name of our image for load and for use at the end 
    of level for show which planet we conquered
    level = for blackscreen who needs to know which level he has
    to show(see "optional_screens - BlackScreen()")
    go_scene = GameOver scene if ship state is "DEAD"
    '''
    def __init__(self, planet_name, level, go_scene):
        LevelScene.__init__(self, planet_name, level, go_scene)

    def _keydown_events(self, event, screen):
        LevelScene._keydown_events(self, event, screen)
        # Click for finish level
        if self.ship.state == STATES['HIDDEN']:
            # Level Finished
            self.ship._prepare_ship()
            self.bg_sound.stop()
            self.switchToScene(Fade(load_image(IMAGES_FOLDER, 'background.png', rect=False), (Transition(Level2('MARS', 2, GameOver(), self.score, self.ship.lifes), self.ship.lifes, self.score))))

        if event.key == pg.K_p and self.ship.state == STATES['ALIVE']:
            # Pause Menu
            pg.mixer.pause()
            reset = self.pause_screen.on_pause(screen)
            if reset:
                pg.mixer.stop()
                self._reset(all_data=True)
                self.switchToScene(Transition(Level1('JUPITER', 1, GameOver()), self.ship.lifes, self.score))
            pg.mixer.unpause()
    
    def _reset(self, all_data=False):
        LevelScene._reset(self)
        self.score = 0
        if all_data:
            self.ship.lifes = LIFES

class Level2(AdvancedLevelScene):
    '''
    Class for second level of game
    score = for add the last score from last level
    lifes = same as score
    '''

    def __init__(self, planet_img, level, go_scene, score, lifes):
        AdvancedLevelScene.__init__(self, planet_img, level, go_scene, score, lifes)

    def _keydown_events(self, event, screen):
        '''
        We check if our final score is better than our database
        records scores. If beats anyone of them, we will switch
        to NewRecord scene, else, to NoRecord scene
        '''
        LevelScene._keydown_events(self, event, screen)
        # Click for finish level
        if self.ship.state == STATES['HIDDEN']:
            # Level Finished
            self.ship._prepare_ship()
            self.bg_sound.stop()
            if BBDD().check_new_record(self.score):
                self.switchToScene(Fade(None, NewRecord(self.score))) # <- Scene Next Level/Records
            else:
                self.switchToScene(Fade(None, NoRecord()))
        if event.key == pg.K_p and self.ship.state == STATES['ALIVE']:
            # Pause Menu
            pg.mixer.pause()
            reset = self.pause_screen.on_pause(screen)
            if reset:
                pg.mixer.stop()
                self._reset(all_data=True)
                self.switchToScene(Transition(Level2('MARS', 2, GameOver(), self.score, self.ship.lifes), self.ship.lifes, self.score))
            pg.mixer.unpause()
    
    def _reset(self, all_data=False):
        AdvancedLevelScene._reset(self)
        if all_data:
            self.ship.lifes = self.remaining_lifes

class BlackScene(Scene):
    # TODO: Finish and implements in game
    def __init__(self, last_scene, level_playing, lifes):
        Scene.__init__(self)
        self.last_scene = last_scene
        self.ship_img, self.ship_rect = load_image(SHIP_FOLDER, 'ship1.png')
        self.level = level_playing
        self.remaining_lifes = lifes

    def _keydown_events(self, event, screen):
        Scene._keydown_events(self, event, screen)
        if event.key == pg.K_SPACE:
            self.switchToScene(self.last_scene)

    def update(self, screen, dt):
        self.ticks += dt
        screen.fill(BLACK)

        create_draw_text(screen, SPACE2, 32, f'Level - {self.level}', WHITE, position='closecenterup')
        create_draw_text(screen, SPACE, 16, 'Lifes - ', WHITE, position='closecenterleft')

        x_pos_lifes = 0
        for life in range(self.remaining_lifes):
            screen.blit(self.ship_img, ((WIDTH/2-(self.ship_rect.w/2))+x_pos_lifes, HEIGHT/2-(self.ship_rect.w/2)))
            x_pos_lifes += self.ship_rect.w

        self._blink_message(screen, SPACE, 16, 'Press < SPACE > to start', WHITE, position='bottomcenter')

        pg.display.flip()

class GameOver(Scene):
    '''
    Class who draws GameOver scene
    '''

    def __init__(self):
        Scene.__init__(self)

    def _keydown_events(self, event, screen):
        Scene._keydown_events(self, event, screen)
        if event.key == pg.K_SPACE:
            self.switchToScene(TitleScene())

    def update(self, screen, dt):
        self.ticks += dt

        screen.fill(BLACK)
        
        create_draw_text(screen, SPACE2, 64, 'GAME OVER', WHITE, position='center')
        
        self._blink_message(screen, SPACE2, 24, 'Press < SPACE > to Main Menu', WHITE, position='bottomcenter')
        
        pg.display.flip()

class NewRecord(Scene):
    '''
    Class who draws the NewRecord scene
    '''

    def __init__(self, score):
        Scene.__init__(self)

        n = [x for x in range(1,27)]
        l = [x for x in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ']
        self.options = dict(zip(n, l))

        self.sel_option = 1
        self.l = [] # For store the letters we put in NewRecord

        self.record = score
        self.recorded = False

    def _keydown_events(self, event, screen):
        Scene._keydown_events(self, event, screen)
        if event.key == pg.K_UP and self.sel_option > 1:
            self.sel_option -= 1
            OPTION_SOUND.play()
        if event.key == pg.K_DOWN and self.sel_option < 26:
            self.sel_option += 1
            OPTION_SOUND.play()
        if event.key == pg.K_SPACE: 
            if len(self.l) != 3:
                self.l.append(self.options[self.sel_option])
                self.sel_option = 1
            else:
                if not self.recorded:
                    name = ''.join(self.l)
                    # Inserting new record
                    BBDD().insert_new_record((self.record, name))
                    self.recorded = True
                else:
                    self.switchToScene(TitleScene())
            SELECTED_SOUND.play()


    def update(self, screen, dt):
        self.ticks += dt

        screen.fill(BLACK)

        create_draw_text(screen, SPACE2, 54, 'NEW RECORD!', WHITE, position='topcenter')
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
                    create_draw_text(screen, SPACE2, 26, 'RECORD ADDED SUCCESFULLY!', RED, pos_x=200, pos_y=400)
                    self._blink_message(screen, SPACE2, 26, 'Press < SPACE > to go to main menu', WHITE, position='bottomcenter')

class NoRecord(Scene):
    '''
    Class who draws the NoRecord scene
    '''
    def __init__(self):
        Scene.__init__(self)

    def _keydown_events(self, event, screen):
        Scene._keydown_events(self, event, screen)
        if event.key == pg.K_SPACE:
            self.switchToScene(TitleScene())

    def update(self, screen, dt):
        self.ticks += dt
        screen.fill(BLACK)

        create_draw_text(screen, SPACE2, 54, 'NO RECORD HAS BEEN BEATED', WHITE, position='topcenter')
        self._blink_message(screen, SPACE2, 26, 'Press < SPACE > to go to main menu', WHITE, position='bottomcenter')

        pg.display.flip()