################################################################################
# This will be an attempt at a functional ant colony optimization function

from GAtools import avgFitness
from tools import *
import numpy as np
import random
import warnings #this module is being used to get rid of the runtime warning

################################################################################
# ETA is computed at beginning of function from table & distances between cities
# TAO is set at beginning based on size of table, init to all 1's (no ants!)
# both ETA and TAO are tables that will be the size of the table examined.
# for 26 puzzle: ANTS=20, ITERS=1000, INIT_PHER/ETA_VAR=100
# Q = 937, ALPHA=2, BETA=2 works sometimes, falls into local minima
ANTS = 20
ITERS = 2000
INIT_PHER = 100 # init put on tao
Q = 937 # pher put down along path like Q?...
ETA_VAR = 100 #eta found by this divided by length?
RHO = .1
ALPHA, BETA = 2, 2
TITLE = './datasets/five19.txt'

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
    
def updatePheromones(ant, tao, table):
    size = table.shape[0]
    tour = findTourLen(ant, table)
    delta = Q / tour
    # this is one directional... doesn't update other way.
    for city in range(0, size - 1):
        tao[ant[city]][ant[city + 1]] += delta
        tao[ant[city + 1]][ant[city]] += delta # for symmetric graphs
    tao[ant[city + 1]][ant[0]] += delta
    tao[ant[0]][ant[city + 1]] += delta
    return tao

def evapPheromones(tao):
    return tao * (1 - RHO)

def main():
    table = np.loadtxt(TITLE)
    size = table.shape[0] #finds size of map
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
        if i == 0 or (i+1) % 100 == 0:
        #     print("COLONY AFTER TRAVEL:")
        #     for ant in colony:
        #         print(ant, "fitness:", findTourLen(ant, table))
            print("GEN:", str(i+1).zfill(4), "AVG FIT: {:.2f}".format(avgFitness(colony, table)))
        # if (i+1) % 500 == 0:
        #     print("NEW TAO, HOPEFULLY:")
        #     print(tao)
        for ant in colony:
            tao = updatePheromones(ant, tao, table)
        tao = evapPheromones(tao)
        
    print("FINAL TAO: \n", tao)
    print("FINAL COLONY AFTER TRAVEL:")
    for ant in colony:
        print(ant, "fitness:", findTourLen(ant, table))
    print("FINAL GEN:", str(i+1).zfill(4), "AVG FIT: {:.2f}".format(avgFitness(colony, table)))



if __name__ == "__main__":
    main()