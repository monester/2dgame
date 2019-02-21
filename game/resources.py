import pyglet

pyglet.resource.path = ['resources']
pyglet.resource.reindex()


def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2


player_image = pyglet.resource.image("car.png", rotate=90)
center_image(player_image)
