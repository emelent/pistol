import pygame
from cake.gameobject import GameObject

class World:

    """
        This class represents a level in a game
        and handles camera focus as well as collision
        between GameObjects
    """
    def __init__(self, width, height, screen_size, bg=None):
        super(World, self).__init__()
        self.screen_size = screen_size
        self.background = bg
        self.width = width
        self.height = height
        self.collideables = set()
        self.noncollideables = set()
        self.items = set()
        self.enemies = set()
        self.players = set()
        self.all_objects = set()
        self.focus = None
        self.hz_focus = False
        self.vt_focus = False
        
    def __add_to_all__(self, obj):
        """
            Performs necessary checks and then adds obj to 
            self.all_objects container.

            This should not be called directly, called indirectly
            by other add_* methods. 
        """
        assert isinstance(GameObject, obj)
        self.all_objects.add(obj)

    def add_collideable(self, obj):
        """
            Add object player/enemies can collide with, object 
            must be instance of GameObject
        """
        self.__add_to_all__(obj)
        self.collideables.add(obj)

    def add_background_object(self, obj):
        """
            Add non-collideable object drawn onto background
        """
        self.__add_to_all__(obj)
        self.noncollideables.add(obj)

    def add_item(self, obj):
        """
            Add object that can be interacted with by 
            player/enemy.

        """
        self.__add_to_all__(obj)
        self.items.add(obj)
        

    def add_player(self, obj):
        """
            Add player to world.
        """
        self.__add_to_all__(obj)
        self.players.add(obj)

    def add_enemy(self, obj):
        """
            Add enemy to world
        """
        self.__add_to_all__(obj)
        self.enemies.add(obj)
        
    def set_focus(self, rect, horz=True, vert=False):
        """
            Set camera focus to obj.
            Object must be previously added to World
            using on of the add_* methods.

            @horz       = boolean, focus horizontally (appears centered x)
            @vert       = boolean, focus vertically (appears centered y)
        """
        if horz or vert:
            self.focus = rect
            self.hz_focus = horz
            self.vt_focus = vert


    def __handle_collisions__(self):
        """
            Handle permitted collisions, such
            as those between player and items/enemies
            and between enemies and items.
            
            Non-permitted collisions such as 
            player and collideables or enemies and 
            collideables will be handle by player
            and enemy classes respectively.

            This is to minimize collision checks,
            for instance, if the player was not colliding with 
            a wall before they moved and the player still hasn't 
            moved, then there is no need to check if the player 
            has collided with the wall again. "Look-ahead" 
            collision should be implemented in the classes of the
            moving game objects, and checked only before the object
            moves for this very purpose.
        """

        # player collisions
        for p in players:
            spr = pygame.sprite.spritecollide(p, self.items)
            for s in sprs:
                p.collide(s)

            enemies = pygame.sprite.spritecollide(p, self.enemies)
            for e in enemies:
                p.collide(e)

        # enemy collisions
        for e in enemies:
            sprs = pygame.sprite.spritecollide(p, self.items)
            for s in sprs:
                p.collide(s)

    def __blit_spr__(self, spr, surf):
        """
            Blit a sprite to the screen surface
            with consideration to the world's
            focus object
        """
        frect = self.focus
        pos = spr.get_position()
        if focus: 
            if self.hz_focus:
                fx = self.screen_size[0]//2 - frect.width //2
                dx = pos[0] - frect.x 
                pos[0] = fx - dx
            if self.vt_focus:
                fy = self.screen_size[1]//2 - frect.height//2
                dy = pos[1] - frect.y 
                pos[1] = fy - dy
        surf.blit(spr.image, pos)

    def update(self, dt, surf): 
        """
            Update, and everything to screen in correct order
            bg, noncollideables, collideables, enemies, player, items
            and according to the correct focus
        """
        self.handle_collisions()
        bg = self.background
        # background is not one that moves, just an image to
        # set theme, motion will be shown by non-collideables
        # shifting according the motion of the focus(normally player)
        if bg:
           surf.blit(bg, [0,0])
        for spr in self.all_objects:
            spr.update(dt)

        for spr in self.noncollideables:
            self.__blit_spr__(spr, surf)
        for spr in self.collideables:
            self.__blit_spr__(spr, surf)
        for spr in self.enemies:
            self.__blit_spr__(spr, surf)
        for spr in self.players:
            self.__blit_spr__(spr, surf)
        for spr in self.items:
            self.__blit_spr__(spr, surf)



