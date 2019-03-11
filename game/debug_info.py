import math
import pyglet
from . import config


class Panel:
    def __init__(self, batch):
        self.batch = batch
        self.labels = []

    def text(self, *items):
        if len(self.labels) != len(items):
            for i in range(len(self.labels), len(items)):
                x = 10
                y = config.WINDOW_HEIGHT - (20 * (i + 1))
                self.labels.append(pyglet.text.Label(x=x, y=y, font_name='FreeMono', batch=self.batch))
        for label, value in zip(self.labels, items):
            label.text = value

    def update(self, player, population):
        current_rotation = (player.current_rotation + math.pi) % (math.pi*2) - math.pi

        self.text(
            "Speed      : %.03f" % player.speed,
            "Vector     : %.03f" % (player.current_vector * 180 / math.pi),
            "Rotation   : %.03f (%.03f)" % (
                current_rotation,
                player.rotation,
            ),
            "Diff angle : %.03f" % (player.diff_angle),
            "Population : %s" % repr(population)
        )
