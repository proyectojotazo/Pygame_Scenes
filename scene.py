import pygame as pg

from tools import *
from folders import *
from config import *

from the_quest.optional_screens import *
from the_quest.sprites import *

class Scene:

    def __init__(self):
        self.next = self
        self.ticks = 0

    def main_loop(self, screen, dt):
        self.handle_events(screen)
        self.update(screen, dt)
        
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
        pass

    def _blink_message(self, screen, font, size, text, color, position, width=WIDTH, height=HEIGHT, antialias=True):
        if self.ticks <= 1000:
            create_draw_text(screen, font, size, text, color, position=position, width=width, height=height, antialias=antialias)
        elif self.ticks <=1500:
            pass
        else:
            self.ticks = 0

    def switchToScene(self, next_scene):
        self.next = next_scene

    def terminateScene(self):
        self.switchToScene(None)

class LevelScene(Scene):

    def __init__(self, planet_name, level, go_scene):
        Scene.__init__(self)

        self.bg_sound = load_sound(SOUNDS_FOLDER, 'background_sound.ogg')
        self.bg_sound.set_volume(BACKGROUND_VOL)
        self.bg_sound.play()

        # Background img
        self.bg_img = load_image(IMAGES_FOLDER, 'background.png', rect=False)
        self.bg_x = 0 # For moving background

        self.meteors = pg.sprite.Group()
        self.ship = Ship()
        self.black_screen = BlackScreen()
        self.pause_screen = PauseScreen()
        self.go_scene = go_scene

        self.planet, self.rect_planet = load_image(IMAGES_FOLDER, f'{planet_name}.png', x=WIDTH, y=50)
        self.planet_x = 0 # For movement planet end level
        self.planet_name = planet_name

        self.ticks = 0

        self.score = 0
        self.meteors_dodged = 0
        self.level = level

        self.bonus_score = 0

    def _keydown_events(self, event, screen):
        Scene._keydown_events(self, event, screen)
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
    def update(self, screen, dt):

        self._add_meteors(dt)

        self._move_background(screen)
        self._top_level_menu(screen)
        self._draw_planet(screen, dt)
        screen.blit(self.ship.image, (self.ship.rect.x, self.ship.rect.y))
        self.meteors.draw(screen)
        self._end_level_msg(screen, dt)

        self._collition()
        
        self._update_sprites()

        self._remove_meteors()

        if self.ship.state == STATES['NOT ALIVE']:
            self.black_screen.on_black(screen, self.level, self.ship.lifes)
            self._reset()
            self.bg_sound.play()

        if self.ship.state == STATES['DEAD']:
            self.switchToScene(self.go_scene)

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
            self.ticks += dt
            if self.ticks >= 85:
                if len(self.meteors) <= MAX_METEORS:
                    self.meteors.add(Meteor())
                self.ticks = 0

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

    def _move_background(self, screen):
        x_rel = self.bg_x % WIDTH
        screen.blit(self.bg_img, (x_rel - WIDTH, 0))
        if x_rel < WIDTH:
            screen.blit(self.bg_img, (x_rel, 0))
        self.bg_x -= 1

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

    def _top_level_menu(self, screen):
        top_level_img, top_level_img_rect = load_image(IMAGES_FOLDER, 'score1.png')

        create_draw_text(screen, SPACE, 16, f'Lifes - {self.ship.lifes}', WHITE, pos_x=50, pos_y=15)
        create_draw_text(screen, SPACE, 16, f'Meteors Dodged - {self.meteors_dodged}', WHITE, pos_x=240, pos_y=15)
        create_draw_text(screen, SPACE, 16, f'Score - {self.score}', WHITE, pos_x=580, pos_y=15)
        
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
                
                create_draw_text(screen, SPACE2, 54, f'{self.planet_name} CONQUERED!', WHITE, position='center', width=WIDTH, height=HEIGHT)

                self.ticks += dt

                if self.ticks <= 500:
                    create_draw_text(screen, SPACE, 16, 'Press < SPACE > to continue', WHITE, position='bottomcenter', width=WIDTH, height=HEIGHT)
                elif self.ticks <= 1000:
                    pass
                else:
                    self.ticks = 0

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

    def _add_bonus_to_score(self):
        if self.ship.lifes == 3:
            self.bonus_score += 1000
        elif self.ship.lifes == 2:
            self.bonus_score += 500
        else:
            self.bonus_score += 250

    def _end_update_score(self):
        self._add_bonus_to_score()
        self.score += self.bonus_score

    def _reset(self):
        self.meteors.empty()
        self.ship.state = STATES['ALIVE']
        self.ship.rect.y = 276
        self.background_x = 0
        self.planet_x = 0
        self.meteors_dodged = 0
        self.ticks = 0

class AdvancedLevelScene(LevelScene):

    def __init__(self, planet_name, level, go_scene, score, lifes):
        LevelScene.__init__(self, planet_name, level, go_scene)

        self.last_score = score
        self.score += self.last_score
        self.remaining_lifes = lifes
        self.ship.lifes = self.remaining_lifes
    
    def _reset(self):
        LevelScene._reset(self)
        self.score = self.last_score
