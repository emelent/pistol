
import pygame
from cake.gameobject import GameObject

class Player(GameObject):

    def __init__(self, x, y, world):
        image = pygame.Surface((50, 50))
        image.fill((0,0,128))
        super(Player, self).__init__(image)
        self.speed = 5
        self.world = world
        self.set_position(x, y)
        self.set_gravity(0, 6)
        self.groundy = 0
        self.auto_focus = True

    def collide(self, other, extra=None):
        pass

    def is_move_valid(self, x=0, y=0):
        """
            "Look Ahead" collision detection

            More accurate to use one argument at
            a time, e.g. is_move_valid(x=-5)
            To check collision in a single direction
            so you know which motion leads to a collision
        """
        rect = self.rect.copy()
        rect.x += round(x) 
        rect.y += round(y) 
        
        return self.world.is_move_valid(rect)

    def __auto_focus__(self):
        """
            Automatically focus the camera on
            player appropriately. 
            Automatically called after player moves
        """
        if not self.auto_focus:
            self.world.focus = None
            return
        w = self.world
        scr_w, scr_h = w.screen_size
        wrld_w, wrld_h = w.width, w.height
        if self.position.x < scr_w//2:
            w.remove_focus()
        elif self.position.x >= wrld_w - scr_w//2:
            w.set_focus(self.rect.copy())
        else:
            w.set_focus(self)



    def update(self, dt):
        
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            if self.is_move_valid(x=-self.speed):
                self.position.x -= self.speed
                self.__auto_focus__()
            else:
                print("left invalid")
        if keystate[pygame.K_RIGHT]:
            if self.is_move_valid(x=self.speed):
                self.position.x += self.speed
                self.__auto_focus__()
            else:
                print("right invalid")
        if keystate[pygame.K_UP]:
            self.jump()
         
        if self.airborne and self.position.y > self.groundy:
            self.position.y = self.groundy
            self.toggle_airborne(False)
            self.set_velocityy(0)
        super(Player, self).update(dt)

    def jump(self):
        if not self.airborne:
            self.groundy = self.position.y
            self.toggle_airborne(True)
            self.set_velocityy(-15)
