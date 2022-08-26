import random

import pyglet

from rigidbody import RigidBody


class Particle(RigidBody):
    def __init__(self, velocity_x, velocity_y, *args, **kwargs):
        super(Particle, self).__init__(*args, **kwargs)

        self.velocity_x = velocity_x * 200 + random.randint(-50, 50)
        self.velocity_y = velocity_y * 200 + random.randint(-50, 50)

        self.rotation_speed = random.randint(-5000, 5000)
        pyglet.clock.schedule_once(self.die, random.randint(10, 100) / 200)

    def update(self, dt):
        super(Particle, self).update(dt)
        self.rotation = self.rotation_speed * dt