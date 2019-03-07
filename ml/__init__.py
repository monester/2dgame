import numpy as np


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def func(dist, speed, params):
    # w1 - distance to wall
    # w2 - speed
    # b - bias
    # ----
    # return 0 - accelerate, 1 - brake
    w1 = params['w1']
    w2 = params['w2']
    b = params['b']

    return sigmoid(dist * w1 + speed * w2 + b)


# data = [
#     [2, 1, 0],
#     [3, 1, 0],
#     [2, .5, 0],
#     [1, 1, 0],
#     [3, 1.5, 1],
#     [3.5, .5, 1],
#     [4, 1.5, 1],
#     [5.5, 1, 1],
# ]
#
# from random import random
#
#
# def train():
#     w1 = random()
#     w2 = random()
#     b = random()
#     learning_rate = .02
#     for i in range(50000):
#         flower = data[i % len(data)]
#         l, w, target = flower
#
#         # prediction
#         pred = func(dist=l, speed=w, params=dict(w1=w1, w2=w2, b=b))
#         cost = (pred - target) ** 2
#         if i % 400000 == 0:
#             print(cost)
#
#         dcost_dpred = 2 * (pred - target)
#         dpred_dz = pred * (1 - pred)
#
#         dz_dw1 = l
#         dz_dw2 = w
#
#         dcost_dw1 = dcost_dpred * dpred_dz * dz_dw1
#         dcost_dw2 = dcost_dpred * dpred_dz * dz_dw2
#         dcost_db = dcost_dpred * dpred_dz * 1
#
#         w1 -= learning_rate * dcost_dw1
#         w2 -= learning_rate * dcost_dw2
#         b -= learning_rate * dcost_db
#     return {'w1': w1, 'w2': w2, 'b': b}
#
#
# p = train()
#
# from functools import partial
# func = partial(func, params=p)
#
# for i in data:
#     print('[%.1f, %.1f, %.1f] = %0.9f' % (*i, func(dist=i[0], speed=i[1])))


from game.player import Player
# p = Player(0, x=1, y=1)


class Brain:
    def __init__(self, target, player, params=None):
        self.params = params or dict(
            w1=np.random.randn(),
            w2=np.random.randn(),
            b=np.random.randn(),
        )
        self.player = player
        self.target = target
        self.ticks = 0

    def __call__(self):
        dist = (self.target - self.player.x) / 1200  # max width
        speed = self.player.speed / 450      # max speed

        r = func(dist=dist, speed=speed, params=self.params)
        resp = dict(up=r > 0.52, down=r<0.48)
        # print(resp)
        return resp

    def __getattr__(self, item):
        return self.params[item]

    def update(self, dt):
        self.ticks += 1
        if self.ticks == 100:
            self.player.dead = True
        keys = self()
        self.player.update(dt, **keys)

    @property
    def fitness(self):
        if self.player.x in [1200, 0]:
            return float('inf')
        # if self.player.dead:
        #     return float('inf')
        return abs(self.target - self.player.x) + abs(self.player.speed * 2)

    def __repr__(self):
        brain = f"fitness={self.fitness:.2f} w1={self.w1:.2f} w2={self.w2:.2f} b={self.b:.2f}"
        player = f"x: {self.player.x} speed: {self.player.speed}"
        return f"{brain:40s} {player:40s}"


class Population:
    def __init__(self, count, target, player, maps):
        self.target = target
        self.player = player
        self.maps = maps
        population = [Brain(target=self.target, player=player()) for _ in range(count)]
        self.alive = list(population)
        self.population = population
        self.generation = 0

    def update(self, dt):
        for i in self.alive[:]:
            i.update(dt)

            # if any(map.check_colision(i.player)[2] for map in self.maps):
            #     i.player.dead = True

            if i.player.dead:
                self.alive.remove(i)

        if len(self.alive) == 0:
            self.population.sort(key=lambda x: x.fitness)
            new_population = []
            print('-'*80, 'Generation: %s' % self.generation)
            self.generation += 1
            for p in self.population[0:10]:
                print(repr(p))
                for _ in range(10):
                    params = {}
                    mutate = np.random.randint(3)
                    for i, (k, v) in enumerate(p.params.items()):
                        if i == mutate:
                            if v != 0:
                                params[k] = v + v * np.random.randn() / 10
                            else:
                                params[k] = np.random.randn() / 10
                        else:
                            params[k] = v

                    new_population.append(Brain(target=self.target, player=self.player(), params=params))
            self.population = new_population
            self.alive = list(self.population)




# population = [
#     Brain(target=300, player=Player(0, x=1, y=1))
#     for i in range(100)
# ]
# for i in range(100):  # 10 sec
#     for brain in population:
#         brain.update(0.1)
#
#
# population.sort(key=lambda x: x.fitness)
# for p in population[0:10]:
#     print(repr(p))
#
# new_population = []
# for p in population[0:10]:
#     for _ in range(100):
#         params = {}
#         mutate = np.random.randint(3)
#         for i, (k, v) in enumerate(p.params.items()):
#             if i == mutate:
#                 if v != 0:
#                     params[k] = v + v * np.random.randn() / 10
#                 else:
#                     params[k] = np.random.randn() / 10
#             else:
#                 params[k] = v
#
#         new_population.append(Brain(target=300, player=Player(0, x=1, y=1), params=params))
#
#
# population = new_population
# for i in range(250):  # 10 sec
#     for brain in population:
#         brain.player.update(0.01, **brain())
#
#
# population.sort(key=lambda x: x.fitness)
# for p in population[0:10]:
#     print(repr(p))

# [p[0].x for p in population]
# [p[1].w1 for p in population]
