import matplotlib.pyplot as plt
import numpy as np
import random


# These are functions specific for solving the TSP in it's array / table 
# representation
################################################################################

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


# just standard mathy things
################################################################################

# returns true if a rando # (0, 1] is less than some prob
def decision(prob):
    return random.random() < prob


################################################################################
# plots the results of two arrays, plotted to x,y axis, automatically sizes
# and connects in said color.
def plot_results(xArray, yArray):
        plt.plot(xArray, yArray, color="blue")
        plt.show()