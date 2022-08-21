from pyglet.gl import *
from pyglet.window import Window
from player import Player
from projectile import Projectile
from resources import sheet_image, cursor_image
from tile import Tile

glEnable(GL_TEXTURE_2D)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

window = Window(854, 480, resizable=True)
WINDOW_TRUE_WIDTH = 426
WINDOW_TRUE_HEIGHT = 240
window.set_exclusive_mouse(True)
glClearColor(.3, .7, 1, 1)

entities = pyglet.graphics.Batch()
player = Player(WINDOW_TRUE_WIDTH, WINDOW_TRUE_HEIGHT, batch=entities)
cursor = pyglet.sprite.Sprite(cursor_image, WINDOW_TRUE_WIDTH // 2, WINDOW_TRUE_HEIGHT // 2, batch=entities)

game_objects = [player]

for handler in player.event_handlers:
    window.push_handlers(handler)

foreground = pyglet.graphics.Batch()


def load_map(path):
    filename = path + ".map"
    with open(filename, "r") as fp:
        return list(map(lambda line: line[:-1].split(','), reversed(fp.read().splitlines())))


game_map = load_map('level1')

tiles = pyglet.image.ImageGrid(sheet_image, rows=8, columns=17)

y = 0
for row in game_map:
    x = 0
    for tile in row:
        if int(tile):
            sheet_pos = int(tile[:len(tile) // 2]), int(tile[len(tile) // 2:len(tile)])
            collidable = True
            if sheet_pos == (6, 15):
                collidable = False

            game_objects.append(Tile(collidable, tiles[sheet_pos], x * 16, y * 16, batch=foreground))
        x += 1
    y += 1

CURRENT_SCALE_WIDTH = 1
CURRENT_SCALE_HEIGHT = 1


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


@window.event
def on_mouse_motion(x, y, dx, dy):
    if 0 < cursor.x < WINDOW_TRUE_WIDTH or cursor.x >= WINDOW_TRUE_WIDTH and dx < 0 or cursor.x <= 0 and dx > 0:
        cursor.x += dx
    if 0 < cursor.y < WINDOW_TRUE_HEIGHT or cursor.y >= WINDOW_TRUE_HEIGHT and dy < 0 or cursor.y <= 0 and dy > 0:
        cursor.y += dy


@window.event
def on_mouse_press(x, y, dx, dy):
    game_objects.append(Projectile(cursor.x, cursor.y, player.x, player.y, batch=entities))


def update(dt):
    to_add = []

    for obj in game_objects:
        obj.update(dt)
        to_add.extend(obj.new_objects)
        obj.new_objects = []

    for to_remove in [obj for obj in game_objects if obj.dead]:
        to_add.extend(to_remove.new_objects)
        # Remove from batches
        to_remove.delete()
        game_objects.remove(to_remove)

    # for i in range(1, len(game_objects)):
    #     for j in range(i + 1, len(game_objects)):
    #         obj_1 = game_objects[i]
    #         obj_2 = game_objects[j]
    #         collision_1 = obj_1.collision(obj_2)
    #         collision_2 = obj_1.collision(obj_2)
    #         if collision_1[0]:
    #             obj_1.handle_collision_with(obj_2, collision_1[1], collision_1[2])
    #             obj_2.handle_collision_with(obj_1, collision_2[1], collision_2[2])

    player_collisions = []
    for i in range(1, len(game_objects)):
        player_collisions.append(player.collision(game_objects[i]))
        if player_collisions[i - 1][0]:
            player.handle_collision_with(game_objects[i], player_collisions[i - 1][1], player_collisions[i - 1][2])
    if not player.gravity and not any(map(lambda collision: collision[2], player_collisions)):
        player.gravity = True

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
    pyglet.clock.schedule_interval(update, 1 / 120.0)
    pyglet.app.run()
