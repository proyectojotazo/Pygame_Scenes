import pygame as pg

import sys

from config import WIDTH, HEIGHT, FPS

from the_quest.scenes import InitialAnimation


pg.init()

class Screen:

    def __init__(self, starting_scene):
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption('The quest')

        self.active_scene = starting_scene

        self.clock = pg.time.Clock()

    def start_game(self):
        while self.active_scene != None:
            dt = self.clock.tick(FPS)
            self.active_scene.main_loop(self.screen, dt)
            self.active_scene = self.active_scene.next

if __name__ == '__main__':
    a = Screen(InitialAnimation())
    a.start_game()