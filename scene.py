import pygame as pg

from tools import *
from folders import *
from config import *

class Scene:

    def __init__(self):
        self.next = self

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
        pass

    def update(self, screen, dt):
        pass

    def switchToScene(self, next_scene):
        self.next = next_scene

    def terminateScene(self):
        self.switchToScene(None)