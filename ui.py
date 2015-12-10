import pygame

__doc__ = """This module contains some basic UI class, namely Button and ButtonGroup,
      nothing fancy"""

class UIObject(pygame.sprite.Sprite):
    """Base UI class"""
    def __init__(self):
        super(UIObject, self).__init__()

    def update(self, mouse_pos, surf):
        pass

class Button(UIObject):
    """
    This class creates a Button Object with onclick 
    callback that is called when button is clicked.

    e.g 
      btn = Button('hello_world')
  """
    default_color = 61, 73, 85

    def __init__(self, text, **kwargs):
        super(Button, self).__init__()
        self.text = text
        self.background_color = kwargs.get('background_color', Button.default_color)
        self._bg_color = self.background_color
        self.border_color = kwargs.get('border_color', (172, 190, 0))
        self.border_width = kwargs.get('border_width', 1)
        self.font_size = kwargs.get('font_size', 16)
        self.text_color = kwargs.get('text_color', (215, 165, 30))
        self.highlight_color = kwargs.get('highlight_color', (128, 128, 128))
        self.enabled = kwargs.get('Enabled', True)
        self.onclick = kwargs.get('callback', None)
        size = kwargs.get('size', (100, self.font_size))
        self.font = kwargs.get('font', pygame.font.Font(None, self.font_size))
        self.text = text
        self.text_data = None
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect()
        self.rect.topleft = kwargs.get('pos', (0, 0))
        self._hover = False
        self.__create_text_surf__()
        self.__render_text__()

    def __create_text_surf__(self):
        surf = self.font.render(self.text, 1, self.text_color)
        surf.set_colorkey((0, 0, 0))
        r = surf.get_rect()
        self.text_data = (surf, r)
        self.__center_text__()

    def __center_text__(self):
        r = self.text_data[1]
        r.centerx = self.rect.width // 2
        r.centery = self.rect.height // 2

    def __render_text__(self):
        """create the text and render it to button image"""
        txt_surf, txt_r = self.text_data
        img = self.image
        r = self.rect
        if txt_r.height > r.height:
            img = pygame.transform.scale(img, (r.width, int(txt_r.height * 1.3)))
            r = img.get_rect()
            self.image = img
            self.rect = r
            self.__center_text__()
        if txt_r.width > r.width:
            img = pygame.transform.scale(img, (int(txt_r.width * 1.3), r.height))
            self.image = img
            r = img.get_rect()
            self.rect = r
            self.__center_text__()

        # hack to allow "black" color, use rgb(1,1,1) since (0,0,0) is
        # color key
        colr = self.background_color
        if colr == (0, 0, 0):
            colr = 1, 1, 1
        img.fill(colr)
        img.blit(txt_surf, (txt_r.x, txt_r.y))

    def __mouse_over__(self):
        self._hover = True
        self.background_color = self.highlight_color
        self.__render_text__()

    def __mouse_out__(self):
        self._hover = False
        self.background_color = self._bg_color
        self.__render_text__()

    def click(self):
        """Simulates button clicks"""
        if self.onclick is not None:
            self.onclick()

    def is_mouse_over(self):
        """Returns True if mouse is hovering over Button"""
        return self._hover

    def set_property(self, prop, val):
        """
      Set Button property

        e.g
          btn = Button('click_me')
          btn.set_property('background_color', pygame.Color('green'))

    """
        if hasattr(self, prop):
            setattr(self, prop, val)
            self.__create_text_surf__()
            self.__render_text__()
        else:
            raise Exception('Button has no property named "%s"' % prop)

    def update_mouse_pos(self, mouse_pos):
        # print(mouse_pos)
        if self.enabled is False:
            self.__mouse_out__()
            return
        mouse_on_btn = self.rect.collidepoint(mouse_pos)
        if mouse_on_btn and not self._hover:
            self.__mouse_over__()
        elif not mouse_on_btn and self._hover:
            self.__mouse_out__()

    def update(self, mouse_pos, surf):
        """render image to surface"""
        self.update_mouse_pos(mouse_pos)
        surf.blit(self.image, self.rect)
        pygame.draw.rect(surf, self.border_color, self.rect, self.border_width)

    def event_callback(self):
        """If using nemoe.input.EventHandler then use this method as callback,
        e.g 
          import nemoe
          eventhandler = nemoe.input.EventHandler()
          eventhandler.assign_mouseup(button=1, callback=btn.event_callback())
    """
        if self.is_mouse_over() and self.enabled is True:
            self.click()


class ButtonGroup(UIObject):
    """Creates an object capable of grouping Button objects"""

    def __init__(self, size, **kwargs):
        super(ButtonGroup, self).__init__()
        self.buttons = []
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect()
        self.btn_height = kwargs.get("btn_height", 20)
        bg = kwargs.get("bg_color", None)
        if bg:
            self.image.fill(bg)
        self.rect.topleft = kwargs.get("position", (0,0))
        self.gap = kwargs.get("btn_gap", 10)
        self.image.set_colorkey((0, 0, 0))
        self.btn_props = {}
        self.btn_props['size'] = [self.rect.width, self.btn_height]
        self.enabled = True

    def __render__(self):
        image = self.image
        for item in self.buttons:
            image.blit(item.image, item.rect)

    def set_button_property(self, prop, val):
        """Sets a property of buttons to be created using the add_button(...) method, only applies to buttons created after property is set"""
        self.btn_props[prop] = val

    def add_created_button(self, btn):
        """Add a Button object to ButtonGroup"""
        buttons = self.buttons
        count = len(buttons)
        if count < 1:
            btn.rect.top = self.gap
        else:
            btn.rect.top = buttons[-1].rect.top + buttons[-1].rect.height + self.gap
        buttons.append(btn)
        self.__render__()

    def add_button(self, text, onclick=None):
        """Creates a button and adds it to the list of buttons stored by ButtonGroup"""
        b = Button(text, **self.btn_props)
        b.onclick = onclick
        b.rect.left = (self.rect.width - b.rect.width) // 2
        self.add_created_button(b)

    def center(self, size):
        """Centers the ButtonGroup according to the size of the surface containing it"""
        self.rect.centerx = size[0] // 2
        self.rect.centery = size[1] // 2

    def update(self, mouse_pos, surf):
        mouse_pos = list(mouse_pos)
        mouse_pos[0] -= self.rect.x
        mouse_pos[1] -= self.rect.y

        for item in self.buttons:
            item.update(mouse_pos, self.image)
        surf.blit(self.image, self.rect)
        # pygame.draw.rect(surf, (178, 90, 50), self.rect, 1)

    def event_callback(self):
        """If using nemoe.input.EventHandler then use this method as callback,
            to enable button callbacks
        e.g 
          btnGroup =  ButtonGroup((100, 200))
          eventhandler = nemoe.input.EventHandler()
          eventhandler.assign_mouseup(button=1, callback=btnGroup.event_callback())
    """
        if self.enabled == True:
            for btn in self.buttons:
                if btn.is_mouse_over():
                    btn.click()
                    break # only click the one button at a time
