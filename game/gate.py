import pyglet
from .map import get_intersect, get_lines


def calc_dist(x1, y1, x2, y2):
    return (x1 - x2) ** 2 + (y1 - y2) ** 2


class Gate:
    def __init__(self, map1_points, map2_points):
        self.last_checked = 0
        self.gates = []
        for p1 in reversed(map1_points):
            min_point = map2_points[0]
            min_distance = calc_dist(*p1, *min_point)
            for p2 in map2_points:
                dist = calc_dist(*p1, *p2)
                if dist < min_distance:
                    min_distance = dist
                    min_point = p2
            self.gates.append(p1 + min_point)

    @property
    def next_gate(self):
        next_gate = self.last_checked + 1
        if next_gate == len(self.gates):
            next_gate = 0
        return next_gate

    def draw(self):
        for i, gate in enumerate(self.gates):
            if i == self.next_gate:
                color = [255, 255, 0, 255, 255, 0]
            else:
                color = [255, 0, 0, 255, 0, 0]
            pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2i', gate), ('c3B', color))

    def check_intersect(self, player):
        obj_lines = get_lines(player.points)
        gate = self.gates[self.next_gate]

        gp1, gp2 = [gate[0], gate[1]], [gate[2], gate[3]]
        for obj_line in obj_lines:
            _, _, intersect = get_intersect(gp1, gp2, *obj_line)
            if intersect:
                self.last_checked = self.next_gate
                return True
        return False
