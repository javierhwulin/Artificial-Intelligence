"""
function GENETIC-ALGORITHM(population, fitness) returns an individual
    repeat
        weights ← WEIGHTED-BY(population, fitness)
        population2 ← empty list
        for i = 1 to SIZE(population) do
            parent1, parent2 ← WEIGHTED-RANDOM-CHOICES(population, weights, 2)
            child ← REPRODUCE(parent1, parent2)
            if (small random probability) then child ← MUTATE(child)
            add child to population2
        population ← population2
    until some individual is fit enough, or enough time has elapsed
    return the best individual in population, according to fitness

function REPRODUCE(parent1, parent2) returns an individual
    n ← LENGTH(parent1)
    c ← random number from 1 to n
    return APPEND(SUBSTRING(parent1, 1, c), SUBSTRING(parent2, c + 1, n))
"""
import numpy as np
import matplotlib.pyplot as plt


def rastrigin(x):
    A = 10
    return A * x.shape[0] + np.sum(x**2 - A * np.cos(2 * np.pi * x), axis=0)


def create_individual(dim):
    return np.random.uniform(-5.12, 5.12, dim)


def create_population(pop_size, dim):
    return [create_individual(dim) for _ in range(pop_size)]


def fitness(individual):
    return rastrigin(individual)


def select_parents(population, fitnesses, num_parents):
    parents = []
    for _ in range(num_parents):
        idx = np.random.choice(len(population), size=3, replace=False)
        tournament = [population[i] for i in idx]
        tournament_fitness = [fitnesses[i] for i in idx]
        winner = tournament[np.argmax(tournament_fitness)]
        parents.append(winner)
    return parents


def crossover(parents, offspring_size):
    offspring = []
    for _ in range(offspring_size):
        selected = np.random.choice(len(parents), 2, replace=False)
        parent1, parent2 = [parents[i] for i in selected]
        child = (parent1 + parent2) / 2
        offspring.append(child)
    return offspring


def mutate(individual, mutation_rate):
    for i in range(len(individual)):
        if np.random.random() < mutation_rate:
            individual[i] += np.random.normal(0, 0.5)
            individual[i] = np.clip(individual[i], -5.12, 5.12)
    return individual


def genetic_algorithm(pop_size, dim, generations, mutation_rate):
    population = create_population(pop_size, dim)
    best_fitness = float('-inf')
    best_individual = None
    fitness_history = []

    for _ in range(generations):
        fitnesses = [fitness(ind) for ind in population]
        best_gen_fitness = max(fitnesses)
        best_gen_individual = population[np.argmax(fitnesses)]

        if best_gen_fitness > best_fitness:
            best_fitness = best_gen_fitness
            best_individual = best_gen_individual

        fitness_history.append(best_fitness)

        parents = select_parents(population, fitnesses, pop_size // 2)
        offspring = crossover(parents, pop_size - len(parents))
        offspring = [mutate(child, mutation_rate) for child in offspring]
        population = (
            parents + offspring
        )  # Select population based on elitism approach

    return best_individual, best_fitness, fitness_history


if __name__ == '__main__':
    dim = 2
    pop_size = 100
    generations = 500
    mutation_rate = 0.1

    best_solution, best_fitness, fitness_history = genetic_algorithm(
        pop_size, dim, generations, mutation_rate
    )

    print(f'Best solution: {best_solution}')
    print(f'Best fitness: {best_fitness}')

    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.plot(fitness_history)
    plt.title('Fitness History')
    plt.xlabel('Generation')
    plt.ylabel('Best Fitness')

    plt.subplot(1, 2, 2)
    x = np.linspace(-5.12, 5.12, 100)
    y = np.linspace(-5.12, 5.12, 100)
    X, Y = np.meshgrid(x, y)
    Z = rastrigin(np.array([X, Y]))

    plt.contourf(X, Y, Z, levels=50, cmap='viridis')
    plt.colorbar(label='Rastrigin Function Value')
    plt.scatter(
        best_solution[0],
        best_solution[1],
        color='red',
        marker='*',
        s=200,
        label='Best Solution',
    )
    plt.title('Rastrigin Function Contour')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()

    plt.tight_layout()
    plt.show()
