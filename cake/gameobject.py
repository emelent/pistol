from .vec2d import Vec2d
from .ssprite import SSprite
import pygame


class GameObject(pygame.sprite.Sprite):
    """
        Generic object should be used whenever an interacteable or mobile object is needed.
        This should be used as a base class, and should collision be needed, the 
        collide() method should be overrided accordingly in child classes.


        @self.image         = pygame.Surface image used to represent GameObject graphically

        @self.rect          = pygame.rect of image, used for positioning

        @self._velocity     = Vec2d object representing velocity of GameObject

        @self._position     = Vec2d object representing position of GameObject

        @self._gravity      = Vec2d object representing gravity affecting the GameObject

        @self._airborne     = boolean value that determines whether or not self.__gravity__()
                              function should run

        @self._airtime      = float contains the duration of time the GameObject has been
                              airborne for. Used when calculating gravity
        
      
    """

    def __init__(self, image):
        super(GameObject, self).__init__()
        # if image != None:
        self.image = image
        self.rect = image.get_rect()
        self._velocity = Vec2d(0, 0)
        self._position = Vec2d(0, 0)
        self._airborne = False
        self._airtime = 0
        self._gravity = Vec2d(0, 0.8)

    def __gravity__(self, dt):
        """Apply gravity to object"""
        t = dt - self._airtime
        self._velocity += self._gravity * t

    def collide(self, other, extra=None):
        """
            Method to call when GameObject collides with another GameObject.
            This does not check for collision. This method should be used to 
            determine how the object responds to a collision with another
            GameObject.
            
            @other      = GameObject that the current object collided with
            @extra      = Extra info about collision at the time of collision
                          which may be changed. 
                            e.g     
                            Obj1 collides with Obj2.
                            Obj1's collide() is called before Obj2
                                Obj1 then change's it's velocity based on Obj2's
                                velocity
                            When Obj2's collide() is called, Obj1's velocity is no
                            longer what it was at the time of the collision.
                            Hence we place velocity and other volatile collision
                            information in extra, so it is preserved regardlessly. :)

        """
        pass

    def __move__(self): 
        """Called by update method to change object's position using object's velocity"""
        v = self._velocity
        p = self._position
        p += v
        self.rect.x = round(p.x)
        self.rect.y = round(p.y)

    def set_gravity(self, x, y):
        """Set GameObject gravity"""
        self._gravity.x = x
        self._gravity.y = y

    def toggle_airborne(self, b=None):
        """toggle self._airborne, if true, gravity will be active"""
        self._airborne = b if b != None else not self._airborne
        if not self._airborne:
            self._airtime = 0

    def set_velocity(self, x, y):
        """Set object's velocity"""
        self._velocity.x = x
        self._velocity.y = y

    def set_position(self, x, y):
        """Set the position of the object"""
        self._position.x = x
        self._position.y = y
        self.rect.topleft = x, y

    def get_position(self):
        """Get the position of the object"""
        return tuple(self._position)

    def update(self, dt, surf):
        if self._airborne:
            if self._airtime == 0:
                self._airtime = dt
            self.__gravity__(dt)
        self.__move__() 
        surf.blit(self.image, self.rect) 

class AnimGameObject(GameObject, SSprite):
    """
        Like a GameObject except uses SSprite class to leverage it's 
        animation capabilities. Allows for creating mobile and animated
        objects that may or may not be interactable
    """
    def __init__(self, default_frames, **kwargs):
        SSprite.__init__(self, default_frames, **kwargs)
        self._velocity = Vec2d(0, 0)
        self._position = Vec2d(0, 0)
        self._airtime = 0
        self._airborne = False

    def update(self, dt, surf):
        if self._airborne:
            if self._airtime == 0:
                self._airtime = dt
            self.__gravity__(dt)
        self.__move__()
        SSprite.update(self, dt, surf)

