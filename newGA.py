################################################################################
# new genetic algorithm to solve the travelling salesperson problem
from tools import *
import random

POPULATION = 50
GENERATIONS = 1000

def getLenArray(pop, table):
    tourLen = []
    for i in pop:
        tourLen.append(findTourLen(i, table))
    print("tourLen", tourLen)
    return tourLen

def createPopulation(size):
    pop = []
    for i in range(0, POPULATION):
       pop.append(createRandoArr(size)) 
    return pop

def chooseParents(pop, lenArray):
    biggest = max(lenArray)
    print("biggest ", biggest)
    diff = []
    for i in lenArray:
        diff.append(int(biggest - i))

    print("diff ", diff)

    total = sum(diff)

    print("total", total)

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
        
# def crossOver(par1, par2):



def main():
    table = np.loadtxt('./datasets/five19.txt')
    size = table.shape[0]

    pop = createPopulation(size)
    tarr = getLenArray(pop, table)

    for i in range(0, POPULATION):
        print("Member: ", pop[i], " score: ", tarr[i])

    for i in range(0, POPULATION // 2):
        par1, par2 = chooseParents(pop, tarr)
        print("Par1: ", par1, " Score: ", findTourLen(par1, table))
        print("Par2: ", par2, " Score: ", findTourLen(par2, table))

if __name__ == "__main__":
    # size = table.shape[0]
    main()