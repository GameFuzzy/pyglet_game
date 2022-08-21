import pyglet

import resources
from util import center_image


class AnimationController:

    def __init__(self, player):
        self.player = player

        sprite_sheet = resources.player_image
        sprites = pyglet.image.ImageGrid(sprite_sheet, rows=4, columns=23)

        for image in sprites:
            center_image(image)

        self.animations = {
            'StillLeft': pyglet.image.Animation.from_image_sequence(sprites[46:47:1], 0.1).get_transform(True),
            'StillRight': pyglet.image.Animation.from_image_sequence(sprites[46:47:1], 0.1),
            'RunLeft': pyglet.image.Animation.from_image_sequence(sprites[60:64:1], 0.1).get_transform(True),
            'RunRight': pyglet.image.Animation.from_image_sequence(sprites[60:64:1], 0.1),
            'JumpPreparationLeft': pyglet.image.Animation.from_image_sequence(sprites[50:51:1], 0.1).get_transform(True),
            'JumpPreparationRight': pyglet.image.Animation.from_image_sequence(sprites[50:51:1], 0.1),
            'JumpUpLeft': pyglet.image.Animation.from_image_sequence(sprites[51:52:1], 0.1).get_transform(True),
            'JumpUpRight': pyglet.image.Animation.from_image_sequence(sprites[51:52:1], 0.1),
            'FallLeft': pyglet.image.Animation.from_image_sequence(sprites[53:54:1], 0.1).get_transform(True),
            'FallRight': pyglet.image.Animation.from_image_sequence(sprites[53:54:1], 0.1),
            'LandingLeft': pyglet.image.Animation.from_image_sequence(sprites[54:55:1], 0.1).get_transform(True),
            'LandingRight': pyglet.image.Animation.from_image_sequence(sprites[54:55:1], 0.1)
        }

        self.current_animation = 'StillRight'

    def change_animation(self, target_animation, change_direction=False):
        animation = target_animation
        if change_direction:
            pass
        elif 'Left' in self.current_animation:
            animation = target_animation + 'Left'
        else:
            animation = target_animation + 'Right'

        if self.player.image == self.animations[animation]:
            return
        self.current_animation = animation
        self.player.image = self.animations[animation]

    def play(self, animation='', direction=''):
        if direction:
            if 'Still' in self.current_animation or 'Landing' in self.current_animation:
                self.change_animation('Run' + direction, True)
            if 'JumpUp' in self.current_animation:
                self.change_animation('JumpUp' + direction, True)
            if 'Fall' in self.current_animation:
                self.change_animation('Fall' + direction, True)
            if 'JumpPreparation' in self.current_animation:
                self.change_animation('JumpPreparation' + direction, True)

        elif animation == 'JumpPreparation':
            self.change_animation(animation)
            pyglet.clock.unschedule(self.animation_callback)
        elif animation == 'JumpUp' and 'JumpPreparation' in self.current_animation:
            self.change_animation(animation)
        elif animation == 'Still' and 'Run' in self.current_animation:
            self.change_animation(animation)
        elif animation == 'Fall':
            if 'Run' in self.current_animation or \
                    'Still' in self.current_animation or \
                    'JumpUp' in self.current_animation:
                self.change_animation(animation)
        elif animation == 'Landing' and 'Fall' in self.current_animation:
            self.change_animation(animation)
            pyglet.clock.schedule_once(self.animation_callback, 0.2, 'Still')

    def animation_callback(self, dt, animation):
        self.change_animation(animation)
