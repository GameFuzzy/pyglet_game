import abc

import pyglet


class RigidBody(pyglet.sprite.Sprite):
    """A sprite with physical properties such as velocity"""

    __metaclass__ = abc.ABCMeta

    def __init__(self, collidable=True, *args, **kwargs):
        super(RigidBody, self).__init__(*args, **kwargs)

        self.collidable = collidable

        self.velocity_x, self.velocity_y = 0.0, 0.0

        self.gravity = False

        self.dead = False

        self.new_objects = []

        self.event_handlers = []

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
        if self.left(self.x) <= other_object.right(other_object.x) and \
                self.right(self.x) >= other_object.left(other_object.x) and \
                self.bottom(self.y) <= other_object.top(other_object.y) and \
                self.top(self.y) >= other_object.bottom(other_object.y):

            if self.top(self.old_y) <= other_object.bottom(other_object.y) <= self.top(self.y):
                # Top
                return True, 0, 1
            elif self.bottom(self.old_y) >= other_object.top(other_object.y) >= self.bottom(self.y):
                # Bottom
                return True, 0, -1

            elif self.right(self.old_x) <= other_object.left(other_object.x) <= self.right(self.x):
                # Right
                return True, 1, 0
            elif self.left(self.old_x) >= other_object.right(other_object.x) >= self.left(self.x):
                # Left
                return True, -1, 0

        return False, 0, 0

    @abc.abstractmethod
    def handle_collision_with(self, other_object, x, y):
        """Handle collisions"""
        return
