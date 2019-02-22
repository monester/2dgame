import math
import pyglet
from pyglet.window import key
from .resources import player_image
from .physicalobject import PhysicalObject


class Player(PhysicalObject):
    def __init__(self, map, *args, **kwargs):
        super().__init__(img=player_image, *args, **kwargs)
        self.map = map
        self.dead = False
        self.thrust = 450.0
        self.key_handler = key.KeyStateHandler()
        # print(player_image.height)

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
        if speed > 400:
            speed = 400
        return speed if self.speed > 0 else -speed

    def update_position(self, dt):
        speed = self.speed
        current_vector = self.current_vector
        current_rotation = self.current_rotation
        self.velocity_x = math.cos(current_rotation) * speed
        self.velocity_y = math.sin(current_rotation) * speed

        super().update_position(dt)

    def check_track(self):
        map = self.map

        for a, b in list(zip(map[:1] + map[1:], map[1:] + map[:1])):
            pass
