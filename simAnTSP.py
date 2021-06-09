# from main import *
import random
import math
from tools import *
import time

################################################################################
ITERATIONS = 200000
TEMP_MOD = 400
################################################################################
# ITERATIONS / TEMP_MOD:
# 200,000 / 400 works REAL good for the 48 city with big distances
# 200,000 / 3000 works good for 42 and 26 puzzles
# 100 / ANY#  I suspect everything works good for 5 city puzzle


# main function
def simuAnneal(table):
    start = time.time()
    bestEver = 99999999 # best tour so far
    bestie = [] # path of best tour
    greatestGen = 0 # gen best is found
    xArray, yArray = [], [] #arrays for storing plot data.
    size = table.shape[0]
    arr1 = createRandoArr(size)

    print("\nSimulated Annealing Starting:\n")

    for i in range(0, ITERATIONS):
        # decreasing temperature

        temp = (ITERATIONS - i) / TEMP_MOD #this works good on 42
        arr2 = findNeighborSA(arr1)
        if isBetter(arr2, arr1, table):
            arr1 = arr2.copy()
            curr = findTourLen(arr1, table)
            if  curr < bestEver:
                bestEver = curr
                bestie = arr1
                greatestGen = i+1
        else:
            delta = findTourLen(arr1, table) - findTourLen(arr2, table)
            # the math part of function e^delt/T
            probability = math.exp( delta / temp)
            # will make a non improving choice depending on prob.
            if decision(probability):
                arr1 = arr2.copy()
        if i == 0 or (i+1) % 10000 == 0:
            print("ITERATION:", str(i+1).zfill(5), "TOUR LENGTH:", findTourLen(arr1, table))
        # NOTE this is the part that stores the table to be displayed.
        if (i+1) % 1000 == 0: #or i == 0: # took out for better graph
            xArray.append(i+1)
            yArray.append(findTourLen(arr1, table))

    
    print("\nBEST TOUR:", bestEver, " FOUND IN ITERATION:", greatestGen)
    print("PATH: ", bestie)

    elapsed = time.time() - start
    print("\nSA ran in {:.3f} seconds".format(elapsed))
    # this is the part that prints the results.
    plot_results(xArray, yArray)
    
    return arr1

# finds a neighbor by taking a random slice and reversing order
def findNeighborSA(arrOG):
    arr = arrOG.copy()
    rando1 = random.randint(0, len(arr) - 1)
    rando2 = random.randint(0, len(arr) - 1)
    # switches so rando1 is smaller
    if rando2 < rando1:
        rando1, rando2 = rando2, rando1
# this switches the array around and makes checks for end cases.
    # if it's the full array, 
    if rando1 == 0 and rando2 == len(arr) - 1:
        arr2 = arr[::-1]
    # if it's the start to some spot
    elif rando1 == 0:
        if rando2 == 0:
            arr2 = arr
        else:
            arr2 = arr[rando2-1::-1] + arr[rando2:]
    # if it's some spot to the end.
    elif rando2 == len(arr) - 1:
        arr2 = arr[0:rando1] + arr[rando2:rando1-1:-1]
    # all the other middle cases
    else:
        arr2 = arr[0:rando1] + arr[rando2-1:rando1-1:-1] + arr[rando2:]

    return arr2