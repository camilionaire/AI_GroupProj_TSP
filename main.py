################################################################################
#
#  Initial set up for travelling salesperson problem to eventually make a few
#  AI algorithms to solve it.
#
################################################################################
from aGoAtACO import antColonyOpt
import numpy as np
from simAnTSP import *
from ga import ga_main
from newGA import geneticAlgorithm
import PySimpleGUI as sg


def pass_filename(option1, option2):
    my_table = []
    if option1 == 1:
        my_table = np.loadtxt('./datasets/five19.txt')
        print("File loaded: five19.txt")
    elif option1 == 2:
        my_table = np.loadtxt('./datasets/twentysix937.txt')
        print("File loaded: ftwentysix937.txt")
    elif option1 == 3:
        my_table = np.loadtxt('./datasets/fortytwo699.txt')
        print("File loaded: fortytwo699.txt")
    elif option1 == 4:
        my_table = np.loadtxt('./datasets/fortyeight33523.txt')
        print("File loaded: fortyeight33523.txt")
    else:
        print("Invalid input for dataset selection")
    call_algorithm(option2, my_table)


def call_algorithm(option2, my_table):
    print(option2)
    if option2 == 1:
        ga_main(my_table)
        # geneticAlgorithm(my_table)
    elif option2 == 2:
        # get's the solution to the problem
        hillClimb = simuAnneal(my_table)
        # prints out the solution to the problem
        print("\nThe final path we found is:\n", hillClimb)
        print("\nIt's path length is: ", findTourLen(hillClimb, my_table), "\n")
    elif option2 == 3:
        print("calling ACO\n")
        antColonyOpt(my_table)


def main():
    # uses np for numpy, loads the file and makes a table!
    # this is the command right after python ./main.py ________ <here
    # if len(sys.argv) == 2:
    #     my_table = np.loadtxt(sys.argv[1])
    # else:
    #

    #option1 = input("Please select the number of cities: \n 1. 5: (Best result: 19) \n 2. 26: (Best result: 937)\n 3. 42: (Best result: 699) \n 4. 48: (Best result: 33523) \n")
    #option2 = input("Please choose the algorithm to solve the TSP: \n 1. Genetic Algorithm. \n 2. Simulated Annealing Algorithm.\n 3. Ant colony optimization \n")

    #pass_filename(int(option1), int(option2))
    event, values = sg.Window('Please select the number of cities: \n', [[sg.Text('Select one -> '), sg.Listbox(
        ['1. 5: (Best result: 19)', '2. 26: (Best result: 937)', '3. 42: (Best result: 699)',
         '4. 48: (Best result: 33523)'], size=(30, 4), key='citynum')], [sg.Button('Ok'), sg.Button('Cancel')]]).read(
        close=True)
    if event == 'Ok':
        print(values['citynum'])
        num = str(values['citynum'])
        option1 = num[2:3]
        print(num)
        print(option1)
        event2, values2 = sg.Window('Please choose the algorithm to solve the TSP: \n',
                                    [[sg.Text('Select one -> '), sg.Listbox(
                                        ['1. Genetic Algorithm.',
                                         '2. Simulated Annealing Algorithm.',
                                         '3. Ant Colony Optimization'],
                                        size=(40, 3),
                                        key='algorithm')],
                                     [sg.Button('Ok'),
                                      sg.Button('Cancel')]]).read(
            close=True)
        if event2 == 'Ok':
            print(values2['algorithm'])
            num2 = str(values2['algorithm'])
            option2 = num2[2:3]
            print(num2)
            print(option2)
            pass_filename(int(option1), int(option2))
        else:
            sg.popup_cancel('user cancelled')
            exit()
    else:
        sg.popup_cancel('user cancelled')
        exit()

if __name__ == "__main__":
    main()
