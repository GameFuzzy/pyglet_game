import pyglet
import resources
import rigidbody


class Enemy(rigidbody.RigidBody):
    def __init__(self, *args, **kwargs):

        sprite_sheet = resources.player_image
        sprites = pyglet.image.ImageGrid(sprite_sheet, rows=4, columns=23)

        for image in sprites:
            image.anchor_x = image.width / 2
            image.anchor_y = image.height / 2

        super(Enemy, self).__init__(False, sprites[0], *args, **kwargs)