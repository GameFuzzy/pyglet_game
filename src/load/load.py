from entities.enemy import Enemy
from tiles.portal import Portal
from tiles import Tile
from util import resource_path


def load_map(path):
    filename = resource_path(f'data/maps/{path}.map')
    with open(filename, "r") as fp:
        return list(map(lambda line: line[:-1].split(','), reversed(fp.read().splitlines())))


def reset_map(game_objects):
    for obj in game_objects:
        if Tile in obj.__class__.__mro__ or Enemy in obj.__class__.__mro__:
            obj.delete()
    return [obj for obj in game_objects if Tile not in obj.__class__.__mro__ and Enemy not in obj.__class__.__mro__]


def change_map(tile_sprites, batch, game_map):
    tiles = []
    y = 0
    for row in game_map:
        x = 0
        for tile in row:
            if tile == 'enemy_001':
                tiles.append(Enemy(x * 16 + 16, y * 16 + 16, batch=batch))
                x += 1
            elif int(tile):
                sheet_pos = int(tile[:len(tile) // 2]), int(tile[len(tile) // 2:len(tile)])
                obj_type = Tile
                if sheet_pos == (6, 15):
                    obj_type = Portal

                tiles.append(obj_type(True, tile_sprites[sheet_pos], x * 16, y * 16, batch=batch))

            x += 1
        y += 1
    return tiles
