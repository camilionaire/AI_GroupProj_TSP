################################################################################
# This will be an attempt at a functional ant colony optimization function

from GAtools import avgFitness
from tools import *
import numpy as np
import random

################################################################################
# ETA is computed at beginning of function from table & distances between cities
# TAO is set at beginning based on size of table, init to all 1's (no ants!)
# both ETA and TAO are tables that will be the size of the table examined.
ANTS = 10
ITERS = 500
INIT_PHER = 1 # init put on tao
# IMPORTANT Q=100 FOR 25 MAP, Q=1 FOR 4 MAP
Q = 10 # pher put down along path like Q?...
ETA_VAR = 1 #eta found by this divided by length?
RHO = .1
ALPHA, BETA = 1, 2
TITLE = './datasets/twentysix937.txt'

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
    tao[ant[city + 1]][ant[0]] += delta
    return tao

def evapPheromones(tao):
    return tao * (1 - RHO)

def main():
    table = np.loadtxt(TITLE)
    size = table.shape[0] #finds size of map
    eta = createETA(table, size)
    tao = createTAO(size)
    # top_prob = bigBad(tao, eta, size)

    print("ETA:\n", eta)
    print("TAO:\n", tao)
    # print("TOP PROB:\n", top_prob)
    
    # for the number of... eventually iterations
    for i in range(0, ITERS):
        colony = []
        fitness = []
        # BUG, I don't know if this approach works
        # top_prob = bigBad(tao, eta, size)
    # all of the ants travel here
        for j in range(0, ANTS):
            ant = createAnt(size)
            colony.append(ant)
        # if i % 200 == 0:
        #     print("COLONY B4 TRAVEL:", colony)
        for ant in colony:
            ant = goTravel(ant, tao, eta, size)
        if i == 0 or (i+1) % 20 == 0:
        #     print("COLONY AFTER TRAVEL:")
        #     for ant in colony:
        #         print(ant, "fitness:", findTourLen(ant, table))
            print("GEN:", str(i+1).zfill(4), "AVG FIT: {:.2f}".format(avgFitness(colony, table)))
        for ant in colony:
            tao = updatePheromones(ant, tao, table)
        tao = evapPheromones(tao)
        # if i % 200 == 0:
        #     print("NEW TAO, HOPEFULLY:")
        #     print(tao)
        

        # BUG this doesn't seem to work, reworking
        # for ant in colony:
        #     makeTravelChoices(ant, top_prob, size)
        #     fitness.append(findTourLen(ant, table))
        # tao = evapAndDist(colony, fitness, table, tao, size)
        # if i == 0 or (i+1) % 400 == 0:
        #     print("Gen:", i+1, "Average Fitness: ", avgFitness(colony, table))
        #     print("TAO:\n", tao)
            # print(tao)

if __name__ == "__main__":
    main()