
import time
import pygame

from cake.gameobject import GameObject
from cake.input import EventHandler
from world import World
from player import Player
from enemy import Enemy


class Game:
    """
        Generic class that handles game setup,
        and game loop as well as in game eventhandlers
    """
    def __init__(self, fps=50):
        events = EventHandler()
        events.assign_keyup(pygame.K_p, self.pause)
        events.assign_keyup(pygame.K_q, self.quit)
        events.assign_keyup(pygame.K_f, self.toggle_focus)
        events.assign_keyup(pygame.K_s, self.toggle_shake)
        self.events = events
        self.fps = fps
        self.focused = False
        
    def toggle_shake(self):
        w = self.data['game']['world']
        w.toggle_shake()
        print("Shake: %s" % w.shake)

    def toggle_focus(self):
        w = self.data['game']['world']
        p = self.data['game']['player']
        if self.focused:
            w.remove_focus()
        else:
            w.set_focus(p)
        self.focused = not self.focused
            

    def initialize(self, data):
        print("initializing...")
        # put level info outside 'game_data' to allow for level selection in future menus
        data['level'] = 1
        w = World(data['SCREEN_SIZE'][0]*2, data['SCREEN_SIZE'][1], data['SCREEN_SIZE'], bg_color=(0, 255, 255)) 
        p = Player(100, 300, w)
        e = Enemy(10, 300, w)
        e2 = Enemy(300, 300, w)
        w.add_player(p) 
        w.add_enemy(e)
        w.add_enemy(e2)
        # w.set_focus(p)
        game= {}
        game['particles'] = pygame.sprite.Group()
        game['spawners'] = pygame.sprite.Group()
        game['world'] = w
        game['player'] = p
        data['game'] = game
        self.data = data

    def run(self, data):
        if data['game'] is None:
            self.initialize(data)
            print("game started")
        else: 
            print("game resumed")
        game= data['game']
        clock = pygame.time.Clock()
        screen = data['screen']
        fps = self.fps
        events = self.events
        t1 = time.time()
        particles = game['particles']
        spawners = game['spawners']
        world = game['world']

        # game loop
        while self.data['in_game']:
            clock.tick(fps)
            screen.fill((148,148,148))
            events.handle_events()

            t2 = time.time()
            dt = t2 - t1

            world.update(dt, screen)
            particles.update(dt, screen)
            spawners.update(t2)
            pygame.display.flip()



    def pause(self):
        self.data['in_game'] = False
        self.data['in_pause_menu'] = True
        self.data['in_start_menu'] = False
        print("game paused")

    def quit(self):
        self.data['in_game'] = False
        self.data['in_pause_menu'] = False
        self.data['in_start_menu'] = False
        print("game quit")
        
