# from main import *
import random
import math
from tools import *

# main functino
def simuAnneal(table):
    size = table.shape[0]
    arr1 = createRandoArr(size)
    iter = 200000
    for i in range(0, iter):
        # decreasing temperature
        temp = (iter - i) / 3000 #this works good on 42
        arr2 = findNeighborSA(arr1)
        if isBetter(arr2, arr1, table):
            arr1 = arr2.copy()
        else:
            delta = findTourLen(arr1, table) - findTourLen(arr2, table)
            probability = math.exp( delta / temp)
            if decision(probability):
                print(findTourLen(arr1, table), findTourLen(arr2, table), i, probability)
                arr1 = arr2.copy()
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