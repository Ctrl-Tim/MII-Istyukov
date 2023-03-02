from collections import namedtuple
from functools import partial
from typing import List, Callable, Tuple
from random import choices, randint, randrange, random

Genome = List[int]
Population = List[Genome]
FitnessFunc = Callable[[Genome], int]
PopulateFunc = Callable[[], Population]
SelectionFunc = Callable[[Population, FitnessFunc], Tuple[Genome, Genome]]
CrossoverFunc = Callable[[Genome, Genome], Tuple[Genome, Genome]]
MutationFunc = Callable[[Genome], Genome]
City = namedtuple('City', ['name', 'value', 'distance'])
y = 3000

cities = [
    City('Ульяновск', 617, 10),
    City('Димитровград', 113, 91),
    City('Сызрань', 165, 140),
    City('Тольятти', 684, 197),
    City('Казань', 1257, 206),
    City('Саранск', 314, 232),
    City('Чебоксары', 508, 240),
    City('Самара', 1173, 248),
    City('Пенза', 522, 318),
    City('Нижний Новгород', 1253, 475)
]

def generate_genome(length: int) -> Genome:
    return choices([0, 1], k=length)


def generate_population(size: int, genome_length: int) -> Population:
    return [generate_genome(genome_length) for _ in range(size)]

def fitness(genome: Genome, cities: [City], value_limit: int, distance_limit: int) -> int:
    if len(genome) != len(cities):
        raise ValueError("genom и cities должны быть одинаковой длины!")
    value = 0
    distance = 0
    for i, city in enumerate(cities):
        if genome[i] == 1:
            value += city.value
            distance += city.distance
            if distance > distance_limit or value*1.1 > value_limit:
                return 0
    return value

def selection_pair(population: Population, fitness_func: FitnessFunc) -> Population:
    return choices(
        population=population,
        weights=[fitness_func(genome) for genome in population],
        k=2
    )

def single_point_crossover(a: Genome, b: Genome) -> Tuple[Genome, Genome]:
    if len(a) != len(b):
        raise ValueError("Геномы a и b должны быть одинаковой длины!")
    length = len(a)
    if length < 2:
        return a, b
    p = randint(1, length-1)
    return a[0:p] + b[p:], b[0:p] + a[p:]

def mutation(genome: Genome, num: int = 1, probability: float = 0.5) -> Genome:
    for _ in range(num):
        index = randrange(len(genome))
        genome[index] = genome[index] if random() > probability else abs(genome[index]-1)
    return genome

def run_evolution(
        populate_func: PopulateFunc,
        fitness_func: FitnessFunc,
        fitness_limit: int,
        selection_func: SelectionFunc = selection_pair,
        crossover_func: CrossoverFunc = single_point_crossover,
        mutation_func: MutationFunc = mutation,
        generation_limit: int = 100
) -> Tuple[Population, int]:
    population = populate_func()
    for i in range(generation_limit):
        population = sorted(
            population,
            key=lambda genome: fitness_func(genome),
            reverse=True
        )
        if fitness_func(population[0]) >= fitness_limit:
            break
        next_generation = population[0:2]
        for j in range(int(len(population) / 2) - 1):
            parents = selection_func(population, fitness_func)
            offspring_a, offspring_b = crossover_func(parents[0], parents[1])
            offspring_a = mutation_func(offspring_a)
            offspring_b = mutation_func(offspring_b)
            next_generation += [offspring_a, offspring_b]
        population = next_generation

    population = sorted(
        population,
        key=lambda genome: fitness_func(genome),
        reverse=True
    )
    return population, i

population, generations = run_evolution(
    populate_func=partial(
        generate_population, size=8, genome_length=len(cities)
    ),
    fitness_func=partial(
        fitness, cities=cities, value_limit=y, distance_limit=1000
    ),
    fitness_limit=4000,
    generation_limit=100
)

def genome_to_things(genome: Genome, cities: [City]) -> [City]:
    result = []
    value = 0
    for i, city in enumerate(cities):
        if genome[i] == 1:
            result += [city.name]
            value += city.value
    return result, value

def final_route(genome: Genome, cities: [City]) -> int:
    route, value = genome_to_things(population[0], cities)
    print(f"1 пункт: {route} = {value}")
    route = []
    value = 0
    id = 2
    for i, city in enumerate(cities):
        if genome[i] == 0:
            if value + city.value >= y:
                print(f"{id} пункт: {route} = {value}")
                id += 1
                value = 0
                route = []
            route += [city.name]
            value += city.value
    print(f"{id} пункт: {route} = {value}")
    return 1

print(f"Количество поколений: {generations}")
# print(f"best solution: {genome_to_things(population[0], cities)}")
final_route(population[0], cities)
print()
print("========== ПОПУЛЯЦИЯ ==========")
for i in range(len(population)):
    print(f"[{i+1}]: {genome_to_things(population[i], cities)}")