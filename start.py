import pyglet
import math
from game import player, config, map as _map

game_window = pyglet.window.Window(width=config.WINDOW_WIDTH, height=config.WINDOW_HEIGHT)


borders = [
    [90, 500],
    [750, 500],
]




current_speed = pyglet.text.Label(x=10, y=config.WINDOW_HEIGHT - 20, font_name='FreeMono')
current_vector = pyglet.text.Label(x=10, y=config.WINDOW_HEIGHT - 40, font_name='FreeMono')
current_rotation = pyglet.text.Label(x=10,y=config.WINDOW_HEIGHT - 60, font_name='FreeMono')
diff_angle = pyglet.text.Label(x=10,y=config.WINDOW_HEIGHT - 80, font_name='FreeMono')

vertex_list = pyglet.graphics.vertex_list(
    2,
    ('v2i', (10, 15, 30, 35)),
    ('c3B', (0, 0, 0, 0, 0, 0))
)

map = _map.Map([
    [81, 545], [60, 338], [68, 170], [213, 63], [376, 50], [614, 46], [797, 63], [1019, 136],
    [1049, 299], [997, 438], [848, 536], [722, 552], [580, 603], [426, 626], [286, 632], [81, 545]
])

player = player.Player(x=120, y=300, map=map)
player.rotation = 270
pyglet.clock.schedule_interval(player.update, 1/120.0)
game_window.push_handlers(player.key_handler)

# @game_window.event
# def on_mouse_press(x, y, button, modifiers):
#     map.append([x, y])


@game_window.event
def on_draw():
    # background
    pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES,
                                 [0, 1, 2, 0, 2, 3],
                                 ('v2i', (0, 0, config.WINDOW_WIDTH, 0, config.WINDOW_WIDTH, config.WINDOW_HEIGHT,
                                          0, config.WINDOW_HEIGHT)),
                                 ('c3B', [86, 176, 0] * 4))

    # debug info
    current_speed.text, current_vector.text, current_rotation.text, diff_angle.text = (
        "Speed      : %.03f" % player.speed,
        "Vector     : %.03f" % (player.current_vector * 180 / math.pi),
        "Rotation   : %.03f (%.03f)" % (-player.current_rotation * 180 / math.pi, player.rotation),
        "Diff angle : %.03f" % (player.diff_angle),
    )


    current_speed.draw()
    current_vector.draw()
    current_rotation.draw()
    diff_angle.draw()

    map.draw()
    player.draw()
    points = player.points
    # print(points)

    _map.Map(points).draw()
    map.check_colision(player)


if __name__ == '__main__':
    pyglet.app.run()
