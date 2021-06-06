################################################################################
# new genetic algorithm to solve the travelling salesperson problem
from tools import *
import random

POPULATION = 100
GENERATIONS = 10000
MUT_PRO = .05
TITLE = './datasets/fortyeight33523.txt'

def getLenArray(pop, table):
    tourLen = []
    for i in pop:
        tourLen.append(findTourLen(i, table))
    # print("tourLen", tourLen)
    return tourLen

def createPopulation(size):
    pop = []
    for i in range(0, POPULATION):
       pop.append(createRandoArr(size)) 
    return pop

def socialStatus(lenArray):
    biggest = max(lenArray)
    diff = []
    for i in lenArray:
        diff.append(int(biggest - i))
    total = sum(diff)
    return total, diff

def chooseParents(pop, total, diff):

    if total == 0:
        return pop[0], pop[1]

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

def avgFitness(pop, table):
    total = 0
    for i in pop:
        total += findTourLen(i, table)
    return total / len(pop)
    
def mutate(child):
    # I think this may be a bug in my logic but will hopefully still work.
    length = len(child)# - 1
    cut1 = random.randint(0, length) # 0 to 25
    cut2 = random.randint(0, length) # 0 to 25
    if cut2 < cut1:
        cut1, cut2 = cut2, cut1
        
    if cut1 == cut2: # escapes this time...
        newChild = child
    elif cut1 == 0 and cut2 == length:
        newChild = child[::-1]
    else: # might not work for edge cases...
        if cut1 == 0:
            newChild = child[cut2-1::-1] + child[cut2:]
        elif cut2 == length: # length is 25
            newChild = child[:cut1] + child[:cut1 - 1:-1] #hopefully is end to cut 1
        else:
            newChild = child[:cut1] + child[cut2 - 1:cut1 - 1:-1] + child[cut2:]

    if len(newChild) != length:
        print("SOMETHING WENT WRONG cut1, cut2:", cut1, cut2)
        print("here is the child:")
        print(newChild)
        print("length = ", len(newChild))
        
    return newChild

def main():
    table = np.loadtxt(TITLE)
    print(TITLE)
    size = table.shape[0]
    bestEver = 99999999
    bestie = []

    oldGen = createPopulation(size)
    tourArray = getLenArray(oldGen, table)

    print("Init Avg Fitness:", avgFitness(oldGen, table))

    for i in range(0, GENERATIONS):
        newGen = []
        for j in range(0, POPULATION):
            tot, better = socialStatus(tourArray)
            par1, par2 = chooseParents(oldGen, tot, better)
            child = crossOver(par1, par2)
            if decision(MUT_PRO):
                child = mutate(child)
            newGen.append(child)

        oldGen = newGen
        tourArray = getLenArray(oldGen, table)

        bestGen = min(tourArray)
        if bestGen < bestEver:
            bestEver = bestGen
            bestie = oldGen[tourArray.index(bestGen)]
        
        if i == 0 or (i+1) % 250 == 0:
            # bestLen = min(tourArray)
            # bestPath = oldGen[tourArray.index(bestLen)]
            print("Generation:", i+1, "Gen Avg: ", avgFitness(newGen, table))
            # print("best score:", bestLen, "for:")
            # print(bestPath)

    print("Finished Result: ", avgFitness(oldGen, table))
    print("Best Tour:", bestEver)
    print("Path: ", bestie)

if __name__ == "__main__":
    main()