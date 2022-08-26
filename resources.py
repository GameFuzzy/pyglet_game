import pyglet
from util import center_image

# Tell pyglet where to find the resources
pyglet.resource.path = ['resources']
pyglet.resource.reindex()

# Load the three main resources and get them to draw centered
player_image = pyglet.resource.image("characters.png")

sheet_image = pyglet.resource.image("sheet.png")

swoosh_image = pyglet.resource.image("swoosh.png")
center_image(swoosh_image)

cursor_image = pyglet.resource.image("cursor.png")
center_image(cursor_image)

particle_image = pyglet.resource.image("particle.png")
center_image(particle_image)
