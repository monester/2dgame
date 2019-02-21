import pyglet


class PhysicalObject(pyglet.sprite.Sprite):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.friction = 0.04

    def check_borders(self):
        if self.x > 800:
            self.velocity_x = 0
            self.x = 800
        elif self.x < 0:
            self.velocity_x = 0
            self.x = 0

        if self.y > 600:
            self.velocity_y = 0
            self.y = 600
        elif self.y < 0:
            self.velocity_y = 0
            self.y = 0

    def update_position(self, dt):
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt

    def check_friction(self):
        if abs(self.velocity_x) < 1 and abs(self.velocity_y) < 1:
            self.velocity_x = 0
            self.velocity_y = 0

        if self.velocity_x > 0:
            self.velocity_x *= 1.0 - self.friction

        if self.velocity_y > 0:
            self.velocity_y *= 1.0 - self.friction

    def update(self, dt):
        # print(self.velocity_x)
        # print(self.velocity_y)
        self.update_position(dt)
        self.check_borders()
        self.check_friction()
