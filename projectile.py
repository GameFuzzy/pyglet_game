import math
import pyglet
import resources
from enemy import Enemy
from rigidbody import RigidBody
from util import center_image


class Projectile(RigidBody):

    def __init__(self, cursor_x, cursor_y, player_x, player_y, *args, **kwargs):
        sprite_sheet = resources.swoosh_image
        sprites = pyglet.image.ImageGrid(sprite_sheet, rows=1, columns=4)

        for image in sprites:
            center_image(image)

        sprite = pyglet.image.Animation.from_image_sequence(sprites, 0.05, False)

        # sqrt((x - player_x)**2 + (y - player_y)**2) * k = 1
        dx = cursor_x - player_x
        dy = cursor_y - player_y

        # Normalization factor
        k = math.sqrt(dx ** 2 + dy ** 2)

        super(Projectile, self).__init__(False, sprite, player_x + dx/k * 30, player_y + dy/k * 30, *args, **kwargs)

        self.velocity_x = dx / k * 500
        self.velocity_y = dy / k * 500

        angle = math.atan2(dy/k, dx/k) - math.atan2(1, 0)

        # Note: pyglet's rotation attributes are in "negative degrees"
        self.rotation = -math.degrees(angle) - 90

        pyglet.clock.schedule_once(self.die, 0.5)

    def handle_collision_with(self, other_object, x, y):
        self.die()
        if other_object.__class__ == Enemy:
            other_object.take_damage(1)
