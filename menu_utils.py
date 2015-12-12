
import pygame 

from ui import ButtonGroup

def create_btnGroup():
    """
        Just a function to create a ButtonGroup 
        with some predefined properties, which
        I'm gonna be using for all my menus
        so they look the same
    """
    btnGroup = ButtonGroup((200, 200), btn_gap=10,btn_height=40, bg_color=(0,0,0))
    btnGroup.set_button_property('background_color', (0, 0, 0))
    btnGroup.set_button_property('border_color', (145, 0, 0) )
    btnGroup.set_button_property('highlight_color', (145,0,0))
    return btnGroup

def menu_loop(data, btnGroup, eventhandler, sentinal):
    """
        Just grabbed all the generic stuff about 
        the menu functions and threw them all in 
        a nice function, just keeping DRY :)
    """
    screen = data['screen']
    btnGroup.center(screen.get_size())
    clock = pygame.time.Clock()
    while data[sentinal]:
        clock.tick(50)
        eventhandler.handle_events()
        screen.fill((80,80,80))
        mouse_pos = pygame.mouse.get_pos()
        btnGroup.update(mouse_pos, screen)
        pygame.display.flip()
