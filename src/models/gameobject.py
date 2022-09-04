import abc
import pyglet.sprite


class GameObject(pyglet.sprite.Sprite):
    __metaclass__ = abc.ABCMeta

    def __init__(self, collidable=False, *args, **kwargs):
        super(GameObject, self).__init__(*args, **kwargs)
        self.original_batch = self.batch
        self.collidable = collidable
        self.dead = False

        self.new_objects = []

    @abc.abstractmethod
    def update(self, dt):
        """Runs every frame"""

    def die(self, dt=0):
        self.dead = True
