import pyglet
import math
from . import config


class PhysicalObject(pyglet.sprite.Sprite):
    def __init__(self, frame_rate, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.frame_rate = frame_rate
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self._speed = 0.0
        self.max_speed = config.MAX_CAR_SPEED
        self.friction = config.FRICTION

    @property
    def points(self):
        points = list(self._vertex_list.vertices)
        points = list(zip(*[points[i::2] for i in range(2)]))
        return points

    def check_borders(self):
        if self.x > config.WINDOW_WIDTH:
            self.velocity_x = 0
            self.x = config.WINDOW_WIDTH
        elif self.x < 0:
            self.velocity_x = 0
            self.x = 0

        if self.y > config.WINDOW_HEIGHT:
            self.velocity_y = 0
            self.y = config.WINDOW_HEIGHT
        elif self.y < 0:
            self.velocity_y = 0
            self.y = 0

    def update_position(self):
        current_rotation = self.current_rotation
        velocity_x = math.cos(current_rotation) * self.speed
        velocity_y = math.sin(current_rotation) * self.speed
        self.x += velocity_x / self.frame_rate
        self.y += velocity_y / self.frame_rate

    def update_friction(self):
        self.speed *= 1 - self.friction

        if abs(self.speed) < 4:
            self.speed = 0

    def update(self):
        self.update_position()
        self.update_friction()
        self.check_borders()

    @property
    def diff_angle(self):
        a = self.current_vector
        b = self.current_rotation
        a = a * 180 / math.pi
        b = b * 180 / math.pi
        r = (b - a) % 360.0
        if r >= 180.0:
            r -= 360.0
        return r

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, speed):
        if speed > 0 and speed > self.max_speed:
            self._speed = self.max_speed
        elif speed < 0 and speed < -self.max_speed:
            self._speed = -self.max_speed
        else:
            self._speed = speed

    @property
    def current_vector(self):
        return math.atan2(self.velocity_y, self.velocity_x)

    @property
    def current_rotation(self):
        return -math.radians(self.rotation)
