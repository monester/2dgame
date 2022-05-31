import math
import numpy as np


def sigmoid(x):
    return 1 / (1 + math.exp(-x))


# def func(dist, speed, params):
#     # w1 - distance to wall
#     # w2 - speed
#     # b - bias
#     # ----
#     # return 0 - accelerate, 1 - brake
#     w1 = params['w1']
#     w2 = params['w2']
#     b = params['b']
#
#     return sigmoid(dist * w1 + speed * w2 + b)


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


class Neuron:
    def __init__(self, total_args, weights=None, bias=None):
        self.weights = weights or list(map(lambda _: np.random.randn(), range(total_args)))
        self.total_args = total_args
        self.bias = bias or np.random.randn()

    def __call__(self, *args):
        sum = np.sum([
            w * value for w, value in zip(self.weights, args)
        ]) + self.bias

        return sigmoid(sum)

    def breed(self, pair, mutate=False):
        weights = [
            (n1 + n2) / 2
            for n1, n2 in zip(self.weights, pair.weights)
        ]
        if mutate:
            mutate_weight = np.random.randint(self.total_args)

            # mutate weight +- 10%
            weights[mutate_weight] += weights[mutate_weight] * np.random.rand() * 0.1

        bias = (self.bias + pair.bias) / 2
        return Neuron(self.total_args, weights, bias)


class Brain:
    def __init__(self, target, player, neurons=None):
        self.neurons = neurons or [Neuron(3), Neuron(3), Neuron(3), Neuron(3)]
        self.player = player
        self.target = target

    def __call__(self):
        dist = (self.target.x - self.player.x) / 1200  # max width
        car_angle = math.atan2(self.player.velocity_y, self.player.velocity_x)
        target_angle = math.atan2(self.target.y - self.player.y, self.target.x - self.player.x)
        # print(car_angle - target_angle, car_angle, target_angle)

        speed = self.player.speed / 450      # max speed
        actions = {}
        for index, action in enumerate(['up', 'down', 'left', 'right']):
            actions[action] = self.neurons[index](dist, speed, car_angle - target_angle) > 0.7

        resp = dict(**actions)
        return resp

    def __getattr__(self, item):
        return self.params[item]

    def update(self, dt):
        keys = self()
        self.player.update(dt, **keys)

    def breed(self, pair, count=10):
        new_species = []
        for _ in range(count):
            mutate_neuron = np.random.randint(len(self.neurons))
            new_neurons = [
                neuron.breed(pair.neurons[i], mutate=mutate_neuron == i)
                for i, neuron in enumerate(self.neurons)
            ]
            new_species.append(new_neurons)
        return new_species

    @property
    def fitness(self):
        if self.player.dead:
            return float('inf')
        distance = math.sqrt((self.target.x - self.player.x) ** 2 + (self.target.y - self.player.y) ** 2)
        return distance + abs(self.player.speed * 2)

    def __repr__(self):
        brain = f"fitness={self.fitness:.2f}" # ' w1={self.w1:.2f} w2={self.w2:.2f} b={self.b:.2f}"
        player = f"x: {self.player.x} y: {self.player.y} speed: {self.player.speed}"
        return f"{brain:20s} {player:40s}"


class Population:
    def __init__(self, count, target, player, maps):
        self.target = target
        self.player = player
        self.maps = maps
        self.alive = []
        self.population = [Brain(target=self.target, player=player()) for _ in range(count)]
        self.generation = 0
        self.count = count
        self.tick = 0

    @property
    def population(self):
        return self._population

    @population.setter
    def population(self, value):
        self._population = value
        self.alive = list(value)

    def update(self, dt):
        self.tick += 1
        for i in self.alive[:]:
            i.update(dt)

            # if any(map.check_colision(i.player)[2] for map in self.maps):
            #     i.player.dead = True

            if i.player.dead:
                self.alive.remove(i)

        if len(self.alive) == 0 or self.tick % 100 == 0:
            self.population.sort(key=lambda x: x.fitness)
            self.generation += 1
            print('-'*80, f'Generation: {self.generation}: Survived: {len(self.alive)}')

            new_population = []
            # keep 3 most performant
            for p in self.population[:3]:
                print('COPY  | %50r |' % p)
                new_population.append(Brain(target=self.target, player=self.player(), neurons=p.neurons))

            # breed 1-17 and 3-20 most performant
            for s1, s2 in zip(self.population[:17], self.population[3:20]):
                print('MERGE | %50r | %50r |' % (s1, s2))

                new_population.extend(
                    Brain(target=self.target, player=self.player(), neurons=neurons)
                    for neurons in s1.breed(s2, count=int(self.count / 17))
                )
            self.population = new_population

    def __repr__(self):
        return f"Alive: {len(self.alive)} Gen: {self.generation} Tick: {self.tick}"

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
