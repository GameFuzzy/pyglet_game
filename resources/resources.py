import pyglet

from util import center_image

# Tell pyglet where to find the resources
pyglet.resource.path = ['resources']
pyglet.resource.reindex()

# Images
player_image = pyglet.resource.image("sprites/characters.png")

sheet_image = pyglet.resource.image("sprites/sheet.png")

swoosh_image = pyglet.resource.image("sprites/swoosh.png")
center_image(swoosh_image)

cursor_image = pyglet.resource.image("sprites/cursor.png")
center_image(cursor_image)

particle_image = pyglet.resource.image("sprites/particle.png")
center_image(particle_image)

shockwave_image = pyglet.resource.image("sprites/shockwave.png")
center_image(shockwave_image)

# Media
enemy_hit_sound = pyglet.resource.media("sfx/enemy_hit.wav", False)
ground_hit_sound = pyglet.resource.media("sfx/ground_hit.wav", False)
jump_sound = pyglet.resource.media("sfx/jump.wav", False)

# Fonts
pyglet.resource.add_font('fonts/dogicapixelbold.ttf')


