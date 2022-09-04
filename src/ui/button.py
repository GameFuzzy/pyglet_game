import pyglet


class Button(pyglet.sprite.Sprite):

    def __init__(self, text, cursor, *args, **kwargs):
        #TODO: Make this work consistently
        pyglet.graphics.OrderedGroup(0, self.batch)
        super(Button, self).__init__(*args, **kwargs)
        self.cursor = cursor
        self.text = pyglet.text.Label(text,
                                      font_name='Dogica Pixel',
                                      bold=True,
                                      color=(255, 255, 255, 255),
                                      font_size=16,
                                      x=self.x, y=self.y,
                                      anchor_x='center', anchor_y='center', batch=self.batch)
        self.action = text
        self.hover = False
        self.pressed = False

        self.new_objects = []
        self.event_handler = self

    def left(self, x):
        return x - self.width // 2

    def right(self, x):
        return x + self.width // 2

    def top(self, y):
        return y + self.height // 2

    def bottom(self, y):
        return y - self.height // 2

    def collision(self, cursor_x, cursor_y):
        return self.left(round(self.x)) <= round(cursor_x) <= self.right(round(self.x)) and \
               self.bottom(round(self.y)) <= round(cursor_y) <= self.top(round(self.y))

    def update(self, dt):
        if self.collision(self.cursor.x, self.cursor.y):
            self.hover = True
        else:
            self.hover = False

        saturation = -self.hover * 55 + 200

        self.color = (saturation, saturation, saturation)

    def on_mouse_press(self, x, y, dx, dy):
        if self.hover:
            self.pressed = True
