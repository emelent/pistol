
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

    def update(self, dt):
        
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            if self.is_move_valid(x=-self.speed):
                self.position.x -= self.speed
            else:
                print("left invalid")
        if keystate[pygame.K_RIGHT]:
            if self.is_move_valid(x=self.speed):
                self.position.x += self.speed
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
