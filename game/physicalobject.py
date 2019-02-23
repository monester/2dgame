import pyglet
import math
from . import config


class PhysicalObject(pyglet.sprite.Sprite):

    def __init__(self, max_speed=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.max_speed = 400
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

    def update_position(self, dt):
        speed = self.speed if self.speed < self.max_speed else self.max_speed
        current_rotation = self.current_rotation
        self.velocity_x = math.cos(current_rotation) * speed
        self.velocity_y = math.sin(current_rotation) * speed
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt

    def update_friction(self, dt):
        speed = abs(self.speed)
        if speed < 2:
            self.velocity_x = 0
            self.velocity_y = 0
        elif speed > 0:
            self.velocity_x *= 1.0 - self.friction * dt
            self.velocity_y *= 1.0 - self.friction * dt

    def update(self, dt):
        self.update_position(dt)
        self.update_friction(dt)
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
        speed = math.sqrt(self.velocity_x ** 2 + self.velocity_y ** 2)
        if abs(self.diff_angle) <= 90:
            return speed
        else:
            return -speed

    @property
    def current_vector(self):
        return math.atan2(self.velocity_y, self.velocity_x)

    @property
    def current_rotation(self):
        return -math.radians(self.rotation)
