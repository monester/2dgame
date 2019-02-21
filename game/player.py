import math
import pyglet
from pyglet.window import key
from .resources import player_image
from .physicalobject import PhysicalObject


class Player(PhysicalObject):
    def __init__(self, *args, **kwargs):
        super().__init__(img=player_image, *args, **kwargs)
        self.thrust = 450.0
        self.key_handler = key.KeyStateHandler()

    def update(self, dt):
        super().update(dt)
        if self.key_handler[key.LEFT]:
            self.rotation -= self.rotate_speed * dt
        if self.key_handler[key.RIGHT]:
            self.rotation += self.rotate_speed * dt
        if self.key_handler[key.UP] or self.key_handler[key.DOWN]:
            thrust = self.thrust if self.key_handler[key.UP] else -self.thrust / 3
            angle_radians = -math.radians(self.rotation)
            force_x = math.cos(angle_radians) * thrust * dt
            force_y = math.sin(angle_radians) * thrust * dt
            self.velocity_x += force_x
            self.velocity_y += force_y

        if self.key_handler[key.Q]:
            pyglet.app.event_loop.exit()

    @property
    def rotate_speed(self):
        speed = abs(self.speed)
        if speed > 100:
            speed = 100
        return speed

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

    def update_position(self, dt):
        speed = self.speed
        current_vector = self.current_vector
        current_rotation = self.current_rotation
        self.velocity_x = math.cos(current_rotation) * speed
        self.velocity_y = math.sin(current_rotation) * speed

        super().update_position(dt)
