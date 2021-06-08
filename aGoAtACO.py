################################################################################
# This will be an attempt at a functional ant colony optimization function

from tools import *
import numpy as np
import random

################################################################################
# ETA is computed at beginning of function from table & distances between cities
# TAO is set at beginning based on size of table, init to all 0's (no ants!)
# both ETA and TAO are tables that will be the size of the table examined.
ANTS = 10
ITERS = 100
INIT_PHER = 1
RHO = .1
ALPHA, BETA = 1, 1
TITLE = './datasets/five19.txt'

# chooses a random city for ant to start in
def createAnt(size):
    start_pos = random.randint(0, size-1)
    ant = [start_pos] # assigns to beg city.
    return ant

# Eta is set to reciprocal of table w/0's on diag
def createETA(table, size):
    eta = np.reciprocal(table)
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

    

def main():
    table = np.loadtxt(TITLE)
    size = table.shape[0] #finds size of map
    eta = createETA(table, size)
    tao = createTAO(size)
    top_prob = bigBad(tao, eta, size)

    print("ETA:\n", eta)
    print("TAO:\n", tao)
    print("TOP PROB:\n", top_prob)
    
    for i in range(0, 20):
        colony = []
        for i in range(0, ANTS):
            ant = createAnt(size)
            colony.append(ant)
        print("Colony: ", colony)

if __name__ == "__main__":
    main()