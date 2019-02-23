import pyglet
from game import player, config, map, debug_info

game_window = pyglet.window.Window(width=config.WINDOW_WIDTH, height=config.WINDOW_HEIGHT)


main_batch = pyglet.graphics.Batch()
debug_player = debug_info.Panel(main_batch)

map1_points = [
    [60, 545], [60, 338], [68, 170], [213, 63], [376, 50], [614, 46], [797, 63], [1019, 136],
    [1149, 299], [1150, 650], [1050, 756], [722, 756], [580, 603], [426, 626], [286, 632], [60, 545]
]
map2_points = [
    [151, 281], [150, 494], [282, 560], [491, 534], [617, 528], [764, 682], [996, 678],[1072, 625],
    [1074, 322], [963, 177], [773, 109], [534, 95], [276, 115], [148, 190], [151, 281]
]

map1 = map.Map(map1_points, batch=main_batch)
map2 = map.Map(map2_points)

player = player.Player(x=100, y=300, rotation=270, batch=main_batch)

pyglet.clock.schedule_interval(player.update, 1/120.0)
game_window.push_handlers(player.key_handler)

new_points = []
@game_window.event
def on_mouse_press(x, y, button, modifiers):
    new_points.append([x, y])
    print(new_points)


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

    # map.Map(player.points).draw()
    map.Map(new_points).draw()
    map2.draw()
    _, _, collide1 = map1.check_colision(player)
    _, _, collide2 = map2.check_colision(player)
    if collide1 or collide2:
        player.restart()


if __name__ == '__main__':
    pyglet.app.run()
