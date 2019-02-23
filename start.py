import pyglet
from game import player, config, map as _map, debug_info

game_window = pyglet.window.Window(width=config.WINDOW_WIDTH, height=config.WINDOW_HEIGHT)


main_batch = pyglet.graphics.Batch()
debug_player = debug_info.Panel(main_batch)

map = _map.Map([
    [81, 545], [60, 338], [68, 170], [213, 63], [376, 50], [614, 46], [797, 63], [1019, 136],
    [1049, 299], [997, 438], [848, 536], [722, 552], [580, 603], [426, 626], [286, 632], [81, 545]
], batch=main_batch)

player = player.Player(x=120, y=300, rotation=270, batch=main_batch)

pyglet.clock.schedule_interval(player.update, 1/120.0)
game_window.push_handlers(player.key_handler)

# @game_window.event
# def on_mouse_press(x, y, button, modifiers):
#     map.append([x, y])


@game_window.event
def on_draw():
    # background
    pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES,
                                 [0, 1, 2, 0, 2, 3],
                                 ('v2i', (0, 0, config.WINDOW_WIDTH, 0, config.WINDOW_WIDTH, config.WINDOW_HEIGHT,
                                          0, config.WINDOW_HEIGHT)),
                                 ('c3B', [86, 176, 0] * 4))

    # debug info
    debug_player.update(player)

    main_batch.draw()

    # _map.Map(player.points).draw()
    _, _, collide = map.check_colision(player)
    if collide:
        player.restart()


if __name__ == '__main__':
    pyglet.app.run()
