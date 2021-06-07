################################################################################
# new genetic algorithm to solve the travelling salesperson problem
from tools import *
import random
import time

################################################################################
POPULATION = 40
GENERATIONS = 15000
MUT_PRO = .045
EXTRA_CHANCE = 0
TITLE = './datasets/fortyeight33523.txt'
################################################################################
# POP / GEN / MUT
# 30 / 15000 / .045 best so far for 48cities sol 34300
# ^^^^^^^^^ this may have been a fluke, usually 35-36k
#

# this gets an array of lengths from the population
def getLenArray(pop, table):
    tourLen = []
    for i in pop:
        tourLen.append(findTourLen(i, table))
    return tourLen

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

def chooseParents(pop, total, diff):
    # if we reached homogeny
    if total == 0:
        return pop[0], pop[1]

    # this acts like a spin wheel, total = wheel size,
    # diff array acts like slices for each member of pop
    choice1 = random.randint(1, total)
    choice2 = random.randint(1, total)
    found1, found2 = False, False

    for i in range(0, len(pop)):
        choice1 -= diff[i]
        choice2 -= diff[i]
        if choice1 <= 0 and not found1:
            parent1 = pop[i]
            found1 = True
        if choice2 <= 0 and not found2:
            parent2 = pop[i]
            found2 = True

    return parent1, parent2

# takes slice of par 1, fills in rest with par2        
def crossOver(par1, par2):
    length = len(par1)
    cut1 = random.randint(0, length) # spot 0 to 25 (example)
    cut2 = random.randint(0, length) # spot 0 to 25 
    if cut2 < cut1:
        cut1, cut2 = cut2, cut1

    child = [-1 for col in range(length)] # pos 0 to 24 (example)

    if cut1 == cut2: #takes after par2 edge case?
        child = par2
    else:
        for i in range(cut1, cut2): # from smallest 0 to 25
            child[i] = par1[i]
        j = 0
        for i in range(0, length):
            if child[i] == -1:
                while par2[j] in child:
                    j += 1
                child[i] = par2[j]

    return child

# finds a populations average fitness.
def avgFitness(pop, table):
    total = 0
    for i in pop:
        total += findTourLen(i, table)
    return total / len(pop)
    
# NOTE this mutate func, while it does work... doesn't do so great.
# needs something a little more mutatety.
def mutate(child):
    length = len(child)# - 1
    cut1 = random.randint(0, length) # 0 to 25 (example)
    cut2 = random.randint(0, length) # 0 to 25
    if cut2 < cut1:
        cut1, cut2 = cut2, cut1
    # checks for edge cases
    if cut1 == cut2: 
        newChild = child
    elif cut1 == 0 and cut2 == length:
        newChild = child[::-1]
    else: # checks for edg cases
        if cut1 == 0:
            newChild = child[cut2-1::-1] + child[cut2:]
        elif cut2 == length:
            newChild = child[:cut1] + child[:cut1 - 1:-1] 
        else: # middle 'normal' switch cases
            newChild = child[:cut1] + child[cut2 - 1:cut1 - 1:-1] + child[cut2:]

    return newChild

def makeBabies(tot, better, pop):
    par1, par2 = chooseParents(pop, tot, better)
    child = crossOver(par1, par2)
    if decision(MUT_PRO):
        child = mutate(child)
    return child

def geneticAlgorithm(table):
    start = time.time()

    size = table.shape[0]
    bestEver = 99999999 # best tour so far
    bestie = [] # path of best tour
    greatestGen = 0 # gen best is found
    xArray, yArray = [], []

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

    print("\nFinal Gen Avg: {:.2f}".format(avgFitness(oldGen, table)))
    print("Best Tour:", bestEver, " Found in Gen:", greatestGen)
    print("Path: ", bestie)

    elapsed = time.time() - start
    print("\nGA ran in {:.3f} seconds".format(elapsed))
    plot_results(xArray, yArray)
################################################################################

if __name__ == "__main__":
    table = np.loadtxt(TITLE)
    geneticAlgorithm(table)

def main():
    pass
    # start = time.time()
    # table = np.loadtxt(TITLE)
    # print(TITLE)
    # size = table.shape[0]
    # bestEver = 99999999 # best tour so far
    # bestie = [] # path of best tour
    # greatestGen = 0 # gen best is found
    # xArray, yArray = [], []

    # oldGen = createPopulation(size)
    # tourArray = getLenArray(oldGen, table)
    # print("\nINITIAL GENERATIONAL AVG: {:.2f}\n".format(avgFitness(oldGen, table)))

    # for i in range(0, GENERATIONS):
    #     newGen = []
    #     #tot = size of wheel, # better = array, size of each slice
    #     tot, better = socialStatus(tourArray)
    #     for j in range(0, POPULATION):
    #         par1, par2 = chooseParents(oldGen, tot, better)
    #         child = crossOver(par1, par2)
    #         if decision(MUT_PRO):
    #             child = mutate(child)
    #         newGen.append(child)

    #     oldGen = newGen
    #     tourArray = getLenArray(oldGen, table)

        # bestGen = min(tourArray)
        # if bestGen < bestEver:
        #     bestEver = bestGen
        #     bestie = oldGen[tourArray.index(bestGen)]
        #     greatestGen = i+1
        
    #     if i == 0:
    #         avg = avgFitness(newGen, table)
    #         print("Generation:", str(i+1).zfill(4), "Gen Avg: {:.2f}".format(avg))
    #     # Starts printing to graph at iteration 100.
    #     if (i+1) % 100 == 0:
    #         avg = avgFitness(newGen, table)
    #         xArray.append(i+1)
    #         yArray.append(avg)
    #         if (i+1) % 500 == 0:
    #             print("Generation:", str(i+1).zfill(4), "Gen Avg: {:.2f}".format(avg))


    # print("\nFinal Gen Avg: {:.2f}".format(avgFitness(oldGen, table)))
    # print("Best Tour:", bestEver, " Found in Gen:", greatestGen)
    # print("Path: ", bestie)

    # elapsed = time.time() - start
    # print("\nGA ran in {:.3f} seconds".format(elapsed))
    # plot_results(xArray, yArray)
