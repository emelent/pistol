
"""
    This module contains classes used for
    simple and hopefully flexible particle simulations.
"""

import math, time, random
import pygame
from pygame import Color
from .vec2d import Vec2d


block = pygame.Surface((2,2))
explosion_block = pygame.Surface((4,4))


def init():
    imgs = [block.copy(), block.copy()]
    imgs[0].fill((221, 56, 47))
    imgs[1].fill(Color('orange'))
    w, h = imgs[0].get_size()
    explosion_block.blit(imgs[0], (0,0))
    explosion_block.blit(imgs[0], (w,h))
    explosion_block.blit(imgs[1], (w,0))
    explosion_block.blit(imgs[1], (0,h))

init()

# ##################################################
## CORE CLASSES
###################################################


class Particle(pygame.sprite.Sprite):
    """
        Simple class for creating particles
        with properties to simulate a few
        simple effects.

        It is best to use a ParticleSpawner object 
        when spawning multiple particles of the same nature
        and set particle properties using the 
        ParticleSpawner.set_particle_property method
        

        note:
            fixed_life is exact lifespan for particle,
                and overrides max_life.
            max_life is upperbound to random lifespan

        default keyword args:
            color=None, velocity=[0, -1], gravity=[0,0], size=4, max_life=2,
                fade=False, fixed_life=None, image=None, birth=None, pos=(0,0)


        @self._birth            = time that particle was spawned

        @self._velocity         = Vec2d object representing velocity of particle

        @self._gravity          = Vec2d object representing gravity on particle

        @self._fade             = boolean, determines whether the object should fade
                                  as it draws nearer to the end of it's lifespan

        @self._max_generations  = int, max number of generations the particle has should
                                  it reproduce

        @self._generation       = int, current generation of the particle

        @self._max_children     = int, max number of children particle can have should it
                                  reproduce

        @self._child_particle   = typename, type name of child particle which will be spawned
                                  should the particle reproduce 

        @self._age              = time, age of particle

        @self._orig_pos         = list, original position of particle 

        @self._props           = dict, contains properties of particle to be passed down to 
                                  child particles
    """
    def __init__(self, **props ):

        super(Particle, self).__init__()
        fixed_life = props.get('fixed_life', None)
        if fixed_life is not None:
            self._life = fixed_life
        else:
            self._life = props.get('max_life', 2) * random.random()

        self._birth = props.get('birth', time.time())
        self._velocity = Vec2d(props.get('velocity', (0, -1)))
        self._gravity = Vec2d(props.get('gravity', (0, 0)))
        self._fade = props.get('fade', False)
        size = props.get('size', 5)
        self._reproduce = props.get('reproduce', False)
        self._max_generations = props.get('max_generations', 2)
        self._generation = props.get('generation', 0)
        self._max_children = props.get('max_children', 2)
        self._child_particle = props.get('child_particle', Particle)
        img = props.get('image', None)

        if img is None:
            img = block
            color = props.get('color', None)
            if color is not None:
                img.fill(color)

        self.image = pygame.transform.scale(img, (size, size))
        self.rect = self.image.get_rect()
        self._age = 0
        pos = props.get('pos', (0,0))
        self._orig_pos = list(pos)
        self.set_position(*pos)
        self._props = props

    def __move__(self):
        """
            Called by update method to change particle's position using
            particle velocity
        """
        v = self._velocity
        self.rect.y += round(v.y)
        self.rect.x += round(v.x)

    def __reproduce__(self):
        """
            Used when reproduce property set to True, causes the 
            Particle to spawn children. Called upon the particle's
            death
        """
        groups = self.groups()
        props = self._props
        props['max_generations'] = self._max_generations
        props['generation'] = self._generation + 1
        props['max_children'] = self._max_children
        props['pos'] = (self.rect.x, self.rect.y)
        props['birth'] = time.time()
        props['max_life'] = self._life
        P = self._child_particle
        for _ in range(self._max_children):
            s = P(**props)
            for group in groups:
                group.add(s)

    def __gravity__(self):
        """
            Apply gravity to particle
        """
        g = self._gravity
        self._velocity += g * self._age

    def set_velocity(self, x, y):
        """Set particle's velocity"""
        self._velocity.x = x
        self._velocity.y = y

    def set_position(self, x, y):
        """Set particle's position"""
        self.rect.x = x
        self.rect.y = y

    def get_position(self):
        return self.rect.x, self.rect.y

    def get_velocity(self):
        return self._velocity

    def kill(self):
        if self._reproduce is True:
            if self._generation < self._max_generations:
                self.__reproduce__()
        super(Particle, self).kill()

    def update(self, t, surf):
        """
            Update particle

            Note:
                t must be time in seconds since the Epoch, i.e time.time() value
                anything else may require further arithmetic on your part to 
                achieve desired results.
        """
        age = t - self._birth
        if age >= self._life:
            self.kill()
            return
        self.__gravity__()
        self.__move__()
        life = age / self._life
        self._age = age
        if self._fade:
            # max_alpha = 255 * ( self._max_generations - self._generation / float(self._max_generations))
            max_alpha = 255
            alpha = max_alpha - (max_alpha * life)
            self.image.set_alpha(alpha)
        surf.blit(self.image, self.rect)


class ParticleSpawner(pygame.sprite.Sprite):
    """
        This class lets you spawn particles in a location,
        allowing you to set various properties of the spawned
        particles, as well as how often you want the particles
        to spawn, and the intensity(amount of particles to spawn 
        each time)

        This class is intended for custom particle spawning, use 
        Smoke and Splatter classes to spawn smoke and particle 
        splattering(explosions, water splashes,blood splashes, 
        rock splatter, confetti) and probably other fun things.


        default kwarg values:
            p_data={}, intensity=5, life_span=5, spawn_time=0.5, colorize=False
        
        @self._intensity        = int, number of particles to be spawned at a time
        
        @self._life             = float, life span of ParticleSpawner in seconds

        @self._spawn_clock       = time, how much time has passed since last particle spawn

        @self._spawn_time       = float, time between each spawn in seconds
                                    e.g. spawn time of 3.0 will spawn particles every
                                         3 seconds

        @self._colorize         = boolean, determines whether or not to randomly color
                                   a particle 

        @self.p_data            = dict, contains properties to be used when spawning
                                   particles

        @self._birth            = time ParticleSpawner was created 

        @self._age              = age of ParticleSpawner

        @self._pgroup           = pygame.sprite.Group, group that particles are added to
                                  and updated from

        @self._pos              = list, position of ParticleSpawner,
                                  this affects where the particles are spawned

        @self._color_list       = list of valid colors to be chosen from randomly
                                  if self._colorize is true.

    """
    #overriding Particle __reproduce__ method to reproduce a ParticleSpawner
    #can create chain reaction effects, like explosion, then smoke at scattered
    #locations. Or explosions that spawn random other explosions.
    # <-- make example of this
    def __init__(self, pos, particle_group, **props):
        super(ParticleSpawner, self).__init__()
        self._intensity = props.get('intensity', 5)
        self._life = props.get('life_span', 5)
        self._spawn_time = props.get('spawn_time', 0.5)
        self._colorize = props.get('colorize', False)
        self.p_data = {}
        pdata = props.get('p_data', {})
        self.p_data['size'] = pdata.get('size', 5)
        self.p_data['max_life'] = pdata.get('max_life', 2)
        self.p_data['fixed_life'] = pdata.get('fixed_life', None)
        self.p_data['pos'] = pos
        self.p_data['gravity'] = pdata.get('gravity', (0,0))
        self.p_data['fade'] = pdata.get('fade', True)
        self.p_data['image'] = pdata.get('image', None)
        self.particle = Particle
        self._birth = time.time()
        self._age = 0
        self._spawn_clock = 0
        self._pgroup = particle_group
        self._pos = list(pos)
        self._color_list = []

    def __colorize__(self):
        """
            Selects a random particle color from particles list of colors
            Note:
                This sets self.p_data['image'] to None, i.e
                the spawned particle will discard image property
                if any specified by set_particle_property.
        """
        self.p_data['image'] = None
        self.p_data['color'] = random.choice(self._color_list)
        # self.p_data['color'] = (random.randint(*ranges['r']),
        #     random.randint(*ranges['g']), random.randint(*ranges['b']))

    def __spawn__(self, t):
        """
            This method is called by update,
            creates particle to be spawned based on pdata(particle data), and
            places particles in intended particle_group
        """
        if self._colorize is True:
            self.__colorize__()
        self.p_data['birth'] = t
        p = self.particle(**self.p_data)
        self._pgroup.add(p)

    def set_position(self, x, y):
        """
            Set location where particles are to spawn
        """
        self._pos[0], self._pos[1] = x, y
        self.p_data['pos'] = self._pos

    def set_particle_class(self, particle_class):
        """
            Set particle class to specified class.
            Allows for custom particle spawning,
                particle must be subclass of Particle
        """
        if not issubclass(particle_class, Particle):
            raise TypeError("%s is not of type %s" %(particle_class, Particle))
        self.particle = particle_class

    def set_pos(self, x_or_pair, y=None):
        """
            Set location where particles are to spawn
        """
        if y is None:
            self._pos = x_or_pair
        else:
            self._pos = (x_or_pair, y)
        self.p_data['pos'] = self._pos

    def set_spawn_time(self, t):
        self._spawn_time = t

    def set_intensity(self, i):
        if i > 0:
            self._intensity = i

    # def set_particle_color_ranges(self, r_range, g_range, b_range):
    #     """
    #         set color ranges for colorize function.
    #         range=[min_val, max_val]
    #     """
    #     self._color_ranges['r'] = r_range
    #     self._color_ranges['g'] = g_range
    #     self._color_ranges['b'] = b_range

    def add_particle_color(self, color, *colors):
        """
            Add one or many colors to Particle's 
            color list. These colors are used by
            self.__colorize__ method
        """
        _colors = self._color_list
        if color not in _colors:
            _colors.append(color)
        for c in colors:
            if c not in _colors:
                _colors.append(c)

    def set_particle_property(self, prop, val):
        """
            Set particle property
             *properties:
                pos=tuple/list, color=tuple/list, velocity=tuple/list,
                gravity=tuple/list, size=int, max_life=float,
                fixed_life=float, image=pygame.Surface, fade=bool
        """
        self.p_data[prop] = val

    def toggle_colorize(self, b=None):
        """This will not do anything if no particle colors are added"""
        if len(self._color_list) > 1:
            self._colorize = b if b is not None else not self._colorize

    def update(self, t):
        """
            Updates the spawner

            Note:
                t must be time in seconds since the Epoch, i.e time.time() value
                anything else and you're on your own.
        """
        self._age = t - self._birth
        if self.is_dead():
            self.kill()
            return
        if t - self._spawn_clock > self._spawn_time:
            for _ in range(self._intensity):
                self.__spawn__(t)
            self._spawn_clock = t

    def is_dead(self):
        return self._age > self._life


class Splatter(ParticleSpawner):
    """
        Class for spawning particles to simulate a random
        splatter of particles.

        playing around with set_max_scatter_speed method to set how
        how fast and __colorize__ function can create fun effects.

        @self._max_scatter_speed        = maximum speed spawned particle's scatter from 
                                          the ParticleSpawner's position

    """

    def __init__(self, pos, particle_group, **props):
        props['intensity'] = props.get('intensity', 20)
        props['spawn_time'] = props.get('spawn_time', 0.01)
        p_data = {}
        p_data['fade'] = True
        p_data['max_life'] = 0.8
        p_data['gravity'] = (0, 0.2)
        props['p_data'] = p_data
        super(Splatter, self).__init__(pos, particle_group, **props)
        self._max_scatter_speed = props.get('max_scatter_speed', 3)

        self.images = []
        image = props.get('image', None)
        if image:
            for angle in (0, 90, 180, 270):
                self.images.append(pygame.transform.rotate(image, angle))


    def set_max_scatter_speed(self, s):
        """Set maximum speed that particle may scatter in a direction"""
        self._max_scatter_speed = s

    def __spawn__(self, t):
        p_data = self.p_data
        if len(self.images) > 0:
            p_data['image'] = random.choice(self.images)
        if self._colorize == True:
            self.__colorize__()
        p_data['birth'] = t
        max_speed = self._max_scatter_speed
        p = Particle(**p_data)
        v = Vec2d(random.uniform(-max_speed, max_speed), random.uniform(-max_speed, max_speed))
        p.set_velocity(v.x, v.y)
        self._pgroup.add(p)


class RadialSplatter(Splatter):
    """
        Similar to Splatter, however the particles scatter in
        a more radial manner. Better suited for confetti,
        and fountains where there is uniform radiation, and
        not a random scattering of particles such as water
        splatter.
    """

    def __init__(self, pos, particle_group, **props):
        super(RadialSplatter, self).__init__(pos, particle_group, **props)

    def __spawn__(self, t):

        p_data = self.p_data
        if len(self.images) > 0:
            p_data['image'] = random.choice(self.images)
        if self._colorize == True:
            self.__colorize__()
        p_data['birth'] = t
        max_speed = 100
        p = Particle(**p_data)
        direction = Vec2d(random.randint(-max_speed, max_speed), random.randint(-max_speed, max_speed)).normalized()
        v = direction * self._max_scatter_speed
        p.set_velocity(v.x, v.y)
        self._pgroup.add(p)


###################################################
## CONVENIENCE CLASSES
###################################################

class SmokeParticle(Particle):
    """
        Particle class with the __move__(self)
        method overriden and preset
        properties. SmokeParticles do not
        spawn at exact location but a random
        location close to the specified location
    """

    def __init__(self, *args, **props):
        if props.get('color', None) == None:
            props['color'] = (100, 100, 100)
        props['fade'] = props.get('fade', True)
        props['velocity'] = props.get('velocity', (0, -1.5))
        # props['reproduce'] = props.get('reproduce', True)
        super(SmokeParticle, self).__init__(**props)
        self.rect.x += random.randint(-5, 5)
        self.rect.y -= random.randint(-10, 10)

    def __move__(self):
        life = self._age / self._life
        v = self._velocity
        self.rect.y += int(v.y)
        self.rect.x += int(v.x) + random.randint(-1, 2) * life * (self._generation + 1)


class CyclicParticle(Particle):
    """Particle that moves in a circular motion"""

    def __init__(self, *args, **props):
        super(CyclicParticle, self).__init__(*args, **props)
        self.rect.x += random.randint(0, 5)
        self.rect.y -= random.randint(0, 5)
        self._clockwise = random.choice((1,-1))
        self._velocity = Vec2d(2, 0)

    def set_motion_radius(self, r):
        self._velocity = Vec2d(r, 0)

    def update(self, t, surf):
        super(CyclicParticle, self).update(t, surf)
        self._velocity.angle += 10 * self._clockwise

class Explosion(Splatter):
    """
        This class is simply a convenient Splatter with
        preset configuration for spawning explosions.
        The same result can easily be achieved with a Splatter
        object.
    """

    def __init__(self, pos, particle_group, **props):
        props['life_span'] = props.get('life_span', 0.5)
        props['spawn_time'] = props.get('spawn_time', 0.01)
        props['image'] = explosion_block
        super(Explosion, self).__init__(pos, particle_group, **props)
        self.set_particle_property('size', 10)


class Smoke(ParticleSpawner):
    """
        This class is simply a convenient ParticleSpawner with
        preset configuration for spawning smoke.
        The same result can easily be achieved with a ParticleSpawner
        object.
    """

    def __init__(self, pos, particle_group, **props):
        props['intensity'] = props.get('intensity', 5)
        props['spawn_time'] = props.get('spawn_time', 0.5)
        props['life_span'] = props.get('life_span', 5)
        super(Smoke, self).__init__(pos, particle_group, **props)
        self.particle = SmokeParticle
