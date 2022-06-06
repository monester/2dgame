import datetime

import pyglet
from typing import Optional
from pyglet.window import key

from game import Player, config, Map, debug_info, Gate
from game.player import LEFT, RIGHT, UP, DOWN

game_window = pyglet.window.Window(width=config.WINDOW_WIDTH, height=config.WINDOW_HEIGHT)

main_batch = pyglet.graphics.Batch()
debug_player = debug_info.Panel(main_batch)
key_handler = key.KeyStateHandler()
game_window.push_handlers(key_handler)

from ml import Population

# pyglet schedule_interval doesn't support more than 60Hz
FRAME_RATE = 60.0
assert FRAME_RATE <= 60.0


class Neat:
    def __init__(self):
        self.target = type('', (), dict(x=600, y=20))
        self.population = Population(
            target=self.target,
            player=lambda: Player(rotation=0, frame_rate=FRAME_RATE, x=20, y=20),
            maps=None,  # self.maps,
            count=1000,
        )

    def step(self, dt):
        self.population.update()

count = 0
last_sec = 0
class Game:
    def __init__(self, maps, key_handler, start_position):
        self.score = 0
        self.player: Optional[Player] = None
        self.draw = False
        # self.start_position = dict(x=190, y=550, rotation=-30)
        # self.start_position = dict(x=0, y=800, rotation=0)
        self.start_position = start_position
        maps = maps or []
        self.key_handler = key_handler
        self.maps = [Map(map) for map in maps]
        if len(maps) == 2:
            self.gates = Gate(maps[0], maps[1])

    def read_key(self) -> int:
        if self.key_handler[key.Q]:
            pyglet.app.event_loop.exit()
        if self.key_handler[key.D]:
            self.draw = not self.draw

        keys = sum([
            RIGHT if self.key_handler[key.RIGHT] else 0,
            LEFT if self.key_handler[key.LEFT] else 0,
            DOWN if self.key_handler[key.DOWN] else 0,
            UP if self.key_handler[key.UP] else 0,
        ])

        return keys

    def loop(self, dt):
        if self.player is None:
            return

        # if any(map.check_colision(self.player)[2] for map in self.maps):
        #     self.restart()

        self.player.update(self.read_key())
        if self.gates.check_intersect(self.player):
            self.score += 10

    def start(self):
        self.player = Player(batch=main_batch, frame_rate=FRAME_RATE, **self.start_position)
        self.score = 0
        self.gates.last_checked = 0

    def restart(self):
        del self.player
        self.start()


@game_window.event
def on_mouse_press(x, y, button, modifiers):
    # new_points.append([x, y])
    print("NEW TARGET: %s" % x)
    # game.population.target = type('', (), dict(x=x, y=y))


mouse = type('Mouse', (), {'x': 0, 'y': 0})()


@game_window.event
def on_mouse_motion(x, y, dx, dy):
    mouse.x, mouse.y = x, y


@game_window.event
def on_draw():
    # background
    pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES,
                                 [0, 1, 2, 0, 2, 3],
                                 ('v2i', (0, 0, config.WINDOW_WIDTH, 0, config.WINDOW_WIDTH, config.WINDOW_HEIGHT,
                                          0, config.WINDOW_HEIGHT)),
                                 ('c3B', [86, 176, 0] * 4))

    # debug info
    debug_player.update(game)
    pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', [
        mouse.x - 20, mouse.y - 20,
        mouse.x + 20, mouse.y - 20,
        mouse.x + 20, mouse.y + 20,
        mouse.x - 20, mouse.y + 20,
    ]))

    main_batch.draw()

    # draw new line
    # Map(new_points).draw()

    # draw box
    # Map(game.player.points).draw()

    pyglet.text.Label(text=f'Score: {game.score}', x=400, y=config.WINDOW_HEIGHT - 20, font_name='FreeMono').draw()
    for map in game.maps:
        map.draw()

    [p.player.draw() for p in neat.population.population[0:100]]

    # draw gates
    game.gates.draw()


if __name__ == '__main__':
    map1_points = [
        [60, 545], [60, 338], [68, 170], [213, 63], [376, 50], [614, 46], [797, 63], [1019, 136],
        [1149, 299], [1150, 650], [1050, 756], [722, 756], [580, 603], [426, 626], [286, 632], [60, 545]
    ]
    map2_points = [
        [151, 281], [150, 494], [282, 560], [491, 534], [617, 528], [764, 682], [996, 678], [1072, 625],
        [1074, 322], [963, 177], [773, 109], [534, 95], [276, 115], [148, 190], [151, 281]
    ]

    game = Game([map1_points, map2_points], key_handler, dict(x=190, y=550, rotation=-30))
    # game = Game([map1_points, map2_points], key_handler, dict(x=0, y=800, rotation=0))
    game.start()

    neat = Neat()

    # def benchmark(dt):
    #     global count, last_sec
    #     dt = datetime.datetime.now()
    #     if last_sec != dt.second:
    #         print(f"count={count}")
    #         count = 0
    #         last_sec = dt.second
    #     count += 1
    #     pyglet.clock.schedule_interval(benchmark, 1/120)
    #
    # pyglet.clock
    # pyglet.clock.schedule_interval(benchmark,1/120)

    pyglet.clock.schedule_interval(game.loop, 1 / FRAME_RATE)
    # pyglet.clock.schedule_interval(neat.step, 1 / 60.0)

    new_points = []

    pyglet.app.run()
