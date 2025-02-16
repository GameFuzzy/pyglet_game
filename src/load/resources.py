import pyglet
from util import center_image, resource_path

# Tell pyglet where to find the data
pyglet.resource.path = [resource_path('data/resources')]
pyglet.resource.reindex()

# Images
player_image = pyglet.resource.image('sprites/characters.png')

sheet_image = pyglet.resource.image('sprites/sheet.png')

health_image = pyglet.resource.image('sprites/health.png')

swoosh_image = pyglet.resource.image('sprites/swoosh.png')
center_image(swoosh_image)

cursor_image = pyglet.resource.image('sprites/cursor.png')
center_image(cursor_image)

particle_image = pyglet.resource.image('sprites/particle.png')
center_image(particle_image)

shockwave_image = pyglet.resource.image('sprites/shockwave.png')
center_image(shockwave_image)

button_01_image = pyglet.resource.image('sprites/button-01.png')
center_image(button_01_image)

# Media
player_hit_sound = pyglet.resource.media('sfx/player_hit.wav', False)
enemy_hit_sound = pyglet.resource.media('sfx/enemy_hit.wav', False)
ground_hit_sound = pyglet.resource.media('sfx/ground_hit.wav', False)
jump_sound = pyglet.resource.media('sfx/jump.wav', False)
bgm = pyglet.resource.media('sfx/bgm.wav', False)

# Fonts
pyglet.resource.add_font('fonts/dogicapixelbold.ttf')


