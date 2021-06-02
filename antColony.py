from main import *
import random
import math
import PySimpleGUI as sg


# GOAL/ CHANGES:
# instead of using createRandoArr to get new path,
# make it so the ant chooses which city to travel to from
# current city based on pheromone + distance


# change pheromone increase from increasing pheromone for whole path
# -> increasing pheromone after path between 2cities has been used by ant


# add evaporation of pheromone on path between cities ....

# node keeping track of each path + info for that path
class pathNode:
    def __init__(self, path, distance, pheromone, count):
        self.path = path  # path taken
        self.distance = distance  # total distance for path
        self.pheromone = pheromone  # pheromone for that path
        self.count = count  # number of ants that have gone on that path

    def __repr__(self):
        return f'pathNode({self.path},{self.distance},{self.pheromone})'

    def ant_eval(colony_size, iterations, alpha, beta, rho, init_pher, pher_weight, table):
        print(f'{colony_size}, {iterations}, {alpha}, {beta}, {rho}, {init_pher}, {pher_weight}')



'''Function get_values will ask the user to select the values for colonysize,
maxiterations, alpha, beta, rho, initial pheromone and pheromone deposit weight'''
def get_values(table):
    punctuations = '''[',]'''
    event, values = sg.Window('Please select the ant colony size: \n', [[sg.Text('Select one -> '), sg.Listbox(
        ['1. 10', '2. 20', '3. 30', '4. 50', '5. 100', '6. 200'], size=(30, 6), key='colsize')],
                                                                        [sg.Button('Ok'), sg.Button('Cancel')]]).read(
        close=True)
    if event == 'Ok':
        print(values['colsize'])
        num = str(values['colsize'])
        option1 = num[4:]
        only_numstring = '' #we want to just get the number back as a string without brackets, quotations, etc
        print(num)
        print(option1)
        for char in option1:
            if char not in punctuations:
                only_numstring += char
        print(only_numstring)
        event2, values2 = sg.Window('Please choose the number of iterations: \n',
                                    [[sg.Text('Select one -> '), sg.Listbox(
                                        ['1. 50',
                                         '2. 100',
                                         '3. 200',
                                         '4. 300',
                                         '5. 500'],
                                        size=(40, 5),
                                        key='iteration')],
                                     [sg.Button('Ok'),
                                      sg.Button('Cancel')]]).read(
            close=True)
        if event2 == 'Ok':
            print(values2['iteration'])
            num2 = str(values2['iteration'])
            option2 = num2[4:]
            print(num2)
            print(option2)
            only_numstring2 = ''  # we want to just get the number back as a string without brackets, quotations, etc
            for char in option2:
                if char not in punctuations:
                    only_numstring2 += char
            print(only_numstring2)
            event3, values3 = sg.Window('Please choose pheromone exponential weight (alpha): \n',
                                        [[sg.Text('Select one -> '), sg.Listbox(
                                            ['1. 1',
                                             '2. 2',
                                             '3. 3',
                                             '4. 4',
                                             '5. 5',
                                             '6. 10',
                                             '7. 15'],
                                            size=(45, 7),
                                            key='alpha')],
                                         [sg.Button('Ok'),
                                          sg.Button('Cancel')]]).read(
                close=True)
            if event3 == 'Ok':
                print(values3['alpha'])
                num3 = str(values3['alpha'])
                option3 = num3[4:]
                only_numstring3 = ''  # we want to just get the number back as a string without brackets, quotations, etc
                for char in option3:
                    if char not in punctuations:
                        only_numstring3 += char
                print(only_numstring3)
                event4, values4 = sg.Window('Please choose pheromone heuristic weight(beta): \n',
                                            [[sg.Text('Select one -> '), sg.Listbox(
                                                ['1. 1',
                                                 '2. 2',
                                                 '3. 3',
                                                 '4. 4',
                                                 '5. 5',
                                                 '6. 10',
                                                 '7. 15'],
                                                size=(45, 7),
                                                key='beta')],
                                             [sg.Button('Ok'),
                                              sg.Button('Cancel')]]).read(
                    close=True)
                if event4 == 'Ok':
                    print(values4['beta'])
                    num4 = str(values4['beta'])
                    option4 = num4[4:]
                    print(num4)
                    print(option4)
                    only_numstring4 = ''  # we want to just get the number back as a string without brackets, quotations, etc
                    for char in option4:
                        if char not in punctuations:
                            only_numstring4 += char
                    print(only_numstring4)
                    event5, values5 = sg.Window('Please choose the pheromone evaporation rate(rho): \n',
                                                [[sg.Text('Select one -> '), sg.Listbox(
                                                    ['1. 0',
                                                     '2. 0.001',
                                                     '3. 0.01',
                                                     '4. 0.05',
                                                     '5. 0.1',
                                                     '6. 0.2',
                                                     '7. 0.5'],
                                                    size=(45, 7),
                                                    key='rho')],
                                                 [sg.Button('Ok'),
                                                  sg.Button('Cancel')]]).read(
                        close=True)
                    if event5 == 'Ok':
                        print(values5['rho'])
                        num5 = str(values5['rho'])
                        option5 = num5[4:]
                        only_numstring5 = ''  # we want to just get the number back as a string without brackets, quotations, etc
                        for char in option5:
                            if char not in punctuations:
                                only_numstring5 += char
                        print(only_numstring5)
                        event6, values6 = sg.Window('Please choose the initial pheromone: \n',
                                                    [[sg.Text('Select one -> '), sg.Listbox(
                                                        ['1. 0',
                                                         '2. 1',
                                                         '3. 2',
                                                         '4. 5',
                                                         '5. 10',
                                                         '6. 20',
                                                         '7. 50'],
                                                        size=(40, 7),
                                                        key='initpher')],
                                                     [sg.Button('Ok'),
                                                      sg.Button('Cancel')]]).read(
                            close=True)
                        if event6 == 'Ok':
                            print(values6['initpher'])
                            num6 = str(values6['initpher'])
                            option6 = num6[4:]
                            only_numstring6 = ''  # we want to just get the number back as a string without brackets, quotations, etc
                            for char in option6:
                                if char not in punctuations:
                                    only_numstring6 += char
                            print(only_numstring6)
                            event7, values7 = sg.Window('Please choose the pheromone deposit weight: \n',
                                                        [[sg.Text('Select one -> '), sg.Listbox(
                                                            ['1. 1',
                                                             '2. 2',
                                                             '3. 5',
                                                             '4. 10',
                                                             '5. 20',
                                                             '6. 50'],
                                                            size=(40, 6),
                                                            key='pherweight')],
                                                         [sg.Button('Ok'),
                                                          sg.Button('Cancel')]]).read(
                                close=True)
                            if event7 == 'Ok':
                                print(values7['pherweight'])
                                num7 = str(values7['pherweight'])
                                option7 = num7[4:]
                                only_numstring7 = ''  # we want to just get the number back as a string without brackets, quotations, etc
                                for char in option7:
                                    if char not in punctuations:
                                        only_numstring7 += char
                                print(only_numstring7)

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
    else:
        sg.popup_cancel('user cancelled')
        exit()
    exit()


# GOAL/ CHANGES:
# instead of using createRandoArr to get new path,
# make it so the ant chooses which city to travel to from
# current city based on pheromone + distance


# change pheromone increase from increasing pheromone for whole path
# -> increasing pheromone after path between 2cities has been used by ant


# add evaporation of pheromone on path between cities ....

# node keeping track of each path + info for that path
class pathNode:
    def __init__(self, path, distance, pheromone, count):
        self.path = path  # path taken
        self.distance = distance  # total distance for path
        self.pheromone = pheromone  # pheromone for that path
        self.count = count  # number of ants that have gone on that path

    def __repr__(self):
        return f'pathNode({self.path},{self.distance},{self.pheromone})'


def antColony(table):
    size = table.shape[0]

    colony_size = 20  # total number of ants
    iterations = 200  # max num of iterations
    tau = .5;  # pheromone initial val

    # pheromone exponential weight
    Alpha = 1;

    # pheromone heristic weight
    beta = 1;

    # pheromone evaporation weight
    rho = 0.05;

    # first ant goes on random path
    ant1 = createRandoArr(size)
    path_temp = ant1;
    totalAnts = 1  # total ants who've gone on path

    # save in node
    antLength = findTourLen(ant1, table)
    bestPath = pathNode(ant1, antLength, tau, 1);

    # array holding each better path taken (only if it is new best path)
    allPaths = []
    allPaths.append(bestPath)
    all_index = 0;

    # droping each ant
    for i in range(colony_size):

        # next ant chooses rand path
        ant2 = createRandoArr(size);
        totalAnts += 1;
        flag = 0;  # =1 if path has already been saved in allPaths
        matchingIndex = 0;  # index of which from allPaths that matched new path

        # checking if new path matches any saved paths from allPaths
        for i in range(all_index):
            # if match is found
            if (ant2 == allPaths[i].path):
                flag = 1;  # note current node is a duplicate
                matchingIndex = i;  # where it is saved in allPaths
                # increase total num ants who've choosen this path
                allPaths[i].count += 1;

        # !!!!! instead of using isbetter - choose new path based on probability !!!!#

        def newpath():
            print('Hello')

        # chech if new path is better than the last best path
        if isBetter(ant2, path_temp, table):
            path_temp = ant2;

            # if this path is a duplicate
            if flag == 1:
                # get paths pheromone
                tau_temp = allPaths[matchingIndex].pheromone;

                # calculate pheromone based on this equation:
                #   = (1-(evaporation))*current pheromone + num ants * (current Pheromone)^total ants on this path so far
                pher = (1 - rho) * tau_temp + (colony_size * tau_temp ** allPaths[matchingIndex].count);

                # update pheromone of path already in allPaths
                allPaths[all_index].pheromone = pher;

            # if path is new
            else:
                # save new best path as node
                bestPath = pathNode(ant2, findTourLen(ant2, table), tau, 1)
                #   save node in allPaths array
                allPaths.append(bestPath)
                all_index += 1;


        # if current ants path is NOT better then the last best
        else:
            # get paths pheromone
            tau_temp = allPaths[all_index].pheromone;

            # calculate pheromone based on this equation:
            #   = (1-(evaporation))*current pheromone + num ants * (current Pheromone)^total ants on this path so far
            pher = (1 - rho) * tau_temp + (colony_size * tau_temp ** allPaths[all_index].count)

            # update pheromone of on last best path
            allPaths[all_index].pheromone = pher;

    # displaying information for each path in allPaths
    for i in range(all_index + 1):
        print(allPaths[i].path, "distance : ", allPaths[i].distance, "pher: ", allPaths[i].pheromone)

    # most recent path saved will be best found -> return
    return allPaths[all_index].path;
