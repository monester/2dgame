import math
import pyglet
from pyglet.window import key
from .resources import player_image
from . import config
from .physicalobject import PhysicalObject


class Player(PhysicalObject):
    def __init__(self, rotation, *args, **kwargs):
        super().__init__(img=player_image, *args, **kwargs)
        self.start_position = kwargs['x'], kwargs['y'], rotation
        self.rotation = rotation
        self.dead = False
        self.thrust = config.CAR_THRUST
        self.max_rotation_speed = config.MAX_CAR_ROTATION_SPEED
        self.key_handler = key.KeyStateHandler()

    def update(self, dt):
        super().update(dt)
        if self.key_handler[key.LEFT]:
            self.rotation -= self.rotate_speed * dt
        if self.key_handler[key.RIGHT]:
            self.rotation += self.rotate_speed * dt
        if self.key_handler[key.UP] or self.key_handler[key.DOWN]:
            if self.key_handler[key.UP]:
                # move forward
                if self.speed >= 0:
                    thrust = self.thrust
                else:
                    thrust = self.thrust * 1.5  # car is slowing
            else:
                # move backward
                if self.speed <= 0:
                    thrust = -self.thrust / 3
                else:
                    thrust = -self.thrust * 1.5  # car is slowing
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
        if speed > self.max_rotation_speed:
            speed = self.max_rotation_speed
        return speed if self.speed > 0 else -speed

    def restart(self):
        self.x, self.y, self.rotation = self.start_position
        self.velocity_x = self.velocity_y = 0
