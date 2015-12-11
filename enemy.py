import pygame
from cake.gameobject import GameObject

class Enemy(GameObject):

    def __init__(self, x, y, world):
        image = pygame.Surface((50, 50))
        image.fill((128,0,0))
        super(Enemy, self).__init__(image)
        self.set_position(x, y)
        self.world = world
