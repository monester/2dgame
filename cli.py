from ml import Population, Player

population = Population(
    1000,
    target=type('', (), dict(x=600, y=20)),
    player=lambda: Player(rotation=0, x=20, y=20),
    maps=[],
)


for i in range(5000):
    population.update(0.05)
