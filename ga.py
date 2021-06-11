import numpy as np
import matplotlib.pyplot as plt

INITIAL_POPULATION = 70
ITERATION = 3000
MUTATION = 0.3
CROSS = 0.5
SELECTIVITY = 0.14


class Population:
    def __init__(self, population, matrix):
        self.population = population
        self.generation = []
        self.score = 0
        self.avg = 0
        self.score_history = []
        self.best = None
        self.matrix = matrix

    def fitness(self, chromosome):
        sum_fit = 0
        for i in range(len(chromosome) - 1):
            sum_fit += self.matrix[chromosome[i]][chromosome[i + 1]]
        sum_fit += self.matrix[chromosome[len(chromosome) - 1]][chromosome[0]]
        return sum_fit

    def evaluate(self):
        distances = np.asarray([self.fitness(chromosome) for chromosome in self.population])
        self.score = np.min(distances)
        self.avg = sum(distances)/len(distances)
        self.best = self.population[distances.tolist().index(self.score)]
        self.generation.append(self.best)
        if False in (distances[0] == distances):
            distances = np.max(distances) - distances
        return distances / np.sum(distances)

    def select_parents(self, selection):
        fit = self.evaluate()
        while len(self.generation) < selection:
            idx = np.random.randint(0, len(fit))
            if fit[idx] > np.random.rand():
                self.generation.append(self.population[idx])
        self.generation = np.asarray(self.generation)

    def crossover_mutation(self, cross_rate, mutate_rate):
        new_gen = []
        children = []
        count, size = self.generation.shape
        for _ in range(len(self.population)):
            if np.random.rand() > cross_rate:
                children.append(list(self.generation[np.random.randint(count, size=1)[0]]))
            else:
                parent1, parent2 = self.generation[np.random.randint(count, size=2), :]
                idx = np.random.choice(range(size), size=2, replace=False)
                start, end = min(idx), max(idx)
                child = [None] * size
                for i in range(start, end + 1, 1):
                    child[i] = parent1[i]
                pointer = 0
                for i in range(size):
                    if child[i] is None:
                        while parent2[pointer] in child:
                            pointer += 1
                        child[i] = parent2[pointer]
                children.append(child)
        for child in children:
            if np.random.rand() < mutate_rate:
                new_gen.append(swap(child))
            else:
                new_gen.append(child)
        return new_gen

    def plot_graph(self, history):
        plt.plot(range(len(history)), history, color="skyblue")
        plt.show()


def swap(chromosome):
    father, mother = np.random.choice(len(chromosome), 2)
    chromosome[father], chromosome[mother] = (chromosome[mother], chromosome[father],)
    return chromosome


def control(cities, matrix):
    population = Population(np.asarray([np.random.permutation(cities) for _ in range(INITIAL_POPULATION)]), matrix)
    best = 0
    best_history = []
    score = float("inf")
    history = []
    for i in range(ITERATION):
        population.select_parents(INITIAL_POPULATION * SELECTIVITY)
        history.append(population.score)
        if i % 300 == 0:
            print(f"Generation", i, ": Average fitness score:", population.avg, "Best of this gen:", population.score)
        if population.score < score:
            best = population.best
            average = population.avg
            best_history.append(average)
            score = population.score
        children = population.crossover_mutation(CROSS, MUTATION)
        population = Population(children, population.matrix)
    population.plot_graph(history)
    print("The best route found was: \n", best, "\nwith the length of:", score)
    return population.best, history


def ga_main(my_table):
    cities = []
    for i in range(len(my_table)):
        cities.append(i)
    control(cities, my_table)
