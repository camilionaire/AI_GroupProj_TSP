################################################################################
# new genetic algorithm to solve the travelling salesperson problem
# EXTRA FILES AND FUNCTIONS FOUND IN GATOOLS.PY AND TOOLS.PY!!!
from tools import *
from GAtools import *
import random
import time

################################################################################
POPULATION = 30
GENERATIONS = 15000
MUT_PRO = .044
EXTRA_CHANCE = 0 # for providing a little extra chance for low pop scores
TITLE = './datasets/fortyeight33523.txt' # testing if run from main()
################################################################################
# POP / GEN / MUT
# 30 / 15000 / .045 best so far for 48cities sol 34300
# 30 / 15000 / .044 scored 34001 in gen 14381, had weird graph
# 100 / 10000 / .05 got a 937 for 26 puzzle, but found in gen 2500.
# TODO find something to either beat that for 48 puzzle
# or get a good mix to crack the 42 puzzle.

# this creates a populations of size specified.
def createPopulation(size):
    pop = []
    for i in range(0, POPULATION):
       pop.append(createRandoArr(size)) 
    return pop

# takes in array of tour lengths
# gets total = size of wheel, diff = slice of wheel to pop
def socialStatus(lenArray):
    # NOTE adding +1 to give everyone a chance
    biggest = max(lenArray) + EXTRA_CHANCE
    diff = []
    for i in lenArray:
        diff.append(int(biggest - i))
    total = sum(diff)
    return total, diff

def makeBabies(tot, better, pop):
    par1, par2 = chooseParents(pop, tot, better)
    child = crossOver(par1, par2)
    if decision(MUT_PRO):
        child = mutate(child)
    return child

def geneticAlgorithm(table):
## TESTING / PRINTING DATA #####################################################
    start = time.time()
    bestEver = 99999999 # best tour so far
    bestie = [] # path of best tour
    greatestGen = 0 # gen best is found
    xArray, yArray = [], []
################################################################################

    size = table.shape[0] # gets size of array
    oldGen = createPopulation(size)
    tourArray = getLenArray(oldGen, table)
    print("\nINITIAL GENERATIONAL AVG: {:.2f}\n".format(avgFitness(oldGen, table)))

    for i in range(0, GENERATIONS):
        newGen = []
        #tot = size of wheel, # better = array, size of each slice
        tot, better = socialStatus(tourArray)
        for j in range(0, POPULATION):
            child = makeBabies(tot, better, oldGen)
            newGen.append(child)
        oldGen = newGen
        tourArray = getLenArray(oldGen, table)
        # end of real functional stuff

        # testing / output for seeing information.
################################################################################
        bestGen = min(tourArray)
        if bestGen < bestEver:
            bestEver = bestGen
            bestie = oldGen[tourArray.index(bestGen)]
            greatestGen = i+1
        if i == 0:
            avg = avgFitness(newGen, table)
            print("Generation:", str(i+1).zfill(4), "Gen Avg: {:.2f}".format(avg))
        # Starts printing to graph at iteration 100.
        if (i+1) % 100 == 0:
            avg = avgFitness(newGen, table)
            xArray.append(i+1)
            yArray.append(avg)
            if (i+1) % 500 == 0:
                print("Generation:", str(i+1).zfill(4), "Gen Avg: {:.2f}".format(avg))

    # outside of for loop
    print("\nFinal Gen Avg: {:.2f}".format(avgFitness(oldGen, table)))
    print("Best Tour:", bestEver, " Found in Gen:", greatestGen)
    print("Path: ", bestie)

    elapsed = time.time() - start
    print("\nGA ran in {:.3f} seconds".format(elapsed))
    plot_results(xArray, yArray)
################################################################################

def main():
    pass

if __name__ == "__main__":
    table = np.loadtxt(TITLE)
    geneticAlgorithm(table)
