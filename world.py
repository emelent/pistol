import pygame
import random

from cake.gameobject import GameObject

# used for shaking the world
SHAKE_PADDING = 5

class World:

    """
        This class represents a level in a game
        and handles camera focus, permitted collision
        between GameObjects and also the blitting
        of GameObjects to screen
    """
    def __init__(self, width, height, screen_size, bg=None, bg_color=None):
        super(World, self).__init__()
        self.screen_size = screen_size
        self.background = bg if bg != None else pygame.Surface((width+SHAKE_PADDING, height + SHAKE_PADDING))
        self.background_color = bg_color
        if bg_color:
            self.background.fill(bg_color)
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0
        self.collideables = set()
        self.noncollideables = set()
        self.items = set()
        self.enemies = set()
        self.players = set()
        self.all_objects = set()
        self.focus = None
        self.hz_focus = False
        self.vt_focus = False
        self.focus_offsetx = 0
        self.focus_offsety = 0
        self.shake = False
        
    def __add_to_all__(self, obj):
        """
            Performs necessary checks and then adds obj to 
            self.all_objects container.

            This should not be called directly, called indirectly
            by other add_* methods. 
        """
        assert isinstance(obj, GameObject)
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
        
    def collides_with_collideable(self, rect):
        spr = pygame.sprite.Sprite()
        spr.rect = rect
        sprs = pygame.sprite.spritecollide(spr, self.collideables, False)
        
        return len(sprs) > 0 

    def collides_with_wall(self, rect):
        return rect.left < 0 or rect.right > self.width

    def is_move_valid(self, rect):
        return not(self.collides_with_wall(rect) or self.collides_with_collideable(rect))

    def set_focus(self, obj, horz=True, vert=False, offsetx=0, offsety=0):
        """
            Set camera focus to on object or rect.
            If object is given, object must have rect property.

            @horz       = boolean, focus horizontally (appears centered x)
            @vert       = boolean, focus vertically (appears centered y)
        """
        if horz or vert:
            if isinstance(obj, pygame.Rect):
                self.focus = obj
            elif isinstance(obj, GameObject):
                self.focus = obj.rect
            self.hz_focus = horz
            self.vt_focus = vert
            self.focus_offsetx = offsetx
            self.focus_offsety = offsety

    def remove_focus(self):
        self.focus = None

    def toggle_shake(self, b=None):
        """
            Toggle screen shaking
        """
        self.shake = b if b != None else not self.shake

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
        for p in self.players:
            sprs = pygame.sprite.spritecollide(p, self.items, False)
            for s in sprs:
                p.collide(s)

            enemies = pygame.sprite.spritecollide(p, self.enemies, False)
            for e in enemies:
                p.collide(e)

        # enemy collisions
        for e in self.enemies:
            sprs = pygame.sprite.spritecollide(p, self.items, False)
            for s in sprs:
                p.collide(s)

    def __blit_spr__(self, spr, surf):
        """
            Blit a sprite to the screen surface
            with consideration to the world's
            focus. If there is a focus, everything
            will be blitted in relation to the focus
            rect
        """
        frect = self.focus
        pos = spr.get_position()
        if frect: 
            if self.hz_focus:
                fx = self.screen_size[0]//2 - frect.width //2
                dx = frect.x - pos[0]
                pos[0] = fx - dx + self.focus_offsetx
            if self.vt_focus:
                fy = self.screen_size[1]//2 - frect.height//2
                dy = frect.y - pos[1]
                pos[1] = fy - dy + self.focus_offsety
        else:
            pos[0] += self.focus_offsetx
            pos[1] += self.focus_offsety
        surf.blit(spr.image, pos)

    def __shake__(self):
        n = SHAKE_PADDING//2
        self.x = random.randint(-n, n)
        self.y = random.randint(-n, n)

    def update(self, dt, surf): 
        """
            Update, and everything to screen in correct order
            bg, noncollideables, collideables, enemies, player, items
            and according to the correct focus
        """
        self.__handle_collisions__()
        if self.shake:
            self.__shake__()
        bg = self.background
        if self.background_color:
            bg.fill(self.background_color)
        # if bg:
        for spr in self.all_objects:
            spr.update(dt)

        for spr in self.noncollideables:
            self.__blit_spr__(spr, bg)
        for spr in self.collideables:
            self.__blit_spr__(spr, bg)
        for spr in self.enemies:
            self.__blit_spr__(spr, bg)
        for spr in self.players:
            self.__blit_spr__(spr, bg)
        for spr in self.items:
            self.__blit_spr__(spr, bg)
        surf.blit(bg, [self.x, self.y])

