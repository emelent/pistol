import pygame, time
from pygame.sprite import Sprite
from .strip import *


class SSprite(Sprite):
    """
        SSprite(StripSprite) that makes use of the strip.Strip class in order to handle
        multi frame sprite animations and frame timing.
        Each animation is represented by a Strip, which contains a list of images frames
        as well as timing properties for each of those frames and the order in which
        this list must be traversed.

        @self._strips       = dict, stores lists of frames with the name of list as key.
                                
        @self._chain        = list, list of strip names to chain together seamlessly.
                              though "chaining" feature might be removed in later revisions

        @self._current_strip= str, name of current strip   
    """

    def __init__(self, default_frames, frame_order=STRIP_FORWARD, strip_timing=0.2, default_strip=None):
        super(SSprite, self).__init__()
        self._strips = {}
        if default_strip == None:
            if isinstance(default_frames, pygame.Surface):
                self.add_strip('default', frames=[default_frames], \
                               frame_order=frame_order, repeat=-1, \
                               strip_timing=strip_timing)
            else:  # pass it on to Strip
                self.add_strip('default', frames=default_frames, \
                               frame_order=frame_order, repeat=-1, \
                               strip_timing=strip_timing)
        else:
            assert isinstance(default_strip, Strip)
            self._strips['default'] = default_strip
        self._current_strip = 'default'
        self.image = self._strips['default'].next(0)
        self.rect = self.image.get_rect()
        self._chain = []

    def add_strip(self, name, frames, frame_order=STRIP_FORWARD, repeat=0,
                  strip_timing=0):
        """add an animation strip to sprite"""
        assert isinstance(frames, list), \
            'Expected list type'
        assert isinstance(frames[0], pygame.Surface), \
            'Expected list of pygame.Surface objects'
        s = Strip(frames, frame_order=frame_order, \
                  repeat=repeat, strip_timing=strip_timing)
        self._strips[name] = s

    # #############################################################
    # ##	Scrap this if there is no need
    # #############################################################
    def add_to_chain(self, *strip_names):
        self._chain += strip_names

    def clear_chain(self):
        self._chain.clear()

    ##############################################################

    def update(self, dt, surf):
        _current = self._current_strip
        if _current != 'default' and \
                self._strips[_current].is_done():
            if len(self._chain) > 0:
                self.set_strips(self._chain[0])
                self._chain.remove(self._chain[0])
            else:
                self.set_strip('default')

        self.image = self._strips[_current].next(dt)
        surf.blit(self.image, self.rect)

    def set_strip(self, name):
        """set current animation strip"""
        self._current_strip = name
        self._strips[name].reset()

