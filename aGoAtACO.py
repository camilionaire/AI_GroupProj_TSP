################################################################################
# This will be an attempt at a functional ant colony optimization function

from GAtools import avgFitness
from tools import *
import numpy as np
import random

################################################################################
# ETA is computed at beginning of function from table & distances between cities
# TAO is set at beginning based on size of table, init to all 0's (no ants!)
# both ETA and TAO are tables that will be the size of the table examined.
ANTS = 10
ITERS = 10000
INIT_PHER = 1 # init put on tao
# IMPORTANT Q=100 FOR 25 MAP, Q=1 FOR 4 MAP
Q = 100 # pher put down along path like Q?...
ETA_VAR = 1 #eta found by this divided by length?
RHO = .1
ALPHA, BETA = 2, 2
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
    # NOTE taken out cuz of div by zero along axis warning error
    # eta = np.reciprocal(table) * ETA_VAR
    # for diag in range(0, size):
    #     eta[diag][diag] = 0
    return eta

# tao initially set to INIT_PHER, will change throughout func.
def createTAO(size):
    tao = np.full((size, size), INIT_PHER)
    for diag in range(0, size):
        tao[diag][diag] = 0
    return tao

# NOTE... not sure the math checks out on this one...
# tao^alpha * eta^beta won't change, can do that ahead, but sum of allowed, need at decision.
# just doing the top of bad function for now.
# def bigBad(tao, eta, size):
#     prob = np.zeros((size, size))
#     for row in range(0, size):
#         for col in range(0, size):
#             prob[row][col] = pow(tao[row][col], ALPHA) * \
#                 pow(eta[row][col], BETA)

#     return prob

# # NOTE this function is currently not taking into account the fact that
# # all the tours are two possible ways.  so 1->2 pheromone != 2->1.
# def evapAndDist(colony, fit, table, tao, size):

#     deltaTao = np.zeros((size, size))
#     for ant in range(0, ANTS):
#         for i in range(0, size - 1):
#             deltaTao[colony[ant][i]][colony[ant][i+1]] += Q / fit[ant]# * table[colony[ant][i]][colony[ant][i+1]]
#         # added in for symmetric graphs
#             deltaTao[colony[ant][i+1]][colony[ant][i]] += Q / fit[ant]# * table[colony[ant][i+1]][colony[ant][i]]

#         # add in back to front here...
#         deltaTao[colony[ant][size - 1]][colony[ant][0]] += Q / fit[ant]# * table[colony[ant][size - 1]][colony[ant][0]] 
#     # added in for symmetric graphs
#         deltaTao[colony[ant][0]][colony[ant][size - 1]] += Q / fit[ant]# * table[colony[ant][0]][colony[ant][size - 1]] 
   
#     # evaporate and add in new stuff.
#     for row in range(0, size):
#         for col in range(0, size):
#             tao[row][col] = (tao[row][col] + deltaTao[row][col]) * (1 - RHO)

#     return tao

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
        if i % 200 == 0:
        #     print("COLONY AFTER TRAVEL:")
        #     for ant in colony:
        #         print(ant, "fitness:", findTourLen(ant, table))
            print("AVG FIT:", avgFitness(colony, table))
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