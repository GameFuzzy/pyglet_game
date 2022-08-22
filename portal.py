from tile import Tile


class Portal(Tile):
    def __init__(self, *args, **kwargs):
        super(Portal, self).__init__(*args, **kwargs)
        self.collidable = False
