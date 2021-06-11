# Jason

from GAtools import avgFitness, getLenArray
from tools import *
import numpy as np
import random
import warnings  # this module is being used to get rid of the runtime warning
import time
import PySimpleGUI as sg

# 5puzzle: ant=10, iters=5000, 1, 1, 1, .1, alpha=1, beta=2
# 26puzzle: ANTS=20, ITERS=1000, INIT_PHER/ETA_VAR=100
# Q = 937, ALPHA=2, BETA=2 works sometimes, falls into local minima
# 48puzzle: ants=100, iters=200, 1, 900, 900, .1, alpha=2, beta=2 under 40k.
# ^^^ not consistent tho, fails to local minima sometimes.'
# adding menus for variable selection


punctuations = '''[',]'''
event, values = sg.Window('Please select the number of ants: \n', [[sg.Text('Select one -> '), sg.Listbox(
    ['1. 10', '2. 20', '3. 100',
     '4. 200'], size=(30, 4), key='antnum')], [sg.Button('Ok'), sg.Button('Cancel')]]).read(
    close=True)
if event == 'Ok':
    print(values['antnum'])
    num = str(values['antnum'])
    option1 = num[4:] #get just the number back
    only_numstring = ''
    for char in option1:
        if char not in punctuations:
            only_numstring += char
            print(only_numstring)
    print(only_numstring)
    ANTS = int(only_numstring) #put this value into ANTS variable
    event2, values2 = sg.Window('Please choose the max number of iterations: \n',
                                [[sg.Text('Select one -> '), sg.Listbox(
                                    ['1. 100',
                                     '2. 200',
                                     '3. 1000',
                                     '4. 5000'],
                                    size=(40, 4),
                                    key='maxiter')],
                                 [sg.Button('Ok'),
                                  sg.Button('Cancel')]]).read(
        close=True)
    if event2 == 'Ok':
        print(values2['maxiter'])
        num2 = str(values2['maxiter'])
        option2 = num2[4:]
        only_numstring = ''
        for char in option2:
            if char not in punctuations:
                only_numstring += char
                print(only_numstring)
        ITERS = int(only_numstring)
        event3, values3 = sg.Window('Please select the init pher: \n', [[sg.Text('Select one -> '), sg.Listbox(
            ['1. 0', '2. 1', '3. 2',
             '4. 5'], size=(30, 4), key='initpher')], [sg.Button('Ok'),
                                                                             sg.Button('Cancel')]]).read(
            close=True)
        if event3 == 'Ok':
            print(values3['initpher'])
            num3 = str(values3['initpher'])
            option3 = num[4:]
            only_numstring = ''
            for char in option3:
                if char not in punctuations:
                    only_numstring += char
                    print(only_numstring)
            INIT_PHER = int(only_numstring)
            event4, values4 = sg.Window('Please choose the value for Q and ETA_VAR: \n',
                                        [[sg.Text('Select one -> '), sg.Listbox(
                                            ['1. 900',
                                             '2. 800',
                                             '3. 700',
                                             '4. 600'],
                                            size=(40, 4),
                                            key='q_eta')],
                                         [sg.Button('Ok'),
                                          sg.Button('Cancel')]]).read(
                close=True)
            if event4 == 'Ok':
                print(values4['q_eta'])
                num4 = str(values4['q_eta'])
                option4 = num4[4:]
                only_numstring = ''
                for char in option4:
                    if char not in punctuations:
                        only_numstring += char
                        print(only_numstring)
                print(num4)
                Q = int(only_numstring)
                ETA_VAR = int(only_numstring)
                event5, values5 = sg.Window('Please select values for rho: \n',
                                          [[sg.Text('Select one -> '), sg.Listbox(
                                              ['1. 0', '2. .01',
                                               '3. .1',
                                               '4. .2'], size=(30, 4), key='rho')],
                                           [sg.Button('Ok'), sg.Button('Cancel')]]).read(
                    close=True)
                if event5 == 'Ok':
                    print(values5['rho'])
                    num5 = str(values5['rho'])
                    option5 = num5[4:]
                    only_numstring = ''
                    for char in option5:
                        if char not in punctuations:
                            only_numstring += char
                            print(only_numstring)
                    RHO = float(only_numstring)
                    event6, values6 = sg.Window('Please choose the values for alpha and beta: \n',
                                                [[sg.Text('Select one -> '), sg.Listbox(
                                                    ['1. 1',
                                                     '2. 2',
                                                     '3. 3',
                                                     '4. 4'],
                                                    size=(40, 4),
                                                    key='alphabeta')],
                                                 [sg.Button('Ok'),
                                                  sg.Button('Cancel')]]).read(
                        close=True)
                    if event6 == 'Ok':
                        print(values6['alphabeta'])
                        num6 = str(values6['alphabeta'])
                        option6 = num6[4:]
                        only_numstring = ''
                        for char in option6:
                            if char not in punctuations:
                                only_numstring += char
                                print(only_numstring)
                        ALPHA = int(only_numstring)
                        BETA = int(only_numstring)
                    else:
                        sg.popup_cancel('user cancelled')
                        exit()
                else:
                    sg.popup_cancel('user cancelled')
                    exit()

            else:
                sg.popup_cancel('user cancelled')
                exit()
        else:
            sg.popup_cancel('user cancelled')
            exit()

    else:
        sg.popup_cancel('user cancelled')
        exit()
else:
    sg.popup_cancel('user cancelled')
    exit()

#ANTS = 96
#ITERS = 200
#INIT_PHER = 1  # init put on tao
#Q = 900  # pher put down along path like Q?... maybe have it optimal sol?
#ETA_VAR = 900  # eta found by this divided by length?
#RHO = .1  # standard rho
#ALPHA, BETA = 1, 4
# TITLE = './datasets/five19.txt'
# TITLE = './datasets/twentysix937.txt'
TITLE = './datasets/fortytwo699.txt'
# TITLE = './datasets/fortyeight33523.txt'


'''def createAnt chooses a random city for ant to start in'''


def createAnt(size):
    start_pos = random.randint(0, size - 1)
    ant = [start_pos]  # assigns to beg city.
    return ant


'''for function createEta, Eta is set to reciprocal of table w/0's on diag '''


def createETA(table, size):
    eta = np.zeros((size, size))  # ETA is computed at beginning of function from table & distances between cities
    for row in range(0, size):  # both ETA and TAO are tables that will be the size of the table examined.
        for col in range(0, size):
            if row != col:
                eta[row][col] = ETA_VAR / table[row][col]
    # div by zero along axis warning error fixed using warnings module!
    # with warnings.catch_warnings():
    #    warnings.simplefilter('ignore')
    #    eta = np.reciprocal(table) * ETA_VAR
    #    for diag in range(0, size):
    #        eta[diag][diag] = 0
    return eta


'''for function createTAO, tao initially set to INIT_PHER, will change throughout func.'''


def createTAO(size):
    tao = np.full((size, size), INIT_PHER)  # TAO is set at beginning based on size of table, init to all 1's (no ants!)
    for diag in range(0, size):
        tao[diag][diag] = 0
    return tao


'''for function goTravel'''


def goTravel(ant, tao, eta, size):
    while len(ant) < size:
        currCity = ant[len(ant) - 1]
        possibilities = []
        sum = 0
        for city in range(0, size):
            if city not in ant:
                possibilities.append(city)  # possible city
                sum += pow(tao[currCity][city], ALPHA) * pow(eta[currCity][city], BETA)

        rand = random.uniform(0, sum)  # creates roulette wheel...
        wheelNeedle = 0

        for city in possibilities:
            wheelNeedle += pow(tao[currCity][city], ALPHA) * pow(eta[currCity][city], BETA)
            if wheelNeedle >= rand:
                ant.append(city)
                break
    return ant


'''for function updatePheromones, '''


def updatePheromones(ant, tao, table, mult):
    size = table.shape[0]
    tour = findTourLen(ant, table)
    delta = Q / tour
    # this is one directional... doesn't update other way.
    for city in range(0, size - 1):
        tao[ant[city]][ant[city + 1]] += delta * mult
        tao[ant[city + 1]][ant[city]] += delta * mult  # for symmetric graphs
    tao[ant[city + 1]][ant[0]] += delta * mult
    tao[ant[0]][ant[city + 1]] += delta * mult
    return tao


'''evapPheromones function will keep track of the pheromone that evaporates as the ants travel from city to city'''


def evapPheromones(tao):
    return tao * (1 - RHO)


'''antColonyOpt function gets the time for ACO, '''


def antColonyOpt(table):
    ## TESTING / PRINTING DATA #####################################################
    start = time.time()  # getting start times
    bestEver = 99999999  # best tour so far
    bestie = []  # path of best tour
    greatestGen = 0  # gen best is found
    xArray, yArray = [], []
    ################################################################################
    size = table.shape[0]  # finds size of map
    print("TABLE AVERAGE", np.average(table))
    eta = createETA(table, size)
    tao = createTAO(size)

    # print("ETA:\n", eta)
    # print("TAO:\n", tao)

    # for the number of... eventually iterations
    for i in range(0, ITERS):
        colony = []
        for j in range(0, ANTS):
            ant = createAnt(size)
            colony.append(ant)
        # if i % 200 == 0:
        #     print("COLONY B4 TRAVEL:", colony)
        for ant in colony:
            ant = goTravel(ant, tao, eta, size)

        antsLen = getLenArray(colony, table)
        bestGen = min(antsLen)
        bestInGen = colony[antsLen.index(bestGen)]
        if bestGen < bestEver:
            bestEver = bestGen
            bestie = bestInGen
            greatestGen = i + 1

        if i == 0 or (i + 1) % 10 == 0:
            avg = avgFitness(colony, table)
            # avg = np.average(antsLen)
            print("GEN:", str(i + 1).zfill(4), "AVG FIT: {:.2f}".format(avg))
            xArray.append(i + 1)
            yArray.append(avg)
        # if (i+1) % 500 == 0:
        #     print("NEW TAO, HOPEFULLY:")
        #     print(tao)
        tao = evapPheromones(tao)
        for ant in colony:
            # NOTE giving it a little bit of elitism here.
            if ant == bestie:
                mult = 4
            # if ant == bestInGen:
            elif ant == bestInGen:
                mult = 2
            else:
                mult = 1
            tao = updatePheromones(ant, tao, table, mult)

    # NOTE TESTING INFORMATION, CAN BE COMMENTED / ADJUSTED
    # print("FINAL TAO: \n", tao)
    file = open("finalTao.txt", "w")
    for row in tao:
        file.write(str(row) + "\n")
    print("FINAL COLONY AFTER TRAVEL:")
    for ant in colony:
        print(ant, "fitness:", findTourLen(ant, table))
    print("\nFINAL GEN:", str(i + 1).zfill(4), "AVG FIT: {:.2f}".format(avgFitness(colony, table)))

    print("Best Tour:", bestEver, " Found in Gen:", greatestGen)
    print("Path: ", bestie)

    elapsed = time.time() - start
    print("\nACO ran in {:.3f} seconds".format(elapsed))
    plot_results(xArray, yArray)


'''main function gets the correct city table and sends it to the antColonyOpt function'''


def main():
    table = np.loadtxt(TITLE)  # get the correct table
    antColonyOpt(table)  # call the antColonyOpt function with table param


if __name__ == "__main__":
    main()