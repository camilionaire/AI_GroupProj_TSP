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
from ga import ga_main

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


def pass_filename(option1, option2):
    my_table = []
    if option1 == 1:
        my_table = np.loadtxt('five19.txt')
        print("File loaded: five19.txt")
    elif option1 == 2:
        my_table = np.loadtxt('twentysix937.txt')
        print("File loaded: ftwentysix937.txt")
    elif option1 == 3:
        my_table = np.loadtxt('fortytwo699.txt')
        print("File loaded: fortytwo699.txt")
    elif option1 == 4:
        my_table = np.loadtxt('fortyeight33523.txt')
        print("File loaded: fortyeight33523.txt")
    else:
        print("Invalid input for dataset selection")
    call_algorithm(option2, my_table)


def call_algorithm(option2, my_table):
    print(option2)
    if option2 == 1:
        ga_main(my_table)
    elif option2 == 2:
        hillClimb = simuAnneal(my_table)
        print(hillClimb)
        print(findTourLen(hillClimb, my_table))
    elif option2 == 3:
        print("calling ACO")


def main():
    # uses np for numpy, loads the file and makes a table!
    # this is the command right after python ./main.py ________ <here
    # if len(sys.argv) == 2:
    #     my_table = np.loadtxt(sys.argv[1])
    # else:
    #

    option1 = input("Please select the number of cities: \n 1. 5: (Best result: 19) \n 2. 26: (Best result: 937)\n 3. 42: (Best result: 699) \n 4. 48: (Best result: 33523) \n")
    option2 = input("Please choose the algorithm to solve the TSP: \n 1. Genetic Algorithm. \n 2. Simulated Annealing Algorithm.\n 3. Ant colony optimization \n")

    pass_filename(int(option1), int(option2))


if __name__ == "__main__":
    main()