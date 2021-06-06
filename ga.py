import numpy as np
import matplotlib.pyplot as plt
import random
import time
from collections import OrderedDict

ITERATION = 1000
INITIAL_POPULATION = 1000


class Population:
    def __init__(self, pop, adjacency_mat):
        self.pop = pop
        self.parents = []
        self.scores = []
        self.best = float('inf')
        self.result_history = []
        self.score_history = []
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
        if self.best >= sum_fit and len(chromosome) == len(set(chromosome)):
            self.best = sum_fit
            self.result_history.append(tuple((chromosome, self.best)))
            self.result = chromosome.copy()
            # print("\n-------------------------------------")
            # print("Best score so far: ", self.best)
            # print("Best result so far: ", self.result)
            # print("-------------------------------------\n")
        return sum_fit

    def evaluate(self):
        distances = []
        for chromosome in self.pop:
            distances.append(self.fitness(chromosome))
        distances = np.asarray(distances)
        distances = np.reciprocal(distances)
        for i in distances:
            self.scores.append(i / np.sum(distances))

    def select_parents(self):
        # candidate = random.choices(self.pop, self.scores)[0]
        # reduce parents has low score because duplicate cities
        # while len(candidate) - len(set(candidate)) > len(self.pop[0]) * 0.4:
        #     candidate = random.choices(self.pop, self.scores)[0]
        candidate = random.choices(self.pop, self.scores)[0]
        return candidate

    def crossover_mutate(self):
        children = []
        for i in range(int(len(self.pop) / 2)):
            father = self.select_parents()
            mother = self.select_parents()

            cross_point = random.randrange(1, len(father) - 2)
            # simple crossover :/
            # temp = father[cross_point:].copy()
            # father[cross_point:] = mother[cross_point:]
            # mother[cross_point:] = temp

            temp_father = father.copy()
            # remove part of father and add missing part from mother according to the order in mother chromosome
            # print("---------------------------------Cross over------------------------------------------------")
            # print("cross:", cross_point, "\nfather:", father, " \n", "mother: ", mother)
            temp = []
            father = father[:cross_point]
            for j in mother:
                if j not in father:
                    temp.append(j)
            father = np.append(father, temp)

            temp = []
            mother = mother[:cross_point]
            for j in temp_father:
                if j not in mother:
                    temp.append(j)
            mother = np.append(mother, temp)
            # print("\ncross:", cross_point, "\nfather:", father, " \n", "mother: ", mother)
            # print("-------------------------------------------------------------------------------------------")

            # 3% mutation rate, will flip subarray in father/mother from startpoint to end point
            mut_start = random.randint(1, len(father) - 2)
            if random.randint(0, 100) <= 3:
                # print("\nmut_start:", mut_start, "\nfather:", father, " \n", "mother: ", mother)
                mutate_temp = father[mut_start:]
                # print("\nmutate_temp:", mutate_temp)
                father = father[:mut_start]
                father = np.append(father, mutate_temp[::-1])
                # print("\nEnd: \nfather:", father, " \n", "mother: ", mother)

            if random.randint(0, 100) <= 3:
                mutate_temp1 = mother[mut_start:]
                mother = mother[:mut_start]
                mother = np.append(mother, mutate_temp1[::-1])

            children.append(father)
            children.append(mother)
        self.pop = children.copy()
        return self.pop

    def get_best(self):
        best_path = []
        for i in self.result_history:
            self.score_history.append(i[1])
            if i[1] == self.best:
                best_path.append(i[0])
        best_path = OrderedDict((tuple(x), x) for x in best_path).values()

        print("\n=============================")
        print("The best score: ", self.best)
        print("Unique paths found with score", self.best, ": ")
        for path in best_path:
            print(path)
        print("============================= \n")

    def plot_results_score(self):
        self.score_history = list(set(self.score_history))
        print(self.score_history)
        plt.plot(range(len(self.score_history)), self.score_history, color="skyblue")
        plt.show()


def ga_main(my_table):
    start = time.time()
    # print(my_table)
    cities = []
    population = Population([], my_table)
    for i in range(len(my_table)):
        cities.append(i)

    pop = population.generate_population(cities, my_table, INITIAL_POPULATION)
    for i in range(ITERATION):
        print("Iteration: ", i) if i % 50 == 0 else None
        population.evaluate()
        population.crossover_mutate()
    population.get_best()
    population.plot_results_score()
    elapsed = time.time() - start
    print("\n\nScript execution time: {} seconds".format(elapsed))
