
import pygame 

import ui
from game import Game 
from cake.input import EventHandler


def prepare():
    pygame.init()
    data = {}
    data['SIZE'] = 480, 360
    data['screen'] = pygame.display.set_mode(data['SIZE'])
    data['in_game'] = False
    data['in_start_menu'] = True
    data['in_pause_menu'] = False
    data['game'] = None
    return data


def start_menu(data):		
    screen = data['screen']
    clock = pygame.time.Clock()
    events = EventHandler()
    btnGroup = ui.ButtonGroup((200, 200), btn_gap=10,btn_height=40, bg_color=(0,0,0))
    btnGroup.set_button_property('background_color', (0, 0, 0))
    btnGroup.set_button_property('border_color', (145, 0, 0) )
    btnGroup.set_button_property('highlight_color', (145,0,0))

    def start_game():
        data['in_start_menu'] = False    
        data['in_game'] = True
        data['in_pause_menu'] = False

    def quit():
        data['in_start_menu'] = False    
        data['in_game'] = False    
        data['in_pause_menu'] = False

    btnGroup.add_button('start', start_game)
    btnGroup.add_button('quit', quit)
    btnGroup.center(screen.get_size())
    events.assign_mouseup(1, btnGroup.event_callback)

    while data['in_start_menu']:
        clock.tick(50)
        screen.fill((80,80,80))
        events.handle_events()

        mouse_pos = pygame.mouse.get_pos()
        btnGroup.update(mouse_pos, screen)
        pygame.display.flip()


def pause_menu(data):		
    screen = data['screen']
    clock = pygame.time.Clock()
    events = EventHandler()
    btnGroup = ui.ButtonGroup((200, 200), btn_gap=10,btn_height=40, bg_color=(0,0,0))
    btnGroup.set_button_property('background_color', (0, 0, 0))
    btnGroup.set_button_property('border_color', (145, 0, 0) )
    btnGroup.set_button_property('highlight_color', (145,0,0))

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
    btnGroup.center(screen.get_size())
    events.assign_mouseup(1, btnGroup.event_callback)

    while data['in_pause_menu']:
        clock.tick(50)
        screen.fill((80,80,80))
        events.handle_events()

        mouse_pos = pygame.mouse.get_pos()
        btnGroup.update(mouse_pos, screen)
        pygame.display.flip()

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
    
