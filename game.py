
import time
import pygame

from cake.gameobject import GameObject
from cake.input import EventHandler
from player import Player
from enemy import Enemy


class Game:
    """
        Generic class that handles game setup,
        and game loop as well as in game eventhandlers
    """
    def __init__(self):
        events = EventHandler()
        events.assign_keyup(pygame.K_ESCAPE, self.pause)
        self.events = events
        
            
    def initialize(self, data):
        print("initializing...")
        game_data = {}
        data['game'] = game_data
        # put level info outside 'game_data' to allow for
        # level selection in future menus
        data['level'] = 1
        self.data = data
        self.game_data = game_data


    def run(self, data):
        if data['game'] is None:
            self.initialize(data)
            print("game started")
        else: 
            print("game resumed")
        game_data = self.game_data
        clock = pygame.time.Clock()
        screen = data['screen']

        # game loop
        while self.data['in_game']:
            clock.tick(1)
            screen.fill((148,148,148))
            self.events.handle_events()
            pygame.display.flip()



    def pause(self):
        self.data['in_game'] = False
        self.data['in_pause_menu'] = True
        self.data['in_start_menu'] = False
        print("game paused")
