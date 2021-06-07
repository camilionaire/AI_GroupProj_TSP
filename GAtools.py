from tools import *

# mutation funtion, although may need rewrite
################################################################################

def mutate2(child):
    # TODO was thinking maybe a slice where we do a permutation
    # of the numbers in the middle, might be more extreme than
    # original mutate... not doing enough.
    pass

# NOTE this mutate func, while it does work... doesn't do so great.
# Needs something a little more mutatety.
def mutate(child):
    length = len(child)# - 1
    cut1 = random.randint(0, length)
    cut2 = random.randint(0, length)
    if cut2 < cut1:
        cut1, cut2 = cut2, cut1
    # checks for edge cases
    if cut1 == cut2: # if are same cut, child lucks out
        newChild = child
    elif cut1 == 0 and cut2 == length: # complete reversal also lucks out
        newChild = child[::-1]
    else: # checks for edge cases
        if cut1 == 0:
            newChild = child[cut2-1::-1] + child[cut2:]
        elif cut2 == length:
            newChild = child[:cut1] + child[:cut1 - 1:-1] 
        else: # middle 'normal' switch cases
            newChild = child[:cut1] + child[cut2 - 1:cut1 - 1:-1] + child[cut2:]

    return newChild


# parent choosing and cross over function
################################################################################

# total is the sum of diff, diff is each in pop's score.
def chooseParents(pop, total, diff):
    # if we reached homogeny
    if total == 0:
        return pop[0], pop[1]

    # this acts like a spin wheel, total = wheel size,
    # diff array acts like slices for each member of pop
    choice1 = random.randint(1, total)
    choice2 = random.randint(1, total)
    found1, found2 = False, False

    # spin the wheel around 1 time
    for i in range(0, len(pop)):
        choice1 -= diff[i] # like flipper 1
        choice2 -= diff[i] # like flipper 2
        if choice1 <= 0 and not found1:
            parent1 = pop[i]
            found1 = True
        if choice2 <= 0 and not found2:
            parent2 = pop[i]
            found2 = True

    return parent1, parent2

# takes slice of par 1, fills in rest with par2        
def crossOver(par1, par2):
    length = len(par1)
    cut1 = random.randint(0, length) # spot 0 to 25 (example)
    cut2 = random.randint(0, length) # spot 0 to 25 
    if cut2 < cut1:
        cut1, cut2 = cut2, cut1

    child = [-1 for col in range(length)] # pos 0 to 24 (example)

    if cut1 == cut2: #takes after par2 edge case?
        child = par2
    else:
        for i in range(cut1, cut2): # from smallest 0 to 25
            child[i] = par1[i]
        j = 0
        for i in range(0, length):
            if child[i] == -1:
                while par2[j] in child:
                    j += 1
                child[i] = par2[j]

    return child

## Math tools for the genetic algorithm
################################################################################

# this gets an array of lengths from the population
def getLenArray(pop, table):
    tourLen = []
    for i in pop:
        tourLen.append(findTourLen(i, table))
    return tourLen

# finds a populations average fitness.
def avgFitness(pop, table):
    total = 0
    for i in pop:
        total += findTourLen(i, table)
    return total / len(pop)


################################################################################
################################################################################
################################################################################