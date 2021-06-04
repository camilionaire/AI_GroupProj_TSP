# from main import *
import random
import math
from tools import *

################################################################################
ITERATIONS = 200000
TEMP_MOD = 3000
################################################################################
# TEMP_MOD:
# 500 works good for the 48 city with big distances
# 3000 works good for 42 and 26 puzzles
# I suspect everything works good for 5 city puzzle


# main function
def simuAnneal(table):
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
        else:
            delta = findTourLen(arr1, table) - findTourLen(arr2, table)
            # the math part of function e^delt/T
            probability = math.exp( delta / temp)
            # will make a non improving choice depending on prob.
            if decision(probability):
                arr1 = arr2.copy()
        if i == 0 or (i+1) % 10000 == 0:
            print("iteration:", i+1, "tour length:", findTourLen(arr1, table))
        # NOTE this is the part that stores the table to be displayed.
        if i == 0 or (i+1) % 2000 == 0:
            xArray.append(i+1)
            yArray.append(findTourLen(arr1, table))

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