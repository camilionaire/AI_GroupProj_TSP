################################################################################
#
#  Initial set up for travelling salesperson problem to eventually make a few
#  AI algorithms to solve it.
#
################################################################################
import numpy as np
import random
import sys
from simAnTSP import *

# finds the current tour length.
def findTourLen(arr, table):
    total = 0
    for i in range(0, len(arr)):
        if i == (len(arr) - 1):
            total = total + table[arr[i]][arr[0]]
        else:
            total = total + table[arr[i]][arr[i+1]]
    return total

# creates a random initial arrangement of size
def createRandoArr(size):
    an_array = [None] * size

    for i in range(0, size):
        a_city = random.randint(0, size - 1)
        while a_city in an_array:
            a_city = random.randint(0, size - 1)
        an_array[i] = a_city

    return an_array


# true if arr1 is better, false otherswise
def isBetter(arr1, arr2, table):
    # it always will choose to move on the plateau
    if findTourLen(arr1, table) <= findTourLen(arr2, table):
        return True
    else:
        return False

# returns true if a rando # (0, 1] is less than some prob
def decision(prob):
    return random.random() < prob

def main():
    # uses np for numpy, loads the file and makes a table!
    # this is the command right after python ./main.py ________ <here
    if len(sys.argv) == 2:
        my_table = np.loadtxt(sys.argv[1])
    else:
        my_table = np.loadtxt('five19.txt')

    hillClimb = simuAnneal(my_table)
    print(hillClimb)
    print(findTourLen(hillClimb, my_table))

if __name__ == "__main__":
    main()