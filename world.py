
from pygame.sprite import Group

from cake.gameobject import GameObject

class World(Group):

    """
        This class represents a level in a game
        and handles camera focus as well as collision
        between GameObjects
    """
    def __init__(self, width, height, screen_size):
        super(self, Group).__init__()
        self.collideables = []
        self.noncollideables = []
        self.enemies = []
        self.players = []
        
    def add_collideable(self, obj):
        """
            Add collideable object, object must be instance of
            GameObject
        """
        assert isinstance(GameObject, obj)

    def add_noncollideable(self, obj):
        pass

    def update(self, dt, surf): 
        pass
