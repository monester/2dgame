import pyglet
from game import player, config, map, debug_info

game_window = pyglet.window.Window(width=config.WINDOW_WIDTH, height=config.WINDOW_HEIGHT)


main_batch = pyglet.graphics.Batch()
debug_player = debug_info.Panel(main_batch)

map1_points = [
    [60, 545], [60, 338], [68, 170], [213, 63], [376, 50], [614, 46], [797, 63], [1019, 136],
    [1149, 299], [1150, 650], [1050, 756], [722, 756], [580, 603], [426, 626], [286, 632], [60, 545]
]
map2_points = [
    [151, 281], [150, 494], [282, 560], [491, 534], [617, 528], [764, 682], [996, 678],[1072, 625],
    [1074, 322], [963, 177], [773, 109], [534, 95], [276, 115], [148, 190], [151, 281]
]

game_score = 0


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
        obj_lines = map.get_lines(player.points)
        gate = self.gates[self.next_gate]

        gp1, gp2 = [gate[0], gate[1]], [gate[2], gate[3]]
        for obj_line in obj_lines:
            _, _, intersect = map.get_intersect(gp1, gp2, *obj_line)
            if intersect:
                self.last_checked = self.next_gate
                return True
        return False


gate = Gate(map1_points, map2_points)

map1 = map.Map(map1_points, batch=main_batch)
map2 = map.Map(map2_points)

player = player.Player(x=100, y=300, rotation=270, batch=main_batch)

pyglet.clock.schedule_interval(player.update, 1/120.0)
game_window.push_handlers(player.key_handler)

new_points = []
@game_window.event
def on_mouse_press(x, y, button, modifiers):
    new_points.append([x, y])
    print(new_points)


@game_window.event
def on_draw():
    global game_score
    # background
    pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES,
                                 [0, 1, 2, 0, 2, 3],
                                 ('v2i', (0, 0, config.WINDOW_WIDTH, 0, config.WINDOW_WIDTH, config.WINDOW_HEIGHT,
                                          0, config.WINDOW_HEIGHT)),
                                 ('c3B', [86, 176, 0] * 4))

    # debug info
    debug_player.update(player)

    main_batch.draw()

    # map.Map(player.points).draw()
    pyglet.text.Label(text=f'Score: {game_score}', x=400, y=config.WINDOW_HEIGHT - 20, font_name='FreeMono').draw()
    map.Map(new_points).draw()
    map2.draw()
    _, _, collide1 = map1.check_colision(player)
    _, _, collide2 = map2.check_colision(player)
    if collide1 or collide2:
        game_score = 0
        player.restart()

    # draw gates
    gate.draw()
    if gate.check_intersect(player):
        game_score += 10


if __name__ == '__main__':
    pyglet.app.run()
