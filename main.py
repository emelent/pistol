
import pygame 

from menus import *
from game import Game 
from cake.input import EventHandler


def prepare():
    pygame.init()
    data = {}
    data['SCREEN_SIZE'] = 480, 360
    data['screen'] = pygame.display.set_mode(data['SCREEN_SIZE'])
    data['in_game'] = False
    data['in_start_menu'] = True
    data['in_pause_menu'] = False
    data['game'] = None
    return data


def main():
    data = prepare()
    game = Game()

    while data['in_start_menu'] or data['in_game'] or data['in_pause_menu']:
        if data['in_start_menu']:
            start_menu(data)

        elif data['in_game']:
            game.run(data)

        elif data['in_pause_menu']:
            pause_menu(data)

    pygame.quit()


if __name__ == '__main__':
    main()
    
