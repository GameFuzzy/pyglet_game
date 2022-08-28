import pyglet

import resources
from models.gameobject import GameObject
from util import center_image


class Shockwave(GameObject):

    def __init__(self, *args, **kwargs):
        sprite_sheet = resources.shockwave_image
        sprites = pyglet.image.ImageGrid(sprite_sheet, rows=1, columns=6)

        for image in sprites:
            center_image(image)

        sprite = pyglet.image.Animation.from_image_sequence(sprites, 0.03, False)

        super().__init__(False, sprite, *args, **kwargs)

        pyglet.clock.schedule_once(self.die, 0.21)

    def update(self, dt):
        self.scale += 5 * dt