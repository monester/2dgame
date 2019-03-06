import pyglet
from pyglet.window import key

from game import Player, config, Map, debug_info, Gate


game_window = pyglet.window.Window(width=config.WINDOW_WIDTH, height=config.WINDOW_HEIGHT)


main_batch = pyglet.graphics.Batch()
debug_player = debug_info.Panel(main_batch)
key_handler = key.KeyStateHandler()
game_window.push_handlers(key_handler)

from ml import Population


class Game:
    def __init__(self, maps, key_handler):
        self.score = 0
        self.player = None
        self.start_position = dict(x=190, y=550, rotation=330)
        maps = maps or []
        self.key_handler = key_handler
        self.maps = [Map(map) for map in maps]
        if len(maps) == 2:
            self.gates = Gate(maps[0], maps[1])

        # neat
        self.population = Population(
            brain=dict(target=900), player=dict(rotation=0, x=10, y=20), count=100,
        )

    def read_key(self):
        if self.key_handler[key.Q]:
            pyglet.app.event_loop.exit()

        return dict(
            left=self.key_handler[key.LEFT],
            right=self.key_handler[key.RIGHT],
            up=self.key_handler[key.UP],
            down=self.key_handler[key.DOWN],
        )

    def loop(self, dt):
        if self.player is None:
            return

        if any(map.check_colision(self.player)[2] for map in self.maps):
            self.restart()

        self.player.update(dt, **self.read_key())
        if self.gates.check_intersect(self.player):
            self.score += 10

        self.population.update(dt)

    def start(self):
        self.player = Player(batch=main_batch, **self.start_position)
        self.score = 0
        self.gates.last_checked = 0

    def restart(self):
        del self.player
        self.start()


map1_points = [
    [60, 545], [60, 338], [68, 170], [213, 63], [376, 50], [614, 46], [797, 63], [1019, 136],
    [1149, 299], [1150, 650], [1050, 756], [722, 756], [580, 603], [426, 626], [286, 632], [60, 545]
]
map2_points = [
    [151, 281], [150, 494], [282, 560], [491, 534], [617, 528], [764, 682], [996, 678],[1072, 625],
    [1074, 322], [963, 177], [773, 109], [534, 95], [276, 115], [148, 190], [151, 281]
]

game = Game([map1_points, map2_points], key_handler)
game.start()

pyglet.clock.schedule_interval(game.loop, 1/60.0)

# new_points = []
# @game_window.event
# def on_mouse_press(x, y, button, modifiers):
#     new_points.append([x, y])
#     print(new_points)


@game_window.event
def on_draw():
    # background
    pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES,
                                 [0, 1, 2, 0, 2, 3],
                                 ('v2i', (0, 0, config.WINDOW_WIDTH, 0, config.WINDOW_WIDTH, config.WINDOW_HEIGHT,
                                          0, config.WINDOW_HEIGHT)),
                                 ('c3B', [86, 176, 0] * 4))

    # debug info
    debug_player.update(game.player)

    main_batch.draw()

    # draw new line
    # Map(new_points).draw()

    # draw box
    # Map(game.player.points).draw()

    pyglet.text.Label(text=f'Score: {game.score}', x=400, y=config.WINDOW_HEIGHT - 20, font_name='FreeMono').draw()
    for map in game.maps:
        map.draw()

    [p.player.draw() for p in game.population.population]

    # draw gates
    game.gates.draw()


if __name__ == '__main__':
    pyglet.app.run()
