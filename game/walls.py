class ComplexWall:
    def __init__(self, points):
        left_points = points
        right_points = points[1:] + [points[-1]]
        self.walls = [
            Wall(*p1, *p2)
            for p1, p2 in zip(left_points, right_points)
        ]


class Wall:
    def __init__(self, x1, y1, x2, y2):
        self.x1, self.y1 = x1, y1
        self.x2, self.y2 = x2, y2
        # self.box = [min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)]

        # pyglet.graphics.draw(2, pyglet.gl.GL_POINTS,