import math
import math
from .resources import player_image
from . import config
from .physicalobject import PhysicalObject

UP, DOWN, LEFT, RIGHT = 0x1, 0x2, 0x4, 0x8


class Player(PhysicalObject):
    def __init__(self, rotation, frame_rate, *args, **kwargs):
        super().__init__(img=player_image, frame_rate=frame_rate, *args, **kwargs)
        self.scale = 0.5
        self.start_position = kwargs['x'], kwargs['y'], rotation
        self.rotation = rotation
        self.dead = False
        self.frame_rate = frame_rate
        self._thrust = config.CAR_THRUST
        self._max_rotation_speed = config.MAX_CAR_ROTATION_SPEED

    @property
    def thrust(self):
        return self._thrust

    @property
    def max_rotation_speed(self):
        return self._max_rotation_speed

    def update(self, keys: int) -> None:
        if self.dead:
            return
        super().update()

        left = keys & LEFT
        right = keys & RIGHT
        up = keys & UP
        down = keys & DOWN

        if left:
            self.rotation -= self.rotate_speed

        if right:
            self.rotation += self.rotate_speed

        if up:
            self.speed += self.thrust

        if down:
            self.speed -= self.thrust

        if self.x == 0 or self.x == config.WINDOW_WIDTH or self.y == 0 or self.y == config.WINDOW_HEIGHT:
            # print("DEAD - collide with wall")
            self.dead = True

    @property
    def rotate_speed(self):
        rotate_speed = abs(self.speed)
        if rotate_speed > self.max_rotation_speed:
            rotate_speed = self.max_rotation_speed
        return rotate_speed / self.frame_rate

    def __repr__(self):
        return f"<Player: x: {self.x} y: {self.y} speed: {self.speed}>"
