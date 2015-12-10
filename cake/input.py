import pygame
from pygame.locals import *


class EventHandler():
    """Handles events received from mouse and keyboard, no joystick support yet"""
    key_up_callbacks = {}
    key_down_callbacks = {}
    mouse_down_callbacks = {}
    mouse_up_callbacks = {}
    mouse_move_callback = None
    mouse_events = [MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION]
    keyboard_events = [KEYDOWN, KEYUP]

    def assign_keyup(self, key, callback, *args, **kwargs):
        """assigns a callback to keyup event"""
        self.__validate_callback__(callback)
        self.key_up_callbacks[key] = (callback, args, kwargs)

    def assign_keydown(self, key, callback, *args, **kwargs):
        """assigns a callback to keydown event"""
        self.__validate_callback__(callback)
        self.key_down_callbacks[key] = (callback, args, kwargs)


    def assign_mousedown(self, button, callback, *args, **kwargs):
        """assigns a callback to mouse button down event"""
        self.__validate_callback__(callback)
        self.mouse_down_callbacks[button] = (callback, args, kwargs)

    def assign_mouseup(self, button, callback, *args, **kwargs):
        """assigns a callback to mouse button up event"""
        self.__validate_callback__(callback)
        self.mouse_up_callbacks[button] = (callback, args, kwargs)

    def assign_mousemove(self, callback, *args, **kwargs):
        self.__validate_callback__(callback)
        self.mouse_move_callback = (callback, args, kwargs)
        
    def handle_events(self):
        """calls necessary callbacks when events occur"""
        #e = pygame.event.poll()
        for e in pygame.event.get():
            if e.type == QUIT:
                self.quit()
                break
            # handle keyboard and mouse simultaneously
            if e.type in self.mouse_events:
                self.__mouse__(e)
            if e.type in self.keyboard_events:
                self.__keyboard__(e)

    def __mouse__(self, e):
        """handles all mouse events"""
        mouse_down = self.mouse_down_callbacks
        mouse_up = self.mouse_up_callbacks
        if e.type == MOUSEBUTTONDOWN:
            if e.button in mouse_down:
                f, args, kwargs = mouse_down[e.button]
                f(*args, **kwargs)
        elif e.type == MOUSEBUTTONUP:
            if e.button in mouse_up:
                f, args, kwargs = mouse_up[e.button]
                f(*args, **kwargs)
        elif e.type == MOUSEMOTION and self.mouse_move_callback:
            f, args, kwargs = self.mouse_move_callback
            f(*args, **kwargs)

    def __keyboard__(self, e):
        """handles all keyboard events"""
        key_up = self.key_up_callbacks
        key_down = self.key_down_callbacks
        if e.type == KEYDOWN:
            if e.key in key_down:
                f, args, kwargs = key_down[e.key]
                f(*args, **kwargs)
        elif e.type == KEYUP:
            if e.key in key_up:
                f, args, kwargs = key_up[e.key]
                f(*args, **kwargs)

    def __validate_callback__(self, callback):
        assert callable(callback), \
            'callback must be a callable value'

    def quit(self):
        """quit pygame and terminate program"""
        print("Quitting...")
        pygame.quit()
        exit(0)

