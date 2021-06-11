################################################################################
# This will be an attempt at a functional ant colony optimization function

from GAtools import avgFitness, getLenArray
from tools import *
import numpy as np
import random
import warnings #this module is being used to get rid of the runtime warning
import time

################################################################################
# ETA is computed at beginning of function from table & distances between cities
# TAO is set at beginning based on size of table, init to all 1's (no ants!)
# both ETA and TAO are tables that will be the size of the table examined.

#5puzze: ant=10, iters=5000, 1, 1, 1, .1, alpha=1, beta=2
#26puzzle: ANTS=20, ITERS=1000, INIT_PHER/ETA_VAR=100
# Q = 937, ALPHA=2, BETA=2 works sometimes, falls into local minima
#48puzzle: ants=100, iters=200, 1, 900, 900, .1, alpha=2, beta=2 under 40k.
# ^^^ not consistent tho, fails to local minima sometimes.
#48puzzle, ants=30, iters=400, 1, 900, 900, .1, 2, 2 seems to get under 40k
ANTS = 30
ITERS = 400
INIT_PHER = 1 # init put on tao
Q = 900 # pher put down along path like Q?... maybe have it optimal sol?
ETA_VAR = 900 # eta found by this divided by length?
RHO = .1 # standard rho
ALPHA, BETA = 2, 2
# TITLE = './datasets/five19.txt'
# TITLE = './datasets/twentysix937.txt'
# TITLE = './datasets/fortytwo699.txt'
TITLE = './datasets/fortyeight33523.txt'

# chooses a random city for ant to start in
def createAnt(size):
    start_pos = random.randint(0, size-1)
    ant = [start_pos] # assigns to beg city.
    return ant

# Eta is set to reciprocal of table w/0's on diag
def createETA(table, size):
    eta = np.zeros((size, size))
    for row in range(0, size):
        for col in range(0, size):
            if row != col:
                eta[row][col] = ETA_VAR / table[row][col]
    #div by zero along axis warning error fixed using warnings module!
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        eta = np.reciprocal(table) * ETA_VAR
        for diag in range(0, size):
            eta[diag][diag] = 0
    return eta

# tao initially set to INIT_PHER, will change throughout func.
def createTAO(size):
    tao = np.full((size, size), INIT_PHER)
    for diag in range(0, size):
        tao[diag][diag] = 0
    return tao

def goTravel(ant, tao, eta, size):
    while len(ant) < size:
        currCity = ant[len(ant) - 1]
        possibilities = []
        sum = 0
        for city in range(0, size):
            if city not in ant:
                possibilities.append(city) # possible city
                sum += pow(tao[currCity][city], ALPHA) * pow(eta[currCity][city], BETA)
        
        rand = random.uniform(0, sum) # creates roulette wheel...
        wheelNeedle = 0

        for city in possibilities:
            wheelNeedle += pow(tao[currCity][city], ALPHA) * pow(eta[currCity][city], BETA)
            if wheelNeedle >= rand:
                ant.append(city)
                break
    return ant
    
def updatePheromones(ant, tao, table, mult):
    size = table.shape[0]
    tour = findTourLen(ant, table)
    delta = Q / tour
    # this is one directional... doesn't update other way.
    for city in range(0, size - 1):
        tao[ant[city]][ant[city + 1]] += delta * mult
        tao[ant[city + 1]][ant[city]] += delta * mult# for symmetric graphs
    tao[ant[city + 1]][ant[0]] += delta * mult
    tao[ant[0]][ant[city + 1]] += delta * mult
    return tao

def evapPheromones(tao):
    return tao * (1 - RHO)

def antColonyOpt(table):
## TESTING / PRINTING DATA #####################################################
    start = time.time()
    bestEver = 99999999 # best tour so far
    bestie = [] # path of best tour
    greatestGen = 0 # gen best is found
    xArray, yArray = [], []
    homogeny, prevAvg = 0, 0
################################################################################
    size = table.shape[0] #finds size of map
    print("TABLE AVERAGE", np.average(table))
    eta = createETA(table, size)
    tao = createTAO(size)

    # print("ETA:\n", eta)
    # print("TAO:\n", tao)
    
    # for the number of... eventually iterations
    for i in range(0, ITERS):
        colony = []
        for j in range(0, ANTS):
            ant = createAnt(size)
            colony.append(ant)
        # if i % 200 == 0:
        #     print("COLONY B4 TRAVEL:", colony)
        for ant in colony:
            ant = goTravel(ant, tao, eta, size)

        antsLen = getLenArray(colony, table)
        bestGen = min(antsLen)
        bestInGen = colony[antsLen.index(bestGen)]
        if bestGen < bestEver:
            bestEver = bestGen
            bestie = bestInGen
            greatestGen = i+1

        if i == 0:
            print("GEN:", str(i+1).zfill(4), "AVG FIT: {:.2f}".format(np.average(antsLen)))
        if (i+1) % 5 == 0:
            avg = np.average(antsLen)
            if prevAvg != avg: homogeny = 0
            else:
                print("Homogeny found.")
                homogeny += 1
                if homogeny == 3: # if it get's stuck in a rut
                    break
            prevAvg = avg
            xArray.append(i+1)
            yArray.append(avg)
            if (i+1) % 10 == 0:
                print("GEN:", str(i+1).zfill(4), "AVG FIT: {:.2f}".format(avg))
                
        # if (i+1) % 500 == 0:
        #     print("NEW TAO, HOPEFULLY:")
        #     print(tao)
        tao = evapPheromones(tao)
        for ant in colony:
            # NOTE giving it a little bit of elitism here.
            if ant == bestInGen:
                mult = 2
            else:
                mult = 1
            tao = updatePheromones(ant, tao, table, mult)
        
# NOTE TESTING INFORMATION, CAN BE COMMENTED / ADJUSTED
    # print("FINAL TAO: \n", tao)
    file = open("finalTao.txt", "w")
    for row in tao:
        file.write(str(row) + "\n")
    print("FINAL COLONY AFTER TRAVEL:")
    for ant in colony:
        print("fitness:", findTourLen(ant, table), end=", ")
    print("\nFINAL GEN:", str(i+1).zfill(4), "AVG FIT: {:.2f}".format(avgFitness(colony, table)))

    print("Best Tour:", bestEver, " Found in Gen:", greatestGen)
    print("Path: ", bestie)

    elapsed = time.time() - start
    print("\nGA ran in {:.3f} seconds".format(elapsed))
    plot_results(xArray, yArray)


def main():
    table = np.loadtxt(TITLE)
    antColonyOpt(table)


if __name__ == "__main__":
    main()