import pyglet
from pyglet.window import key
from animationcontroller import AnimationController
from enemy import Enemy
from portal import Portal
from projectile import Projectile
from rigidbody import RigidBody


class Player(RigidBody):
    def __init__(self, window_width, window_height, cursor, *args, **kwargs):

        self.cursor = cursor

        self.current_level = 1
        self.can_proceed = False

        self.window_width = window_width
        self.window_height = window_height

        self.animation_controller = AnimationController(self)

        super(Player, self).__init__(False, self.animation_controller.animations['StillRight'], window_width // 2,
                                     window_height // 2, *args, **kwargs)
        self.animation_controller.current_animation = 'StillRight'

        self.jump_charge = 0
        self.jump = 0

        self.hp = 5

        self.key_handler = key.KeyStateHandler()
        self.event_handlers = [self, self.key_handler]

    def update(self, dt):

        super(Player, self).update(dt)

        if self.key_handler[key.SPACE] and self.jump:
            if self.key_handler[key.RIGHT] and not self.key_handler[key.LEFT]:
                self.animation_controller.play(direction='Right')
            elif self.key_handler[key.LEFT] and not self.key_handler[key.RIGHT]:
                self.animation_controller.play(direction='Left')
            if self.jump_charge < 500:
                self.jump_charge += 1000 * dt

        elif self.key_handler[key.RIGHT] and not self.key_handler[key.LEFT]:
            self.animation_controller.play(direction='Right')
            if not self.key_handler[key.SPACE] and not self.jump:
                self.velocity_x = 100
            else:
                self.jump = 1

        elif self.key_handler[key.LEFT] and not self.key_handler[key.RIGHT]:
            self.animation_controller.play(direction='Left')
            if not self.key_handler[key.SPACE] and not self.jump:
                self.velocity_x = -100
            else:
                self.jump = -1

        elif self.gravity:
            self.animation_controller.play('Still')

        else:
            self.velocity_x = 0
            self.animation_controller.play('Still')

        if self.velocity_y < 0:
            self.animation_controller.play('Fall')

        self.check_bounds()

    def check_bounds(self):
        min_x = self.width / 2
        min_y = self.height / 2
        max_x = self.window_width - self.width / 2
        max_y = self.window_height - self.height / 2
        if self.x < min_x:
            self.x = min_x
            self.velocity_x = 0
        elif self.x > max_x:
            self.x = max_x
        if self.y < min_y:
            self.y = min_y
        elif self.y > max_y:
            self.y = max_y
            self.velocity_y = 0

    def on_key_press(self, symbol, modifiers):
        if symbol == key.SPACE and not self.gravity:
            self.animation_controller.play('JumpPreparation')
            if self.velocity_x:
                self.jump = self.velocity_x / 100
            else:
                self.jump = 2
            self.velocity_x = 0

    def on_key_release(self, symbol, modifiers):
        if symbol == key.SPACE and not self.gravity and self.jump:
            self.animation_controller.play('JumpUp')
            self.velocity_y = self.jump_charge
            if self.jump != 2:
                self.velocity_x = self.jump * 100
            self.jump_charge = 0
            self.jump = 0
            self.gravity = True
        if symbol == key.RIGHT or symbol == key.LEFT:
            self.velocity_x = 0

    def on_mouse_press(self, x, y, dx, dy):
        self.new_objects.append(Projectile(self.cursor.x, self.cursor.y, self.x, self.y, batch=self.batch))

    def set_saturation(self, dt, saturation):
        self.color = (saturation, saturation, saturation)

    def take_damage(self, hp):
        if self.hp > 0:
            self.set_saturation(0, saturation=200)
            pyglet.clock.schedule_once(self.set_saturation, 0.2, saturation=255)
            self.hp -= hp
        else:
            self.die()
    def handle_collision_with(self, other_object, x, y):
        super(Player, self).handle_collision_with(other_object, x, y)

        if RigidBody not in other_object.__class__.__mro__:
            return

        if not other_object.collidable:
            if other_object.__class__ == Portal:
                self.can_proceed = True
            if other_object.__class__ == Enemy:
                self.velocity_x *= -1
                self.velocity_y *= -1
                self.take_damage(1)
            return

        if x:
            self.velocity_x = 0
            if x == 1:
                # Right
                self.x = other_object.left(other_object.x) - self.width // 2
            else:
                # Left
                self.x = other_object.right(other_object.x) + self.width // 2
        else:
            self.velocity_y = 0

            if y == 1:
                # Top
                self.y = other_object.bottom(other_object.y) - self.height // 2
            else:
                # Bottom
                self.gravity = False
                self.animation_controller.play('Landing')
                self.y = other_object.top(other_object.y) + self.height // 2
