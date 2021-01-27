import pygame as pg

import sys, os

from scene import Scene
from tools import *
from folders import *
from config import *

from the_quest.sprites import *
from the_quest.optional_screens import *

class InitialAnimation(Scene):

    def __init__(self):
        Scene.__init__(self)

        self.ship_img = load_image(SHIP_FOLDER, 'ship.xcf')

        self.x_pos_ship = 800
        self.y_pos_ship = 110
        self.x_pos_title = 848
        self.y_pos_title = 75

    def _keydown_events(self, event, screen):
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
        self.bg_img = load_image(IMAGES_FOLDER, 'background.xcf', rect=False)

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

    def _keydown_events(self, event, screen):
        if event.key == pg.K_ESCAPE:
            self.switchToScene(TitleScene())

    def update(self, screen, dt):
        screen.fill(BLUE)
        create_draw_text(screen, SPACE2, 54, 'INSTRUCCTIONS', WHITE, position='topcenter', width=WIDTH, height=HEIGHT)

        pg.display.update()

class StartingGame(Scene):

    def __init__(self):
        Scene.__init__(self)
        self.ship_img, self.ship_rect = load_image(SHIP_FOLDER, 'ship.xcf')
        self.ix_pos = -50
        self.ticks = 0

    def _keydown_events(self, event, screen):
        if event.key == pg.K_SPACE and self.ix_pos == 0:
            self.switchToScene(Level1())

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

class Level1(Scene):

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
        self.level = 1

        self.bonus_score = 0

    def _keydown_events(self, event, screen):
        if event.key == pg.K_SPACE: 
            # Click for rotate ship
            if self.ship.state == STATES['ALIVE']\
                and self.meteors_dodged >= METEORS_TO_DODGE\
                and self.planet_x == 272 and self.ship.rect.top >= 200\
                and self.ship.rect.top <= 300:
                self.ship.state = STATES['ROTATING']
            # Click for land
            if self.ship.state == STATES['PREPARED TO LAND']\
                and self.ship.rect.top >= 200:
                self.ship.state = STATES['LANDING']
            # Click for finish level
            if self.ship.state == STATES['HIDDEN']:
                # Level Finished
                self._end_update_score()
                self.ship._restart_ship()
                self.bg_sound.stop()
                self.switchToScene(Level2(self.score, self.ship)) # <- Scene Next Level
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
            self.black_screen.on_black(screen, self.level, self.ship.lifes)
            self._reset()
            self.bg_sound.play()

        if self.ship.state == STATES['DEAD']:
            self.switchToScene(GameOver())

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
                self._landing_msg(screen)

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

    def _landing_msg(self, screen):
        if self.ship.rect.top >= 260 and self.ship.rect.top <= 280:
            pos_land_msg = 'PERFECT'
            if not self.bonus_score:    
                self.bonus_score += 1000
        elif self.ship.rect.top >= 240 and self.ship.rect.top <= 280:
            pos_land_msg = 'SUCCESFULLY'
            if not self.bonus_score:
                self.bonus_score += 500
        else:
            pos_land_msg = 'NOT BAD'
            if not self.bonus_score:
                self.bonus_score += 250
        create_draw_text(screen, SPACE, 26, f'{pos_land_msg} LANDED!', WHITE, position='topcenter', width=WIDTH)

    def _end_update_score(self):
        self._add_bonus_to_score()
        self.score += self.bonus_score

    def _add_bonus_to_score(self):
        if self.ship.lifes == 3:
            self.bonus_score += 1000
        elif self.ship.lifes == 2:
            self.bonus_score += 500
        else:
            self.bonus_score += 250

class Level2(Scene):

    def __init__(self, score, ship):
        Scene.__init__(self)
        self.bg_sound = load_sound(SOUNDS_FOLDER, 'background_sound.ogg')
        self.bg_sound.set_volume(BACKGROUND_VOL)
        self.bg_sound.play()

        # Background img
        self.background = load_image(IMAGES_FOLDER, 'background.xcf', rect=False)
        self.background_x = 0 # For moving_background

        self.meteors_timer = 0 # For adding meteors

        self.meteors = pg.sprite.Group()
        self.ship = ship
        self.remaining_lifes = self.ship.lifes
        self.ship.state = STATES['ALIVE']
        self.ship.rect.x = 2
        self.ship.image = load_image(SHIP_FOLDER, 'ship.xcf', rect=False)
        self.black_screen = BlackScreen()
        self.pause_screen = PauseScreen()

        self.planet, self.rect_planet = load_image(IMAGES_FOLDER, 'marte.png', x=WIDTH, y=50)
        self.planet_x = 0 # For moving planet

        self.ticks = 0

        # Vars top level
        self.score = score
        self.meteors_dodged = 30
        self.level = 2

        self.bonus_score = 0

    def _keydown_events(self, event, screen):
        if event.key == pg.K_SPACE: 
            # Click for rotate ship
            if self.ship.state == STATES['ALIVE']\
                and self.meteors_dodged >= METEORS_TO_DODGE\
                and self.planet_x == 272 and self.ship.rect.top >= 200\
                and self.ship.rect.top <= 300:
                self.ship.state = STATES['ROTATING']
            # Click for land
            if self.ship.state == STATES['PREPARED TO LAND']\
                and self.ship.rect.top >= 200:
                self.ship.state = STATES['LANDING']
            # Click for finish level
            if self.ship.state == STATES['HIDDEN']:
                # Level Finished
                self._end_update_score()
                self.switchToScene(None) # <- Scene Records
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
            self.black_screen.on_black(screen, self.level, self.ship.lifes)
            self._reset()
            self.bg_sound.play()

        if self.ship.state == STATES['DEAD']:
            self.switchToScene(GameOver())

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
                self._landing_msg(screen)

            if self.ship.state == STATES['HIDDEN']:
                
                create_draw_text(screen, SPACE2, 54, 'MARS CONQUERED!', WHITE, position='center', width=WIDTH, height=HEIGHT)

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
            self.ship.lifes = self.remaining_lifes

    def _landing_msg(self, screen):
        if self.ship.rect.top >= 260 and self.ship.rect.top <= 280:
            pos_land_msg = 'PERFECT'
            if not self.bonus_score:    
                self.bonus_score += 1000
        elif self.ship.rect.top >= 240 and self.ship.rect.top <= 280:
            pos_land_msg = 'SUCCESFULLY'
            if not self.bonus_score:
                self.bonus_score += 500
        else:
            pos_land_msg = 'NOT BAD'
            if not self.bonus_score:
                self.bonus_score += 250
        create_draw_text(screen, SPACE, 26, f'{pos_land_msg} LANDED!', WHITE, position='topcenter', width=WIDTH)

    def _end_update_score(self):
        self._add_bonus_to_score()
        self.score += self.bonus_score

    def _add_bonus_to_score(self):
        if self.ship.lifes == 3:
            self.bonus_score += 1000
        elif self.ship.lifes == 2:
            self.bonus_score += 500
        else:
            self.bonus_score += 250

class GameOver(Scene):

    def __init__(self):
        Scene.__init__(self)

        self.ticks = 0

    def _keydown_events(self, event, screen):
        if event.key == pg.K_SPACE:
            self.switchToScene(TitleScene())
        if event.key == pg.K_ESCAPE:
            self.terminateScene()

    def update(self, screen, dt):
        screen.fill(BLACK)
        self.ticks += dt
        create_draw_text(screen, SPACE2, 64, 'GAME OVER', WHITE, position='center', width=WIDTH, height=HEIGHT)
        if self.ticks <= 500:
            create_draw_text(screen, SPACE, 16, 'Press < SPACE > to start', WHITE, position='bottomcenter', width=WIDTH, height=HEIGHT)
        elif self.ticks <= 1000:
            pass
        else:
            self.ticks = 0

        pg.display.flip()
