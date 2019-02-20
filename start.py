import pyglet
game_window = pyglet.window.Window(width=800, height=600)

pyglet.resource.path = ['resources']
pyglet.resource.reindex()


if __name__ == '__main__':
    pyglet.app.run()
