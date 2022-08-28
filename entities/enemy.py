import pyglet
import resources
from models import RigidBody
from util import center_image


class Enemy(RigidBody):
    def __init__(self, *args, **kwargs):
        sprite_sheet = resources.player_image
        sprites = pyglet.image.ImageGrid(sprite_sheet, rows=4, columns=23)

        for image in sprites:
            center_image(image)

        self.animations = {
            'Left': pyglet.image.Animation.from_image_sequence(sprites[0:4], 0.2).get_transform(True),
            'Right': pyglet.image.Animation.from_image_sequence(sprites[0:4], 0.2)
        }

        super(Enemy, self).__init__(False, self.animations['Right'], *args, **kwargs)
        self.current_animation = 'Right'

        self.velocity_x = 10

        self.hp = 5

    def turn(self):
        if self.current_animation == 'Left':
            animation = 'Right'
        else:
            animation = 'Left'

        if self.image == self.animations[animation]:
            return
        self.current_animation = animation
        self.image = self.animations[animation]
        self.velocity_x = -self.velocity_x

    def set_saturation(self, dt, saturation):
        self.color = (saturation, saturation, saturation)

    def take_damage(self, hp):
        if self.hp > 0:
            self.set_saturation(0, saturation=200)
            pyglet.clock.schedule_once(self.set_saturation, 0.2, saturation=255)
            self.hp -= hp
        else:
            self.die()
            pyglet.clock.unschedule(self.set_saturation)
