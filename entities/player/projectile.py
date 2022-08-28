import math
import numpy as np
import pyglet
import resources
from entities.enemy import Enemy
from models.gameobject import GameObject
from vfx.particle import Particle
from vfx.shockwave import Shockwave
from resources import particle_image, enemy_hit_sound, ground_hit_sound
from models.rigidbody import RigidBody
from util import center_image


class Projectile(RigidBody):

    def __init__(self, cursor_x, cursor_y, player_x, player_y, *args, **kwargs):
        sprite_sheet = resources.swoosh_image
        sprites = pyglet.image.ImageGrid(sprite_sheet, rows=1, columns=4)

        for image in sprites:
            center_image(image)

        sprite = pyglet.image.Animation.from_image_sequence(sprites, 0.1, False)

        # sqrt((x - player_x)**2 + (y - player_y)**2) * k = 1
        dx = cursor_x - player_x
        dy = cursor_y - player_y

        # Normalization factor
        k = math.sqrt(dx ** 2 + dy ** 2)

        super(Projectile, self).__init__(False, sprite, player_x, player_y, *args, **kwargs)

        self.scale = 0.7

        self.velocity_x = dx / k * 500
        self.velocity_y = dy / k * 500

        angle = math.atan2(dy / k, dx / k) - math.atan2(1, 0)

        # Note: pyglet's rotation attributes are in "negative degrees"
        self.rotation = -math.degrees(angle) - 90

        pyglet.clock.schedule_once(self.die, 0.4, particles=False, shockwave=False)

    def handle_collision_with(self, other_object, x, y):
        particles = True
        if other_object.__class__ == Enemy:
            other_object.take_damage(1)
            particles = False

        if (GameObject not in other_object.__class__.__mro__ or not other_object.collidable) and particles:
            return

        normal = np.array([-x, -y])
        if x == 1:
            self.die(0, particles, True, normal, other_object.left(other_object.x), self.y)
        if x == -1:
            self.die(0, particles, True, normal, other_object.right(other_object.x), self.y)
        if y == 1:
            self.die(0, particles, True, normal, self.x, other_object.bottom(other_object.y))
        if y == -1:
            self.die(0, particles, True, normal, self.x, other_object.top(other_object.y))

    def die(self, dt=0, particles=True, shockwave=True, normal=np.array([0, 0]), x=0, y=0):
        if particles:
            ground_hit_sound.play()
            # r=d−2(d⋅n)n
            direction = np.array([math.cos(-math.radians(self.rotation)), math.sin(math.radians(-self.rotation))])
            reflection = direction - 2 * np.dot(direction, normal) * normal
            for i in range(0, 100):
                self.new_objects.append(Particle(reflection[0], reflection[1], particle_image, x, y, batch=self.batch))
        if shockwave:
            self.new_objects.append(Shockwave(x, y, batch=self.batch))

        if shockwave and not particles:
            enemy_hit_sound.play()

        pyglet.clock.unschedule(self.die)
        super(Projectile, self).die(dt)
