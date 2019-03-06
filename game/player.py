import math
from .resources import player_image
from . import config
from .physicalobject import PhysicalObject


class Player(PhysicalObject):
    def __init__(self, rotation, *args, **kwargs):
        super().__init__(img=player_image, *args, **kwargs)
        self.scale = 0.5
        self.start_position = kwargs['x'], kwargs['y'], rotation
        self.rotation = rotation
        self.dead = False
        self.thrust = config.CAR_THRUST
        self.max_rotation_speed = config.MAX_CAR_ROTATION_SPEED

    def update(self, dt, left=False, right=False, up=False, down=False):
        if self.dead:
            return
        super().update(dt)
        if left:
            self.rotation -= self.rotate_speed * dt
        if right:
            self.rotation += self.rotate_speed * dt
        if up or down:
            if up:
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

        if self.x == 0 or self.x == config.WINDOW_WIDTH:
            self.dead = True

    @property
    def rotate_speed(self):
        speed = abs(self.speed)
        if speed > self.max_rotation_speed:
            speed = self.max_rotation_speed
        return speed if self.speed > 0 else -speed

    def __repr__(self):
        return f"<Player: x: {self.x} y: {self.y} speed: {self.speed}>"
