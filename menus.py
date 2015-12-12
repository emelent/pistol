import pygame 

from ui import ButtonGroup
from menu_utils import *
from cake.input import EventHandler


def start_menu(data):		
    
    events = EventHandler()
    btnGroup = create_btnGroup()
    def start_game():
        data['in_start_menu'] = False    
        data['in_game'] = True
        data['in_pause_menu'] = False

    def quit():
        data['in_start_menu'] = False    
        data['in_game'] = False    
        data['in_pause_menu'] = False
        print("Quitting...")

    btnGroup.add_button('start', start_game)
    btnGroup.add_button('quit', quit)
    events.assign_mouseup(1, btnGroup.event_callback)
    events.assign_keyup(pygame.K_q, quit)
    menu_loop(data, btnGroup, events, 'in_start_menu')
    print("leaving main menu..")


def pause_menu(data):		
    events = EventHandler()
    btnGroup = create_btnGroup()

    def resume_game():
        data['in_start_menu'] = False    
        data['in_game'] = True
        data['in_pause_menu'] = False

    def new_game():
        data['game'] = None
        resume_game()

    def quit():
        data['in_start_menu'] = False    
        data['in_game'] = False    
        data['in_pause_menu'] = False

    def go_to_main():
        data['game'] = None
        data['in_start_menu'] = True
        data['in_game'] = False    
        data['in_pause_menu'] = False

    btnGroup.add_button('resume', resume_game)
    btnGroup.add_button('new game', new_game)
    btnGroup.add_button('quit to menu', go_to_main)
    btnGroup.add_button('quit to desktop', quit)

    events.assign_mouseup(1, btnGroup.event_callback)
    events.assign_keyup(pygame.K_ESCAPE, resume_game)
    events.assign_keyup(pygame.K_q, quit)

    menu_loop(data, btnGroup, events, 'in_pause_menu')
    print("leaving pause menu..")
