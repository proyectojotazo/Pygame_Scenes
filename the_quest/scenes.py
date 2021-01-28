import pygame as pg

import sys, os

from scene import *
from tools import *
from folders import *
from config import *

from the_quest.sprites import *
from the_quest.optional_screens import *

class InitialAnimation(Scene):

    def __init__(self):
        Scene.__init__(self)

        self.x_pos_ship = 800
        self.y_pos_ship = 110
        self.x_pos_title = 848
        self.y_pos_title = 75

    def update(self, screen, dt):
        screen.fill(BLACK)

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
            # Records Screen
            pass
        else:
            # Exit Game
            self.terminateScene()

    def update(self, screen, dt):
        screen.fill(BLACK)

        create_draw_text(screen, TITLE, 120, 'THE QUEST', WHITE, position='topcenter', width=WIDTH, height=HEIGHT)
        self._draw_options(screen)

        pg.display.flip()

    def _draw_options(self, screen):
        # TODO: Refactor this method
        if self.option == 0:
            create_draw_text(screen, SPACE, 24, 'New Game', RED, position='center', width=WIDTH, height=HEIGHT)
            create_draw_text(screen, SPACE, 24, 'How To Play', WHITE, position='closecenterbottom', width=WIDTH, height=HEIGHT)
            create_draw_text(screen, SPACE, 24, 'Records', WHITE, position='closecenterbottom2', width=WIDTH, height=HEIGHT)
            create_draw_text(screen, SPACE, 24, 'Exit', WHITE, position='closecenterbottom3', width=WIDTH, height=HEIGHT)
        elif self.option == 1:
            create_draw_text(screen, SPACE, 24, 'New Game', WHITE, position='center', width=WIDTH, height=HEIGHT)
            create_draw_text(screen, SPACE, 24, 'How To Play', RED, position='closecenterbottom', width=WIDTH, height=HEIGHT)
            create_draw_text(screen, SPACE, 24, 'Records', WHITE, position='closecenterbottom2', width=WIDTH, height=HEIGHT)
            create_draw_text(screen, SPACE, 24, 'Exit', WHITE, position='closecenterbottom3', width=WIDTH, height=HEIGHT)
        elif self.option == 2:
            create_draw_text(screen, SPACE, 24, 'New Game', WHITE, position='center', width=WIDTH, height=HEIGHT)
            create_draw_text(screen, SPACE, 24, 'How To Play', WHITE, position='closecenterbottom', width=WIDTH, height=HEIGHT)
            create_draw_text(screen, SPACE, 24, 'Records', RED, position='closecenterbottom2', width=WIDTH, height=HEIGHT)
            create_draw_text(screen, SPACE, 24, 'Exit', WHITE, position='closecenterbottom3', width=WIDTH, height=HEIGHT)
        else:
            create_draw_text(screen, SPACE, 24, 'New Game', WHITE, position='center', width=WIDTH, height=HEIGHT)
            create_draw_text(screen, SPACE, 24, 'How To Play', WHITE, position='closecenterbottom', width=WIDTH, height=HEIGHT)
            create_draw_text(screen, SPACE, 24, 'Records', WHITE, position='closecenterbottom2', width=WIDTH, height=HEIGHT)
            create_draw_text(screen, SPACE, 24, 'Exit', RED, position='closecenterbottom3', width=WIDTH, height=HEIGHT)

class Fade(Scene):

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

class HowToPlay(Scene):
    # TODO:Look for keydown events, SPACE to return Main Menu
    # TODO:Finish the update
    def __init__(self):
        Scene.__init__(self)

        self.ticks = 0

    def _keydown_events(self, event, screen):
        Scene._keydown_events(self, event, screen)
        if event.key == pg.K_SPACE:
            self.switchToScene(TitleScene())

    def update(self, screen, dt):

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
        
        if self.ticks <= 1000:
            create_draw_text(screen, SPACE, 16, 'Press < SPACE > to go Main Menu', WHITE, position='bottomcenter', width=WIDTH, height=HEIGHT)
        elif self.ticks <= 1500:
            pass
        else:
            self.ticks = 0

        pg.display.update()

class StartingGame(Scene):

    def __init__(self):
        Scene.__init__(self)
        self.ship_img, self.ship_rect = load_image(SHIP_FOLDER, 'ship.png')
        self.ix_pos = -50
        self.ticks = 0

    def _keydown_events(self, event, screen):
        Scene._keydown_events(self, event, screen)
        if event.key == pg.K_SPACE and self.ix_pos == 0:
            self.switchToScene(Level1Test('JUPITER', 1, GameOver()))

    def update(self, screen, dt):
        
        self.ticks += dt

        load_and_draw_image(screen, IMAGES_FOLDER, 'background.png')
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

class Level1Test(LevelScene):

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
            self.switchToScene(Level2Test('MARS', 2, GameOver(), self.score, self.ship.lifes))
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

class Level2Test(AdvancedLevelScene):

    def __init__(self, planet_img, level, go_scene, score, lifes):
        AdvancedLevelScene.__init__(self, planet_img, level, go_scene, score, lifes)

    def _keydown_events(self, event, screen):
        LevelScene._keydown_events(self, event, screen)
        # Click for finish level
        if self.ship.state == STATES['HIDDEN']:
            # Level Finished
            self.ship._prepare_ship() # Delete if last level
            self._end_update_score()
            self.bg_sound.stop()
            self.switchToScene(TitleScene()) # <- Scene Next Level
        if event.key == pg.K_p:
            # Pause Menu
            reset = self.pause_screen.on_pause(screen)
            if reset:
                self._reset(all_data=True)
                self.switchToScene(Level2Test('MARS', 2, GameOver(), self.score, self.ship.lifes))
    
    def _reset(self, all_data=False):
        AdvancedLevelScene._reset(self)
        if all_data:
            self.ship.lifes = self.remaining_lifes

class BlackScene(Scene):

    def __init__(self, last_scene, level_playing, lifes):
        Scene.__init__(self)
        self.last_scene = last_scene
        self.ship_img, self.ship_rect = load_image(SHIP_FOLDER, 'ship.png')
        self.ticks = 0
        self.level = level_playing
        self.remaining_lifes = lifes

    def update(self, screen, dt):
        screen.fill(BLACK)

        create_draw_text(screen, SPACE2, 32, f'Level - {self.level}', WHITE, position='closecenterup', width=WIDTH, height=HEIGHT)
        create_draw_text(screen, SPACE, 16, 'Lifes - ', WHITE, position='closecenterleft', width=WIDTH, height=HEIGHT)

        x_pos_lifes = 0
        for life in range(self.remaining_lifes):
            screen.blit(self.ship_img, ((WIDTH/2-(self.ship_rect.w/2))+x_pos_lifes, HEIGHT/2-(self.ship_rect.w/2)))
            x_pos_lifes += self.ship_rect.w

        if self.ticks <= 500:
            create_draw_text(screen, SPACE, 16, 'Press < SPACE > to start', WHITE, position='bottomcenter', width=WIDTH, height=HEIGHT)
        elif self.ticks <= 1000:
            pass
        else:
            self.ticks = 0

        pg.display.flip()

    def _keydown_events(self, event, screen):
        Scene._keydown_events(self, event, screen)
        if event.key == pg.K_SPACE:
            self.switchToScene(self.last_scene)

class GameOver(Scene):

    def __init__(self):
        Scene.__init__(self)

        self.ticks = 0

    def _keydown_events(self, event, screen):
        Scene._keydown_events(self, event, screen)
        if event.key == pg.K_SPACE:
            self.switchToScene(TitleScene())


    def update(self, screen, dt):
        screen.fill(BLACK)
        self.ticks += dt
        create_draw_text(screen, SPACE2, 64, 'GAME OVER', WHITE, position='center', width=WIDTH, height=HEIGHT)
        if self.ticks <= 500:
            create_draw_text(screen, SPACE, 16, 'Press < SPACE > to Main Menu', WHITE, position='bottomcenter', width=WIDTH, height=HEIGHT)
        elif self.ticks <= 1000:
            pass
        else:
            self.ticks = 0

        pg.display.flip()
