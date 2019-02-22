import pyglet
import math
from . import config


class PhysicalObject(pyglet.sprite.Sprite):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.friction = 0.4

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
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt

    def check_friction(self, dt):
        if abs(self.speed) < 1:
            self.velocity_x = 0
            self.velocity_y = 0

        if self.velocity_x > 0:
            self.velocity_x *= 1.0 - self.friction * dt

        if self.velocity_y > 0:
            self.velocity_y *= 1.0 - self.friction * dt

    def update(self, dt):
        # print(self.velocity_x)
        # print(self.velocity_y)
        self.update_position(dt)
        self.check_borders()
        self.check_friction(dt)

    @property
    def rotate_speed(self):
        speed = abs(self.speed)
        if speed > 400:
            speed = 400
        return speed if self.speed > 0 else -speed

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
