import pyglet
from src.models.rigidbody import RigidBody
import random


class Particle(RigidBody):
    def __init__(self, velocity_x, velocity_y, color, *args, **kwargs):
        super(Particle, self).__init__(False, *args, **kwargs)

        self.color = color

        self.velocity_x = velocity_x * 200 + random.randint(-50, 50)
        self.velocity_y = velocity_y * 200 + random.randint(-50, 50)
        self.scale = 2

        self.rotation_speed = random.randint(-200, 200)
        self.shrink_speed = random.randint(3, 4)
        pyglet.clock.schedule_once(self.die, 2 / self.shrink_speed)

    def update(self, dt):
        super(Particle, self).update(dt)
        self.rotation += self.rotation_speed * dt
        self.scale -= self.shrink_speed * dt

    def handle_collision_with(self, other_object, x, y):
        pass
