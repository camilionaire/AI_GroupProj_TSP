import numpy as np
import matplotlib.pyplot as plt
import random
import time

INIT_POP = 200
GENERATIONS = 2000

class Population:
    def __init__(self, pop, adjacency_mat):
        self.pop = pop
        self.parents = []
        self.scores = []
        self.best = float('inf')
        self.result_history = []
        self.result = []
        self.adjacency_mat = adjacency_mat

    def generate_population(self, cities, adjacency_mat, n_population):
        self.pop = np.asarray([np.random.permutation(cities) for _ in range(n_population)])
        return self.pop

    def fitness(self, chromosome):
        sum_fit = 0
        # clear previous generation's weights
        self.scores = []
        for i in range(len(chromosome) - 1):
            sum_fit += self.adjacency_mat[chromosome[i]][chromosome[i + 1]]
        sum_fit += self.adjacency_mat[chromosome[len(chromosome) - 1]][chromosome[0]]
        if self.best > sum_fit and len(chromosome) == len(set(chromosome)):
            self.best = sum_fit
            self.result_history.append(sum_fit)
            self.result = chromosome.copy()
            print("\n-------------------------------------")
            print("Best score so far: ", self.best)
            print("Best result so far: ", self.result)
            print("-------------------------------------\n")
        return sum_fit

    def evaluate(self):
        distances = []
        for chromosome in self.pop:
            distances.append(self.fitness(chromosome))

        distances = np.asarray(distances)
        distances = np.reciprocal(distances)
        for i in distances:
            self.scores.append(i/np.sum(distances))

    def get_best(self):
        print("\n=============================")
        print("The best: ", self.best)
        print("Result: ", self.result)
        print("============================= \n")

    def select_parents(self):
        candidate = random.choices(self.pop, self.scores)[0]
        # reduce parents has low score because duplicate cities
        while len(candidate) - len(set(candidate)) > len(self.pop[0]) * 0.4:
            candidate = random.choices(self.pop, self.scores)[0]

        return candidate

    def crossover_mutate(self):
        children = []
        for i in range(int(len(self.pop) / 2)):
            father = self.select_parents()
            mother = self.select_parents()

            cross_point = random.randrange(1, len(father) - 2)
            temp = father[cross_point:].copy()
            father[cross_point:] = mother[cross_point:]
            mother[cross_point:] = temp

            # 3% mutation rate
            if random.randint(0, 100) <= 3:
                mutate_index = random.randint(0, len(father) - 1)
                father[mutate_index] = mutate_index

            if random.randint(0, 100) <= 3:
                mutate_index = random.randint(0, len(father) - 1)
                mother[mutate_index] = mutate_index

            children.append(father)
            children.append(mother)
        self.pop = children.copy()
        return self.pop

    def plot_results_score(self):
        plt.plot(range(len(self.result_history)), self.result_history, color="skyblue")
        plt.show()


def ga_main(my_table):
    start = time.time()
    # print(my_table)
    cities = []
    population = Population([], my_table)
    for i in range(len(my_table)):
        cities.append(i)

    pop = population.generate_population(cities, my_table, INIT_POP)
    for i in range(GENERATIONS):
        print("Iteration: ", i) if i % 100 == 0 else None
        population.evaluate()
        population.crossover_mutate()
    population.get_best()
    population.plot_results_score()
    elapsed = time.time() - start
    print("\n\nScript execution time: {} seconds".format(elapsed))