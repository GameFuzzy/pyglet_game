import pyglet
from load import resources
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
            'Right': pyglet.image.Animation.from_image_sequence(sprites[0:4], 0.2),
            'HurtLeft': pyglet.image.Animation.from_image_sequence(sprites[4:8], 0.1).get_transform(True),
            'HurtRight': pyglet.image.Animation.from_image_sequence(sprites[4:8], 0.1),
        }

        super(Enemy, self).__init__(False, self.animations['Right'], *args, **kwargs)
        self.current_animation = 'Right'

        self.velocity_x = 10

        self.hp = 3

    def turn(self):
        if self.current_animation == 'Left' or self.current_animation == 'HurtLeft':
            animation = 'Right'
            self.x += 1
        else:
            animation = 'Left'
            self.x -= 1

        pyglet.clock.unschedule(self.reset_animation)

        if self.image == self.animations[animation]:
            return
        self.current_animation = animation
        self.image = self.animations[animation]
        self.velocity_x = -self.velocity_x

    def reset_animation(self, dt):
        animation = 'Right'
        if self.current_animation == 'HurtLeft' or self.current_animation == 'Left':
            animation = 'Left'

        self.image = self.animations[animation]
        self.current_animation = animation

    def take_damage(self, hp):
        if self.hp > hp:
            animation = 'HurtRight'
            if self.current_animation == 'Left':
                animation = 'HurtLeft'

            self.image = self.animations[animation]
            self.current_animation = animation

            pyglet.clock.schedule_once(self.reset_animation, 0.3)
            self.hp -= hp
        else:
            self.die()
            pyglet.clock.unschedule(self.reset_animation)
