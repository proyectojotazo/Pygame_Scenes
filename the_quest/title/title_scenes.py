import pygame as pg

import sys, os

from scene import Scene
from tools import *
from folders import *
from config import *

from the_quest.game.game_scenes import StartingGame



class InitialAnimation(Scene):

    def __init__(self):
        Scene.__init__(self)

        self.ship_img = load_image(SHIP_FOLDER, 'ship.xcf')

        self.x_pos_ship = 800
        self.y_pos_ship = 110
        self.x_pos_title = 848
        self.y_pos_title = 75

    def handle_events(self, screen):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.terminateScene()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.terminateScene()

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

    def handle_events(self, screen):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.terminateScene()
            if event.type == pg.KEYDOWN:
                self._keydown_events(event, screen)

    def _keydown_events(self, event, screen):
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
        if event.key == pg.K_ESCAPE:
            pg.quit()
            sys.exit()

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
        self.bg_img = load_image(IMAGES_FOLDER, 'background.xcf', rect=False)

    def handle_events(self, screen):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.terminateScene()
            if event.type == pg.KEYDOWN:
                self._keydown_events(event, screen)

    def _keydown_events(self, event, screen):
        if event.key == pg.K_ESCAPE:
            self.terminateScene()

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

    def __init__(self):
        Scene.__init__(self)

    def handle_events(self, screen):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.terminateScene()
            if event.type == pg.KEYDOWN:
                self._keydown_events(event, screen)

    def _keydown_events(self, event, screen):
        if event.key == pg.K_ESCAPE:
            self.switchToScene(TitleScene())

    def update(self, screen, dt):
        screen.fill(BLUE)
        create_draw_text(screen, SPACE2, 54, 'INSTRUCCTIONS', WHITE, position='topcenter', width=WIDTH, height=HEIGHT)

        pg.display.update()