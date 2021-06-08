
# old travel choice function... wasn't sure if was working.
# def makeTravelChoices(ant, prob, size):
#     while len(ant) < size:
#         currCity = ant[len(ant) - 1]
#         possibilities = []
#         poss_prob = []
#         sum_pos = 0
#         for col in range(0, size): # we go through cities
#             # sees if the city is a possibility
#             if col not in ant: # matches city to tao*eta func
#                 possibilities.append(col)
#                 poss_prob.append(prob[currCity][col])
#                 sum_pos += prob[currCity][col]

#     # normalization quotient
#         poss_prob = poss_prob / sum_pos
#         # why do I need to put zero at the end here?...
#         choice = random.choices(possibilities, poss_prob)[0]
#         # for testing that things were getting selected correctly
#         # print("Choices:", possibilities, "Probs:", poss_prob)
#         ant.append(choice)