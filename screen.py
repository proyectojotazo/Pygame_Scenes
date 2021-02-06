import pygame as pg

import sys

from config import WIDTH, HEIGHT, FPS, GAME_TITLE

from the_quest.scenes import InitialAnimation

class Screen:

    def __init__(self):
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(GAME_TITLE)

        self.active_scene = InitialAnimation()

        self.clock = pg.time.Clock()

    def start_game(self):
        while self.active_scene != None:
            dt = self.clock.tick(FPS)
            self.active_scene.main_loop(self.screen, dt)
            self.active_scene = self.active_scene.next

if __name__ == '__main__':
    pg.init()
    a = Screen()
    a.start_game()