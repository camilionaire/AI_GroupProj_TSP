import main
import random
import math
import PySimpleGUI as sg
import numpy


# now ACO
class Ant:
   def __init__(self, num, path, p_start, pher, distance):
       self.num = num
       self.path = path
       self.p_start = p_start
       self.pher = pher
       self.dist = distance

colony_list = []

def aco_main(my_table):
   print(my_table)
   # now the variables
   colony_size = 10  # 10,20,30,50,100,200
   max_iter = 2  # 100 200
   alpha = 1
   beta = 1
   rho = 0
   initial_pher = 0.1
   pher_dep_weight = 1
   current_iter = 1
   ant_dist = 0
   best_score = 0  # this will keep track of the best score we find
   time = 0  # this will keep track of the runtime
   print(len(my_table))
   t_range = len(my_table) - 1
   for i in range(0, colony_size):  # time to create our ants and their start points
       # rand_path = random.randint(0,t_range) #generate random ant starting point
       rand_path = 0
       Ant.num = i  # ant number
       Ant.p_start = rand_path  # where the ant will start
       Ant.pher = initial_pher  # pheromone amount ant will carry initially
       Ant.dist = ant_dist  #
       print(f'{Ant.num} {Ant.p_start} {Ant.pher} {Ant.dist}')
       ants_list = []
       ants_list.extend((Ant.num, Ant.p_start, Ant.pher, Ant.dist))
       colony_list.extend([ants_list])
       print(ants_list)
       print(colony_list)
   while (1):
       for i in colony_list:
           traversal_list = list(range(0, len(my_table)))
           path_travelled = []
           best_paths = []
           ant_results = []
           print('this is the first traversal list', traversal_list)
           print('this is the ant data', i)  # this is our first list of an individual ant data
           print('this is the ant number', i[0])  # this is the number of the ant
           print('this is the start city', i[1])  # this is the start city the ant will be placed in
           print('this is the ant pheromone', i[2])  # this is the amt of pheromone the ant has
           print('this is the distance the ant has travelled',
                 i[3])  # this is the distance the ant has travelled (initially zero)
           path_travelled.append(i[1])  # add the start point to the traversed path
           # traversal_list.remove(i[1])  # remove the option from the traversal list
           # print('This is updated traversal list', traversal_list)
           path_data = list(my_table[rand_path])  # select the correct row from the imported table
           print('This is path data', path_data)
           total = 0
           # min = 100
           for j in range(0, len(path_data)):  # should run five times for first table
               min = 100
               start_at = -1
               copy_list = traversal_list[:]
               for k in path_data[:]:
                   print('k is', k)  # get each value from the row
                   path_index = path_data.index(k, start_at + 1)  # get the index for each value
                   print(path_index)
                   if k == 0:
                       print('skip')
                   elif (k < min) and path_index not in path_travelled:  # so if we have 2 < 100 good but needs another constraint
                       min = k
                   elif (path_data.count(k) > 1):
                       start_at += 1
               print('min is ', min)
               total += min
               print('total is ', total)
               # if path_data.index(min) in traversal_list:
               # traversal_list.remove(path_data.index(min))
               print('updated traversal list is ', traversal_list)
               path_travelled.append(path_data.index(min, start_at + 1))
               print('current nodes visited', path_travelled)
               path_data[:] = list(my_table[path_data.index(min, start_at + 1)])
               if (len(path_travelled) == len(traversal_list)):  # now the table is complete
                   path_travelled.append(i[1])  # add the start point to the table
                   amount = path_travelled[-1]
                   total += path_data[amount]
                   print(path_travelled)  # now the ant finished its journey
                   print(total)  # return the total
                   ant_results.append(total)
                   total = 0 #reset total
                   path_travelled[:] = [] #reset path travelled list
                   continue

