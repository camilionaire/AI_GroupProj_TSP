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
ANTS = 20
ITERS = 2000
INIT_PHER = 1 # init put on tao
PHEROMONES = 902 # pher put down along path like Q?...
ETA_VAR = 1
RHO = .1
ALPHA, BETA = 1, 1
TITLE = './datasets/twentysix937.txt'

# chooses a random city for ant to start in
def createAnt(size):
    start_pos = random.randint(0, size-1)
    ant = [start_pos] # assigns to beg city.
    return ant

# Eta is set to reciprocal of table w/0's on diag
def createETA(table, size):
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

# NOTE... not sure the math checks out on this one...
# tao^alpha * eta^beta won't change, can do that ahead, but sum of allowed, need at decision.
# just doing the top of bad function for now.
def bigBad(tao, eta, size):
    prob = np.zeros((size, size))
    for row in range(0, size):
        for col in range(0, size):
            prob[row][col] = pow(tao[row][col], ALPHA) * \
                pow(eta[row][col], BETA)

    return prob

def makeTravelChoices(ant, prob, size):
    while len(ant) < size:
        currCity = ant[len(ant) - 1]
        possibilities = []
        poss_prob = []
        sum_pos = 0
        for col in range(0, size): # we go through cities
            # sees if the city is a possibility
            if col not in ant: # matches city to tao*eta func
                possibilities.append(col)
                poss_prob.append(prob[currCity][col])
                sum_pos += prob[currCity][col]

    # normalization quotient
        poss_prob = poss_prob / sum_pos
        # why do I need to put zero at the end here?...
        choice = random.choices(possibilities, poss_prob)[0]
        # for testing that things were getting selected correctly
        # print("Choices:", possibilities, "Probs:", poss_prob)
        ant.append(choice)

# NOTE this function is currently not taking into account the fact that
# all the tours are two possible ways.  so 1->2 pheromone != 2->1.
def evapAndDist(colony, fit, table, tao, size):

    deltaTao = np.zeros((size, size))
    for ant in range(0, ANTS):
        for i in range(0, size - 1):
            deltaTao[colony[ant][i]][colony[ant][i+1]] += \
                (PHEROMONES / fit[ant]) * table[colony[ant][i]][colony[ant][i+1]]
        # added in for symmetric graphs
            deltaTao[colony[ant][i+1]][colony[ant][i]] += \
                PHEROMONES / fit[ant] * table[colony[ant][i+1]][colony[ant][i]]

        # add in back to front here...
        deltaTao[colony[ant][size - 1]][colony[ant][0]] += \
            PHEROMONES / fit[ant] * table[colony[ant][size - 1]][colony[ant][0]] 
    # added in for symmetric graphs
        deltaTao[colony[ant][0]][colony[ant][size - 1]] += \
            PHEROMONES / fit[ant] * table[colony[ant][0]][colony[ant][size - 1]] 
   
    # evaporate and add in new stuff.
    for row in range(0, size):
        for col in range(0, size):
            tao[row][col] = tao[row][col] * (1 - RHO) + \
                deltaTao[row][col]

    return tao

        
def main():
    table = np.loadtxt(TITLE)
    size = table.shape[0] #finds size of map
    eta = createETA(table, size)
    tao = createTAO(size)
    top_prob = bigBad(tao, eta, size)

    print("ETA:\n", eta)
    print("TAO:\n", tao)
    print("TOP PROB:\n", top_prob)
    
    # for the number of... eventually iterations
    for i in range(0, ITERS):
        colony = []
        fitness = []

        top_prob = bigBad(tao, eta, size)
    # all of the ants travel here
        for j in range(0, ANTS):
            ant = createAnt(size)
            colony.append(ant)
        # print("Colony: ", colony)
        for ant in colony:
            makeTravelChoices(ant, top_prob, size)
            fitness.append(findTourLen(ant, table))
            
        tao = evapAndDist(colony, fitness, table, tao, size)

        if i == 0 or (i+1) % 50 == 0:
            print("Gen:", i+1, "Average Fitness: ", avgFitness(colony, table))
            # print("TAO:\n", tao)
            # print(tao)

if __name__ == "__main__":
    main()