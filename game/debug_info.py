import math
import pyglet
from . import config


class Panel:
    def __init__(self, batch):
        self.current_speed = pyglet.text.Label(x=10, y=config.WINDOW_HEIGHT - 20, font_name='FreeMono', batch=batch)
        self.current_vector = pyglet.text.Label(x=10, y=config.WINDOW_HEIGHT - 40, font_name='FreeMono', batch=batch)
        self.current_rotation = pyglet.text.Label(x=10, y=config.WINDOW_HEIGHT - 60, font_name='FreeMono', batch=batch)
        self.diff_angle = pyglet.text.Label(x=10, y=config.WINDOW_HEIGHT - 80, font_name='FreeMono', batch=batch)

    def update(self, player):
        self.current_speed.text, self.current_vector.text, self.current_rotation.text, self.diff_angle.text = (
            "Speed      : %.03f" % player.speed,
            "Vector     : %.03f" % (player.current_vector * 180 / math.pi),
            "Rotation   : %.03f (%.03f)" % (-player.current_rotation * 180 / math.pi, player.rotation),
            "Diff angle : %.03f" % (player.diff_angle),
        )
