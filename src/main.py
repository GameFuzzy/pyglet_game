from pyglet.gl import *
from pyglet.window import Window, key
from entities.enemy import Enemy
from entities.player import Player, Projectile
from models import GameObject
from tiles import Portal, Tile
from load.resources import sheet_image, cursor_image, bgm, button_01_image
from load.load import load_map, reset_map, change_map
from ui.button import Button

glEnable(GL_TEXTURE_2D)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

window = Window(854, 480, resizable=True, vsync=False)
WINDOW_TRUE_WIDTH = 426
WINDOW_TRUE_HEIGHT = 240
window.set_exclusive_mouse(True)
glClearColor(.36, .59, .55, 1)

entities = pyglet.graphics.Batch()
foreground = pyglet.graphics.Batch()
background = pyglet.graphics.Batch()
gui = pyglet.graphics.Batch()

cursor = pyglet.sprite.Sprite(cursor_image, WINDOW_TRUE_WIDTH // 2, WINDOW_TRUE_HEIGHT // 2, batch=entities)

tiles = pyglet.image.ImageGrid(sheet_image, rows=8, columns=17)

menu_objects = []
game_objects = []

CURRENT_SCALE_WIDTH = 1
CURRENT_SCALE_HEIGHT = 1

current_scroll = [0, 0]
scroll = [0, 0]

bgm = bgm.play()

bgm.loop = True
bgm.volume = 0.5


@window.event
def on_resize(width, height):
    global CURRENT_SCALE_WIDTH
    global CURRENT_SCALE_HEIGHT

    width_scaling_factor = window.width / WINDOW_TRUE_WIDTH
    height_scaling_factor = window.height / WINDOW_TRUE_HEIGHT

    glScalef(width_scaling_factor / CURRENT_SCALE_WIDTH, height_scaling_factor / CURRENT_SCALE_HEIGHT, 0)
    CURRENT_SCALE_WIDTH = width_scaling_factor
    CURRENT_SCALE_HEIGHT = height_scaling_factor


counter = pyglet.window.FPSDisplay(window=window)


@window.event
def on_draw():
    window.clear()
    background.draw()
    foreground.draw()
    gui.draw()
    entities.draw()
    counter.draw()


def on_mouse_motion(x, y, dx, dy):
    if 0 < cursor.x < WINDOW_TRUE_WIDTH or cursor.x >= WINDOW_TRUE_WIDTH and dx < 0 or cursor.x <= 0 and dx > 0:
        cursor.x += dx
    if 0 < cursor.y < WINDOW_TRUE_HEIGHT or cursor.y >= WINDOW_TRUE_HEIGHT and dy < 0 or cursor.y <= 0 and dy > 0:
        cursor.y += dy


def on_key_press(symbol, modifiers):
    global current_level
    global game_objects
    global current_scroll
    if game_objects and (symbol == key.UP or symbol == key.W) and game_objects[0].can_proceed and not len(
            [obj for obj in game_objects if obj.__class__ == Enemy]):
        if current_level == 2:
            pyglet.text.Label('Le end',
                              font_name='Dogica Pixel',
                              bold=True,
                              color=(0, 255, 0, 255),
                              font_size=36,
                              x=WINDOW_TRUE_WIDTH // 2, y=WINDOW_TRUE_HEIGHT // 2,
                              anchor_x='center', anchor_y='center', batch=gui)
            return
        next_level = load_map(f'level{current_level + 1}')
        current_scroll = [0, 0]
        game_objects = reset_map(game_objects)
        game_objects.extend(change_map(tiles, (foreground, background), next_level))
        current_level += 1


window.push_handlers(on_mouse_motion, on_key_press)

menu = False

game_over = False


def toggle_game_visibility():
    for obj in game_objects:
        if obj.batch:
            obj.batch = None
        else:
            obj.batch = obj.original_batch
    if game_objects:
        for obj in game_objects[0].health_bar:
            obj.visible = not obj.visible


def set_game():
    global game_objects
    global menu
    menu = False
    toggle_game_visibility()
    for to_remove in menu_objects:
        # Remove from batches
        to_remove.delete()
        menu_objects.remove(to_remove)
        if to_remove.text:
            to_remove.text.delete()
    player = Player(WINDOW_TRUE_WIDTH, WINDOW_TRUE_HEIGHT, cursor, batch=entities)
    game_map = load_map(f'level{current_level}')
    game_objects = [player] + (change_map(tiles, (foreground, background), game_map))
    for handler in player.event_handlers:
        window.push_handlers(handler)


def set_menu():
    global menu
    menu = True
    toggle_game_visibility()
    if game_objects:
        window.remove_handlers(game_objects[0])
    menu_objects.append(Button("Play", cursor, button_01_image, WINDOW_TRUE_WIDTH // 2, WINDOW_TRUE_HEIGHT // 2, batch=gui))
    for obj in menu_objects:
        window.push_handlers(obj.event_handler)


current_level = 1
set_menu()


def update(dt):
    global menu
    global game_over

    to_add = []

    if cursor.x > window.width:
        cursor.x = window.width
    elif cursor.x < 0:
        cursor.x = 0
    if cursor.y > window.height:
        cursor.y = window.height
    elif cursor.y < 0:
        cursor.y = 0

    if menu:
        for obj in menu_objects:
            obj.update(dt)
        for obj in [obj for obj in menu_objects if obj.__class__ == Button]:
            if obj.pressed:
                if obj.action == 'Play':
                    set_game()
        return
    else:
        if game_objects[0].dead and not game_over:
            pyglet.clock.unschedule(game_objects[0].animation_controller.change_animation)
            scroll[0] = 0
            scroll[1] = 0
            game_over = True
            cursor.visible = False
            window.pop_handlers()
            window.remove_handlers(game_objects[0])
            pyglet.text.Label('Bruh',
                              font_name='Dogica Pixel',
                              bold=True,
                              color=(255, 0, 0, 255),
                              font_size=36,
                              x=WINDOW_TRUE_WIDTH // 2, y=WINDOW_TRUE_HEIGHT // 2,
                              anchor_x='center', anchor_y='center', batch=gui)
    
        if round(game_objects[0].x) - current_scroll[0] > WINDOW_TRUE_WIDTH * 1.5 - 20:
            scroll[0] = 5 * (round(current_scroll[0]) + WINDOW_TRUE_WIDTH - 20)
        elif round(game_objects[0].x) - current_scroll[0] < WINDOW_TRUE_WIDTH * 0.5:
            scroll[0] = 5 * (round(current_scroll[0]))
        else:
            scroll[0] = 5 * -(WINDOW_TRUE_WIDTH // 2 - round(game_objects[0].x))

        if round(game_objects[0].y) - current_scroll[1] > WINDOW_TRUE_HEIGHT * 1.5 - 39:
            scroll[1] = 5 * (round(current_scroll[1]) + WINDOW_TRUE_HEIGHT)
        elif round(game_objects[0].y) - current_scroll[1] < WINDOW_TRUE_HEIGHT * 0.5 - 39:
            scroll[1] = 5 * round(current_scroll[1])
        else:
            scroll[1] = -5 * (WINDOW_TRUE_HEIGHT // 2 - 39 - round(game_objects[0].y))
    
        current_scroll[0] -= scroll[0] * dt
        current_scroll[1] -= scroll[1] * dt
    
        for obj in [obj for obj in game_objects if obj.batch != background]:
            obj.x -= scroll[0] * dt
            obj.y -= scroll[1] * dt
            obj.update(dt)
            to_add.extend(obj.new_objects)
            obj.new_objects = []
    
        for to_remove in [obj for obj in game_objects if obj.dead]:
            to_add.extend(to_remove.new_objects)
            # Remove from batches
            to_remove.delete()
            game_objects.remove(to_remove)
    
        for enemy in [obj for obj in game_objects if obj.__class__ == Enemy]:
            enemy_collisions = []
            for i in range(0, len(game_objects)):
                other_obj = game_objects[i]
                enemy_collisions.append(enemy.collision(other_obj))
                if enemy_collisions[i][0]:
                    enemy.handle_collision_with(other_obj, enemy_collisions[i][1], enemy_collisions[i][2])
            if len([collision for collision in enemy_collisions if collision[3] == Tile and collision[2] == -1]) < 3:
                enemy.turn()
    
        for projectile in [obj for obj in game_objects if obj.__class__ == Projectile]:
            for other_obj in game_objects:
                if (GameObject not in other_obj.__class__.__mro__ or not other_obj.collidable) and other_obj.__class__ != Enemy:
                    continue
                projectile_collision = projectile.collision(other_obj)
                if projectile_collision[0]:
                    projectile.handle_collision_with(other_obj, projectile_collision[1], projectile_collision[2])
                    break
    
        player_collisions = []
        for i in range(1, len(game_objects)):
            if game_objects[0].dead:
                break
            player_collisions.append(game_objects[0].collision(game_objects[i]))
            if player_collisions[i - 1][0]:
                game_objects[0].handle_collision_with(game_objects[i], player_collisions[i - 1][1], player_collisions[i - 1][2])
        if not game_objects[0].gravity and not any(map(lambda collision: collision[2] == -1, player_collisions)):
            game_objects[0].gravity = True
        if not any([collision for collision in player_collisions if collision[3] == Portal and collision[0]]):
            game_objects[0].can_proceed = False
    
        for obj in to_add:
            game_objects.append(obj)


if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1 / 165.0)
    pyglet.app.run()
