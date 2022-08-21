import rigidbody


class Tile(rigidbody.RigidBody):

    def left(self, x):
        return x

    def right(self, x):
        return x + self.width

    def top(self, y):
        return y + self.height

    def bottom(self, y):
        return y

    def handle_collision_with(self, other_object, x, y):
        return
