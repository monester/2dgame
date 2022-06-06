import pyglet
import math
from .resources import player_image
from . import config

UP, DOWN, LEFT, RIGHT = 0x1, 0x2, 0x4, 0x8


class Player(pyglet.sprite.Sprite):
    def __init__(self, rotation, frame_rate, *args, **kwargs):
        super().__init__(img=player_image, *args, **kwargs)
        self.scale = 0.5
        self.start_position = kwargs['x'], kwargs['y'], rotation
        self.rotation = rotation
        self.dead = False
        self.frame_rate = frame_rate
        self.thrust = config.CAR_THRUST
        self.max_rotation_speed = config.MAX_CAR_ROTATION_SPEED
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self._speed = 0.0
        self._acceleration = 0.0
        self.max_speed = config.MAX_CAR_SPEED
        self.friction = config.FRICTION

    @property
    def acceleration(self):
        return self._acceleration

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

    @property
    def points(self):
        points = list(self._vertex_list.vertices)
        points = list(zip(*[points[i::2] for i in range(2)]))
        return points

    def update(self, keys: int) -> None:
        if self.dead:
            return
        left = keys & LEFT
        right = keys & RIGHT
        up = keys & UP
        down = keys & DOWN

        self.update_position()
        self.update_friction(up)
        self.check_borders()

        if left:
            self.rotation -= self.rotate_speed / self.frame_rate

        if right:
            self.rotation += self.rotate_speed / self.frame_rate

        if up:
            self.speed += self.thrust / self.frame_rate

        if down:
            self.speed -= self.thrust / self.frame_rate

        if self.x == 0 or self.x == config.WINDOW_WIDTH or self.y == 0 or self.y == config.WINDOW_HEIGHT:
            # print("DEAD - collide with wall")
            self.dead = True

    @property
    def rotate_speed(self):
        rotate_speed = abs(self.speed)
        if rotate_speed > self.max_rotation_speed:
            rotate_speed = self.max_rotation_speed
        return rotate_speed

    def __repr__(self):
        return f"<Player: x: {self.x} y: {self.y} speed: {self.speed}>"

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
        self._speed += self.acceleration / self.frame_rate
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

    def update_position(self):
        current_rotation = self.current_rotation
        velocity_x = math.cos(current_rotation) * self.speed
        velocity_y = math.sin(current_rotation) * self.speed
        self.x += velocity_x / self.frame_rate
        self.y += velocity_y / self.frame_rate

    def update_friction(self, up):
        self.speed *= 1 - self.friction / self.frame_rate

        if abs(self.speed) < 4 and not up:
            self.speed = 0
