import abc
from . import GameObject
from src.tiles import Tile


class RigidBody(GameObject):
    """A sprite with physical properties such as velocity"""

    __metaclass__ = abc.ABCMeta

    def __init__(self, collidable=True, *args, **kwargs):
        super(RigidBody, self).__init__(collidable, *args, **kwargs)

        self.velocity_x, self.velocity_y = 0.0, 0.0

        self.gravity = False

        self.original_x = self.x
        self.original_y = self.y

        self.old_x = self.x
        self.old_y = self.y

    def update(self, dt):
        if self.gravity and self.velocity_y >= -1000:
            self.velocity_y -= 1000 * dt

        self.old_x = self.x
        self.old_y = self.y

        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt

    def left(self, x):
        return x - self.width // 2

    def right(self, x):
        return x + self.width // 2

    def top(self, y):
        return y + self.height // 2

    def bottom(self, y):
        return y - self.height // 2

    def collision(self, other_object):

        if RigidBody not in other_object.__class__.__mro__ and Tile not in other_object.__class__.__mro__:
            return False, 0, 0, other_object.__class__

        if self.left(round(self.x)) <= other_object.right(round(other_object.x)) and \
                self.right(round(self.x)) >= other_object.left(round(other_object.x)) and \
                self.bottom(round(self.y)) <= other_object.top(round(other_object.y)) and \
                self.top(round(self.y)) >= other_object.bottom(round(other_object.y)):

            if self.top(round(self.old_y)) <= other_object.bottom(round(other_object.y)) <= self.top(round(self.y)):
                # Top
                return True, 0, 1, other_object.__class__
            elif self.bottom(round(self.old_y)) >= other_object.top(round(other_object.y)) >= self.bottom(round(self.y)):
                # Bottom
                return True, 0, -1, other_object.__class__

            elif self.right(round(self.old_x)) <= other_object.left(round(other_object.x)) <= self.right(round(self.x)):
                # Right
                return True, 1, 0, other_object.__class__
            elif self.left(round(self.old_x)) >= other_object.right(round(other_object.x)) >= self.left(round(self.x)):
                # Left
                return True, -1, 0, other_object.__class__

            return True, 0, 0, other_object.__class__

        return False, 0, 0, other_object.__class__

    @abc.abstractmethod
    def handle_collision_with(self, other_object, x, y):
        """Handle collisions"""
        return

    def die(self, dt=0):
        self.dead = True
