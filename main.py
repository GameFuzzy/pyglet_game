from pyglet.gl import *
from pyglet.window import Window, key
from entities.enemy import Enemy
from entities.player import Player, Projectile
from models import GameObject
from tiles import Portal, Tile
from resources import sheet_image, cursor_image, bgm
from maps.load import load_map, reset_map, change_map

glEnable(GL_TEXTURE_2D)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

window = Window(854, 480, resizable=True, vsync=False)
WINDOW_TRUE_WIDTH = 426
WINDOW_TRUE_HEIGHT = 240
window.set_exclusive_mouse(True)
glClearColor(.3, .7, 1, 1)

entities = pyglet.graphics.Batch()
cursor = pyglet.sprite.Sprite(cursor_image, WINDOW_TRUE_WIDTH // 2, WINDOW_TRUE_HEIGHT // 2, batch=entities)
player = Player(WINDOW_TRUE_WIDTH, WINDOW_TRUE_HEIGHT, cursor, batch=entities)

game_objects = [player]

for handler in player.event_handlers:
    window.push_handlers(handler)

foreground = pyglet.graphics.Batch()

current_level = 1

game_map = load_map('level1')

tiles = pyglet.image.ImageGrid(sheet_image, rows=8, columns=17)

game_objects.extend(change_map(tiles, foreground, game_map))

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
    foreground.draw()
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
    if (symbol == key.UP or symbol == key.W) and player.can_proceed and not len(
            [obj for obj in game_objects if obj.__class__ == Enemy]):
        if current_level == 2:
            pyglet.text.Label('Le end',
                              font_name='Dogica Pixel',
                              bold=True,
                              color=(0, 255, 0, 255),
                              font_size=36,
                              x=WINDOW_TRUE_WIDTH // 2, y=WINDOW_TRUE_HEIGHT // 2,
                              anchor_x='center', anchor_y='center', batch=foreground)
            return
        next_level = load_map(f'level{current_level + 1}')
        current_scroll = [0, 0]
        game_objects = reset_map(game_objects)
        game_objects.extend(change_map(tiles, foreground, next_level))
        current_level += 1


window.push_handlers(on_mouse_motion, on_key_press)

game_over = False


def update(dt):
    global game_over

    to_add = []

    if player.dead and not game_over:
        scroll[0] = 0
        scroll[1] = 0
        game_over = True
        cursor.visible = False
        window.pop_handlers()
        window.remove_handlers(player)
        pyglet.text.Label('Bruh',
                          font_name='Dogica Pixel',
                          bold=True,
                          color=(255, 0, 0, 255),
                          font_size=36,
                          x=WINDOW_TRUE_WIDTH // 2, y=WINDOW_TRUE_HEIGHT // 2,
                          anchor_x='center', anchor_y='center', batch=foreground)
        return

    if player.x - current_scroll[0] > WINDOW_TRUE_WIDTH * 1.5 - 36:
        scroll[0] = 5 * dt * (round(current_scroll[0]) + WINDOW_TRUE_WIDTH - 36)
    elif player.x - current_scroll[0] < WINDOW_TRUE_WIDTH * 0.5:
        scroll[0] = 5 * dt * (round(current_scroll[0]))
    else:
        scroll[0] = 5 * dt * -(WINDOW_TRUE_WIDTH // 2 - round(player.x))

    scroll[1] = -5 * dt * (WINDOW_TRUE_HEIGHT // 2 - round(player.y) - 39)

    current_scroll[0] -= scroll[0]
    current_scroll[1] -= scroll[1]

    for obj in game_objects:
        obj.x -= scroll[0]
        obj.y -= scroll[1]
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
        if not any(map(lambda collision: collision[3] == Tile and collision[2], enemy_collisions)):
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
        if player.dead:
            break
        player_collisions.append(player.collision(game_objects[i]))
        if player_collisions[i - 1][0]:
            player.handle_collision_with(game_objects[i], player_collisions[i - 1][1], player_collisions[i - 1][2])
    if not player.gravity and not any(map(lambda collision: collision[2], player_collisions)):
        player.gravity = True
    if not any(map(lambda collision: collision[3] == Portal and collision[0], player_collisions)):
        player.can_proceed = False

    for obj in to_add:
        game_objects.append(obj)

    if cursor.x > window.width:
        cursor.x = window.width
    elif cursor.x < 0:
        cursor.x = 0
    if cursor.y > window.height:
        cursor.y = window.height
    elif cursor.y < 0:
        cursor.y = 0


if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1 / 165.0)
    pyglet.app.run()
