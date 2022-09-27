import math
import os
import sys
from datetime import datetime


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def distance(point_1=(0, 0), point_2=(0, 0)):
    """Returns the distance between two points"""
    return math.sqrt((point_1[0] - point_2[0]) ** 2 + (point_1[1] - point_2[1]) ** 2)


def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width / 2
    image.anchor_y = image.height / 2


# TODO: Get rid of this since it is excruciatingly slow. Could be replaced with an inherent color property for each tile.
def get_pixel_region(image, x, y, width, height):
    t = datetime.now()
    img_data = image.get_region(x, y, width, height).get_image_data()
    print('get_region:', (datetime.now() - t).microseconds, 'microseconds')
    width = img_data.width
    t = datetime.now()
    data = img_data.get_data('RGB', 3 * width)
    print('get_data:', (datetime.now() - t).microseconds, 'microseconds')
    return [(data[i], data[i + 1], data[i + 2]) for i in range(0, len(data), 3)]
