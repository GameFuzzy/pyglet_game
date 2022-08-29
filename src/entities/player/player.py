import math
import pyglet
from pyglet.window import key
from . import AnimationController, Projectile
from entities.enemy import Enemy
from models.gameobject import GameObject
from tiles import Portal
from load.resources import jump_sound, player_hit_sound, health_image
from models.rigidbody import RigidBody


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

        self.min_jump = 100
        self.max_jump = 300
        self.jump_charge = self.min_jump
        self.jump_charge_speed = 1000
        self.jump = 0
        self.boost_counter = 0

        self.projectile_speed = 500

        self.speed = 200
        self.friction = 0.6

        self.hp = 5
        self.invincible = False

        self.key_handler = key.KeyStateHandler()
        self.event_handlers = [self, self.key_handler]

        self.hp_scale = 0.7

        self.health_bar = [GameObject(False, health_image, x * 32 * self.hp_scale, window_height - 32 * self.hp_scale, batch=self.batch) for x in range(self.hp)]
        for hp in self.health_bar:
            hp.scale = self.hp_scale

    def update(self, dt):

        super(Player, self).update(dt)

        if not self.gravity:
            if -0.1 > self.velocity_x > 0.1:
                self.velocity_x = 0
            else:
                self.velocity_x *= self.friction

        left = self.key_handler[key.LEFT] or self.key_handler[key.A]
        right = self.key_handler[key.RIGHT] or self.key_handler[key.D]

        if self.key_handler[key.SPACE] and self.jump:
            if right and not left:
                self.animation_controller.play(direction='Right')
            elif left and not right:
                self.animation_controller.play(direction='Left')
            if self.jump_charge < self.max_jump:
                self.jump_charge += self.jump_charge_speed * dt

        elif right and not left and not self.gravity:
            self.animation_controller.play(direction='Right')
            self.velocity_x = self.speed

        elif left and not right and not self.gravity:
            self.animation_controller.play(direction='Left')
            self.velocity_x = -self.speed

        else:
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
            self.x = min_x + 1
            self.velocity_x = 0
        elif self.x > max_x:
            self.x = max_x - 1
        if self.y < min_y:
            self.y = min_y + 1
        elif self.y > max_y:
            self.y = max_y - 1
            self.velocity_y = 0

    def on_key_press(self, symbol, modifiers):
        if symbol == key.SPACE and not self.gravity:
            self.animation_controller.play('JumpPreparation')
            self.jump = 2
            self.velocity_x = 0

    def on_key_release(self, symbol, modifiers):
        if symbol == key.SPACE and not self.gravity and self.jump:
            left = self.key_handler[key.LEFT] or self.key_handler[key.A]
            right = self.key_handler[key.RIGHT] or self.key_handler[key.D]

            self.animation_controller.play('JumpUp')
            self.velocity_y = self.jump_charge

            if right and not left:
                self.jump = 1
            elif left and not right:
                self.jump = -1
            if self.jump != 2:
                self.velocity_x = self.jump * self.speed
            jump_sound.play()
            self.jump_charge = self.min_jump
            self.jump = 0

    def on_mouse_press(self, x, y, dx, dy):
        self.new_objects.append(Projectile(self.cursor.x, self.cursor.y, self.x, self.y, batch=self.batch))
        if self.cursor.x > self.x:
            self.animation_controller.play(direction='Right')
        elif self.cursor.x < self.x:
            self.animation_controller.play(direction='Left')
        if self.boost_counter < 2:
            # sqrt((x - player_x)**2 + (y - player_y)**2) * k = 1
            dx = self.cursor.x - self.x
            dy = self.cursor.y - self.y

            # Normalization factor
            k = math.sqrt(dx ** 2 + dy ** 2)
            self.velocity_x = -dx / k * self.projectile_speed
            self.velocity_y = -dy / k * self.projectile_speed
            self.boost_counter += 1

    def toggle_invincibility(self, dt=0):
        if self.invincible:
            self.set_saturation(0, 255)
        else:
            self.set_saturation(0, 200)
        self.invincible = not self.invincible

    def set_saturation(self, dt, saturation):
        self.color = (saturation, saturation, saturation)

    def remove_hp(self, dt):
        self.health_bar.pop()

    def take_damage(self, hp):
        self.health_bar[-1].color = (200, 200, 200)
        pyglet.clock.schedule_once(self.remove_hp, 0.2)
        if self.hp > hp:
            self.toggle_invincibility()
            pyglet.clock.schedule_once(self.toggle_invincibility, 0.5)
            player_hit_sound.play()
            self.hp -= hp
        else:
            self.die()

    def handle_collision_with(self, other_object, x, y):
        super(Player, self).handle_collision_with(other_object, x, y)

        if GameObject not in other_object.__class__.__mro__:
            return

        if not other_object.collidable:
            if other_object.__class__ == Portal:
                self.can_proceed = True
            if other_object.__class__ == Enemy and not self.invincible:
                self.take_damage(1)
                if x or y:
                    self.velocity_y = 200
                    self.gravity = True
                    if math.fabs(self.velocity_x) >= 100:
                        self.velocity_x = -self.velocity_x
                    else:
                        self.velocity_x = 100
            return

        if x:
            self.velocity_x = 0

            if x == 1:
                # Right
                self.x = other_object.left(other_object.x) - self.width // 2 - 1
            else:
                # Left
                self.x = other_object.right(other_object.x) + self.width // 2 + 1
        else:
            self.velocity_y = 0

            if y == 1:
                # Top
                self.y = other_object.bottom(other_object.y) - self.height // 2 - 1
            else:
                # Bottom
                self.gravity = False
                self.boost_counter = 0
                self.animation_controller.play('Landing')
                self.y = other_object.top(other_object.y) + self.height // 2
