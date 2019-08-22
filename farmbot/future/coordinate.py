class Coordinate(object):
    @staticmethod
    def home():
        return Coordinate(0, 0, 0)

    @staticmethod
    def from_tuple(xyz):
        return Coordinate(xyz[0], xyz[1], xyz[2])

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def at_max_height(self):
        return self.x, self.y, 0