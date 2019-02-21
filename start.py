import pyglet
from pyglet.window import key
from game import player
game_window = pyglet.window.Window(width=800, height=600)

player = player.Player(x=400, y=300)
game_window.push_handlers(player.key_handler)

borders = [
    [90, 500],
    [750, 500],
]


pyglet.clock.schedule_interval(player.update, 1/20.0)


# @game_window.event
# def on_mouse_press(x, y, button, modifiers):
#     print(x, y, button, modifiers)

# @game_window.event
# def on_key_press(symbol, mods):
#     if symbol == key.Q:
#         pyglet.app.event_loop.exit()

current_speed = pyglet.text.Label(text="Speed: %s" % player.current_vector, x=10, y=585, font_name='FreeMono')
current_vector = pyglet.text.Label(text="Score: %s" % player.current_vector, x=10, y=565, font_name='FreeMono')
current_rotation = pyglet.text.Label(text="Score: %s" % player.current_rotation, x=10,y=545, font_name='FreeMono')
diff_angle = pyglet.text.Label(text="Score: %s" % player.current_rotation, x=10,y=525, font_name='FreeMono')

import math
@game_window.event
def on_draw():
    pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES,
                                 [0, 1, 2, 0, 2, 3],
                                 ('v2i', (0, 0,
                                          800, 0,
                                          800, 600,
                                          0, 600)),
                                 ('c3B', (86, 176, 0,
                                          86, 176, 0,
                                          86, 176, 0,
                                          86, 176, 0),
                                 ))
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
    pyglet.graphics.draw(2, pyglet.gl.GL_POINTS,
                         ('v2i', (10, 15, 30, 35)),
                         ('c3B', (0, 0, 255, 0, 255, 0))
                         )
    # pyglet.graphics.draw_indexed()

    player.draw()


if __name__ == '__main__':
    pyglet.app.run()
