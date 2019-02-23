import pyglet
import numpy as np
import math
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])


def get_intersect(a1, a2, b1, b2):
    """
    Returns the point of intersection of the lines passing through a2,a1 and b2,b1.
    a1: [x, y] a point on the first line
    a2: [x, y] another point on the first line
    b1: [x, y] a point on the second line
    b2: [x, y] another point on the second line
    """
    s = np.vstack([a1,a2,b1,b2])        # s for stacked
    h = np.hstack((s, np.ones((4, 1)))) # h for homogeneous
    l1 = np.cross(h[0], h[1])           # get first line
    l2 = np.cross(h[2], h[3])           # get second line
    x, y, z = np.cross(l1, l2)          # point of intersection
    if z == 0:                          # lines are parallel
        return float('inf'), float('inf'), False

    a = Point(*a1)
    b = Point(*a2)
    c = Point(x / z, y / z)
    d, e = Point(*b1), Point(*b2)

    # epsilon = 0.0001
    # print(f'({c.y} - {a.y}) * ({b.x} - {a.x}) - ({c.x} - {a.x}) * ({b.y} - {a.y})')
    # crossproduct = (c.y - a.y) * (b.x - a.x) - (c.x - a.x) * (b.y - a.y)

    def distance(a, b):
        return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)

    def is_between(a, c, b):
        return distance(a, c) + distance(c, b) - distance(a, b) <= 0.0001

    return [a,b,c,d,e], c.y, is_between(a, c, b) and is_between(d, c, e)


def get_lines(points):
    # for index, point in enumerate(points):
    #     lines += point
    #     if len(lines) % 4 == 0:
    #         lines += point
    lines = list(zip(*[points[i::2] for i in range(2)]))
    lines += list(zip(*[points[i + 1::2] + [points[0]] for i in range(2)]))
    return lines

class Map:
    def __init__(self, points, batch=None):
        self.points = points
        self.batch = batch
        if self.batch and len(self.points) > 1:
            lines = self.lines
            self.batch.add(
                int(len(self.lines) / 2), pyglet.gl.GL_LINES, None, ('v2i', lines)
            )

    @property
    def lines(self):
        lines = []
        for index, point in enumerate(self.points):
            lines += point
            if len(lines) % 4 == 0:
                lines += point
        return lines

    def draw(self):
        if len(self.points) > 1:
            mode = pyglet.gl.GL_LINES
            lines = self.lines
            pyglet.graphics.draw(int(len(lines) / 2), mode, ('v2i', lines))

    def check_colision(self, obj):
        map_lines = get_lines(self.points)
        obj_lines = get_lines(obj.points)

        for mline in map_lines:
            for oline in obj_lines:
                x, y, intersect = get_intersect(*mline, *oline)
                if intersect:
                    # obj.velocity_x = obj.velocity_y =0
                    mode = pyglet.gl.GL_LINES
                    pyglet.graphics.draw(2, mode, ('v2i', mline[0] + mline[1]), ('c3B', [255, 0, 0, 255, 0, 0]))
                    pyglet.graphics.draw(2, mode, ('v2i', oline[0] + oline[1]), ('c3B', [255, 0, 0, 255, 0, 0]))
                    return x, y, intersect
        return float('Inf'), float('Inf'), False
