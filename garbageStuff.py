
# NOTE this was all stuff that I tried, but didn't seem to be working

        # fitness = []
        # BUG, I don't know if this approach works
        # top_prob = bigBad(tao, eta, size)
    # all of the ants travel here

        # BUG this doesn't seem to work, reworking
        # for ant in colony:
        #     makeTravelChoices(ant, top_prob, size)
        #     fitness.append(findTourLen(ant, table))
        # tao = evapAndDist(colony, fitness, table, tao, size)
        # if i == 0 or (i+1) % 400 == 0:
        #     print("Gen:", i+1, "Average Fitness: ", avgFitness(colony, table))
        #     print("TAO:\n", tao)
            # print(tao)
# was doing something wrong... think was in random.choices... maybe numbers were too small and it did work... i dunno
# old travel choice function... wasn't sure if was working.
def makeTravelChoices(ant, prob, size):
    while len(ant) < size:
        currCity = ant[len(ant) - 1]
        possibilities = []
        poss_prob = []
        sum_pos = 0
        for col in range(0, size): # we go through cities
            # sees if the city is a possibility
            if col not in ant: # matches city to tao*eta func
                possibilities.append(col)
                poss_prob.append(prob[currCity][col])
                sum_pos += prob[currCity][col]

    # normalization quotient
        poss_prob = poss_prob / sum_pos
        # why do I need to put zero at the end here?...
        choice = random.choices(possibilities, poss_prob)[0]
        # for testing that things were getting selected correctly
        # print("Choices:", possibilities, "Probs:", poss_prob)
        ant.append(choice)


# NOTE... not sure the math checks out on this one...
# tao^alpha * eta^beta won't change, can do that ahead, but sum of allowed, need at decision.
# just doing the top of bad function for now.
# def bigBad(tao, eta, size):
#     prob = np.zeros((size, size))
#     for row in range(0, size):
#         for col in range(0, size):
#             prob[row][col] = pow(tao[row][col], ALPHA) * \
#                 pow(eta[row][col], BETA)

#     return prob

# # NOTE this function is currently not taking into account the fact that
# # all the tours are two possible ways.  so 1->2 pheromone != 2->1.
# def evapAndDist(colony, fit, table, tao, size):

#     deltaTao = np.zeros((size, size))
#     for ant in range(0, ANTS):
#         for i in range(0, size - 1):
#             deltaTao[colony[ant][i]][colony[ant][i+1]] += Q / fit[ant]# * table[colony[ant][i]][colony[ant][i+1]]
#         # added in for symmetric graphs
#             deltaTao[colony[ant][i+1]][colony[ant][i]] += Q / fit[ant]# * table[colony[ant][i+1]][colony[ant][i]]

#         # add in back to front here...
#         deltaTao[colony[ant][size - 1]][colony[ant][0]] += Q / fit[ant]# * table[colony[ant][size - 1]][colony[ant][0]] 
#     # added in for symmetric graphs
#         deltaTao[colony[ant][0]][colony[ant][size - 1]] += Q / fit[ant]# * table[colony[ant][0]][colony[ant][size - 1]] 
   
#     # evaporate and add in new stuff.
#     for row in range(0, size):
#         for col in range(0, size):
#             tao[row][col] = (tao[row][col] + deltaTao[row][col]) * (1 - RHO)

#     return tao