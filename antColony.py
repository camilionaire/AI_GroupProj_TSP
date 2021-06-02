from main import *
import random
import math


# GOAL/ CHANGES:
# instead of using createRandoArr to get new path,
# make it so the ant chooses which city to travel to from
# current city based on pheromone + distance


# change pheromone increase from increasing pheromone for whole path
# -> increasing pheromone after path between 2cities has been used by ant


# add evaporation of pheromone on path between cities ....

#node keeping track of each path + info for that path
class pathNode:
    def __init__(self, path, distance, pheromone, count):
        self.path=path #path taken
        self.distance=distance #total distance for path
        self.pheromone=pheromone #pheromone for that path
        self.count=count #number of ants that have gone on that path
    def __repr__(self):
        return f'pathNode({self.path},{self.distance},{self.pheromone})'

def antColony(table):
    print('testing')
    exit()
    size = table.shape[0]

    #total number of ants
    colony_size = 20;

    #max num of iterations
    iterations= 200;

    #pheromone initial val
    tau= .5;

    #pheromone exponential weight
    Alpha = 1;

    #pheromone heristic weight
    beta = 1;

    #pheromone evaporation weight
    rho =0.05;



    #first ant goes on random path
    ant1 = createRandoArr(size)
    path_temp=ant1;
    totalAnts=1 #total ants who've gone on path

    #save in node
    antLength=findTourLen(ant1, table)
    bestPath = pathNode(ant1,antLength, tau, 1);

    #array holding each better path taken (only if it is new best path)
    allPaths=[]
    allPaths.append(bestPath)
    all_index =0;

    #droping each ant
    for i in range(colony_size):

        #next ant chooses rand path
        ant2= createRandoArr(size);
        totalAnts +=1;
        flag=0; # =1 if path has already been saved in allPaths
        matchingIndex=0; #index of which from allPaths that matched new path

        #checking if new path matches any saved paths from allPaths
        for i in range (all_index):
            #if match is found
            if(ant2 == allPaths[i].path):
                flag=1; #note current node is a duplicate
                matchingIndex=i; #where it is saved in allPaths
                #increase total num ants who've choosen this path
                allPaths[i].count+=1;

#!!!!! instead of using isbetter - choose new path based on probability !!!!#

        def newpath():
            print('Hello')


        #chech if new path is better than the last best path
        if isBetter(ant2, path_temp, table):
            path_temp=ant2;

            #if this path is a duplicate
            if flag == 1:
                #get paths pheromone
                tau_temp= allPaths[matchingIndex].pheromone;

                #calculate pheromone based on this equation:
                #   = (1-(evaporation))*current pheromone + num ants * (current Pheromone)^total ants on this path so far
                pher=(1-rho)*tau_temp + (colony_size * tau_temp**allPaths[matchingIndex].count);

                #update pheromone of path already in allPaths
                allPaths[all_index].pheromone = pher;

            #if path is new
            else:
                #save new best path as node
                bestPath = pathNode(ant2,findTourLen(ant2, table), tau, 1)
                #   save node in allPaths array
                allPaths.append(bestPath)
                all_index +=1;


        #if current ants path is NOT better then the last best
        else:
            #get paths pheromone
            tau_temp= allPaths[all_index].pheromone;

            #calculate pheromone based on this equation:
            #   = (1-(evaporation))*current pheromone + num ants * (current Pheromone)^total ants on this path so far
            pher=(1-rho)*tau_temp + (colony_size * tau_temp**allPaths[all_index].count)

            #update pheromone of on last best path
            allPaths[all_index].pheromone = pher;


    #displaying information for each path in allPaths
    for i in range(all_index+1):
        print(allPaths[i].path, "distance : ", allPaths[i].distance, "pher: ", allPaths[i].pheromone)

    #most recent path saved will be best found -> return
    return allPaths[all_index].path;

