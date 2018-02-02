from random import randint
from random import random
from random import sample



# 读入的初始化数据
knapfile = 'F:\\个人文档\\人工智能\\Python\\Knapsack\\test.txt'

with open(knapfile, 'rU') as testfile:        # 变量testfile来接收这个文件，自动调用close()等方法
    lines = testfile.readlines()
n = int(lines[0])  # Number of items
c = int(lines[n+1])  # Knapsack capacity
# Dict of possible items
items = {int(line.split()[0]): tuple(map(int, line.split()))[1:] for line in lines[1:n+1]}


# 关键函数 初始化 GA parameters
max_generations = 100
K = 2               # tournament size
pX = 1              # Overall crossover rate
pU = 0.5            # Uniform crossover rate
pM = 1.1/float(n)   # Mutation rate
P = 50              # Population size
E = 2               # number of Elites

#  关键函数 变异
def mutate(human):
    """
    Takes a binary list and flips bits at a probability of pM, outputs another binary list.
    """
    xman = human[:]
    for i in range(n):
        if pM > random():
            if human[i] == 0:
                xman[i] = 1
            else:
                xman[i] = 0
    return xman

#  关键函数 交叉
def unifXover(parentA, parentB):
    """
    Takes 2 binary lists and with probablity pX performs uniform crossover at probability
    pU to produce a list of 2 new binary lists.
    """
    childA = parentA[:]
    childB = parentB[:]
    if pX > random():
        for i in range(n):
            #if (1/float(n)) > random():
            if pU > random():
                childA[i] = parentB[i]
                childB[i] = parentA[i]
    return [childA, childB]

#  计算适应度函数的weight和value的总和
def packing_info(b):  # 这个b到底是染色体的集合还是染色体
    """
    Accepts a binary list denoting packed items and returns a list of their index numbers,
    total value and total weight.
    """
    indexes = []
    total_value = 0
    total_weight = 0
    for idx, val in enumerate(b):
        if val == 1:                                # 这个为什么会为1
            indexes.append(idx+1)
            total_value += items[idx+1][0]
            total_weight += items[idx+1][1]
    return [indexes, total_value, total_weight]

#  计算value的总和
def vFitness(b):
    """
    Accepts a binary list denoting packed items and returns their total value.
    """
    total_value = 0
    for idx, val in enumerate(b):
        if val == 1:
            total_value += items[idx+1][0]
    return total_value

#  计算weight的总和
def wFitness(b):
    """
    Accepts a binary list denoting packed items and returns their total weight.
    """
    total_weight = 0
    for idx, val in enumerate(b):
        if val == 1:
            total_weight += items[idx+1][1]
    return total_weight

#  得到一个最优的个体
def tournament_selection(pop, K):
    """
    Takes population list of binary lists and tournament size and returns a winning binary list.
    """
    tBest = 'None'
    for i in range(K):
        contestant = pop[randint(0, P-1)]
        if (tBest == 'None') or vFitness(contestant) > vFitness(tBest):
            tBest = contestant[:]
    return tBest


# 这一段代码充满了奇怪？？？？？？？？？？？？？？
def initialize_population():
    """
    Generates a list of binary lists each representing a valid packing selection.
    """
    popS = set()
    while len(popS) < P:     # P是这个总群的大小 50
        b0weight = c+1       # c是这个背包客容纳的量 112648
        while b0weight > c:  # the starting population only includes valid solutions
            # 相当于是200个长度吗？？？？？？？？
            b0 = tuple(randint(0, 1) for _ in range(n))   # “_” means the last value calculated  n: Number of items
            b0weight = wFitness(b0)
        popS.add(b0)
    return [list(elem) for elem in list(popS)]  # Converts a set of tuples into a list of lists


#  选择出最后的个体            应该有个参数要传进来 ***popD***
def select_elites():
    """
    Selects the E best solutions from the population and returns them as a list of binary lists.
    """
    elites = []
    while len(elites) < E:  # Keep choosing elites until there are E of them
        new_elites = popD[max(popD)]  # These are the binary lists with the best fitness
        # If adding all the elites with this fitness would be too many, then discard the surplus at random
        while len(new_elites) > (E - len(elites)):
            new_elites.remove(sample(new_elites, 1)[0])
        elites.extend(new_elites)
        popD.pop(max(popD), None)  # Remove the key with the value just added from popD{}
    return elites


def popMean():
    """
    Calculate the mean fitness of the current generation
    """
    t = 0
    for i in popR:
        t += i[0]
    return t/P

# 输出这一代最大popD，这一代的平均适应度，这一代的最小popD
def report():
    return "max: "+str(max(popD))+", mean: "+str(popMean())+", min: "+str(min(popD))

def updateBest():
    return [max(popD), popD[max(popD)][0], s]

def rankedList():
    # Make a list of each binary list and its fitness
    return [(vFitness(i), i) for i in popL]
def rankedDict():
    # Make a dictionary where keys are fitness and values are tuples of the binary lists with that fitness
    popD = {}
    for item in popR:
        key = item[0]
        popD.setdefault(key, []).append(item[-1])
    return popD




# 主程序应该是从这里开始的  Create an initial population
popL = initialize_population()
popR = rankedList()
popD = rankedDict()
s = 0  # the generation counter
bestResults = updateBest()
print("Starting population - "+str(report()))

while True:
    s += 1
    popR = rankedList()
    popD = rankedDict()

    # Update current best
    if max(popD) > bestResults[0]:
        bestResults = updateBest()

    # Stop if optimum attained (optimum only known if enumeration was possible)
    if 'global_optimum' in globals():
        if bestResults[0] == global_optimum:
            print
            "Global Optimum reached after " + str(s) + " generations."
            break

    # Stop if time is up
    if s == max_generations:
        print
        "Stopped after " + str(s) + " generations."
        break

    # Give an update every 10% of total progress
    if s % (max_generations / 10) == 0:
        print
        "Best: " + str(bestResults[0]) + ", " + str(
            max_generations - s) + " generations remaining. Current population - " + str(report())

    # Start the child generation with E elites (direct copies from current generation)
    nextGen = select_elites()

    # Fill the next generation to size P, same size as the previous one
    while len(nextGen) < P:
        parentA = tournament_selection(popL, K)  # Selection
        parentB = tournament_selection(popL, K)
        childrenAB = unifXover(parentA, parentB)  # Crossover
        mutatedChildA = mutate(childrenAB[0])  # Mutation
        mutatedChildB = mutate(childrenAB[1])
        if (wFitness(mutatedChildA) <= c) and (wFitness(mutatedChildB) <= c):  # Discard infeasible solutions
            nextGen.extend([mutatedChildA, mutatedChildB])

    popL = nextGen[:]

packing_info = packing_info(bestResults[1])
print("\nBest feasible solution found (on generation " + str(bestResults[2]) + "/" + str(max_generations)
      + "): value=" + str(packing_info[1]) + ", weight=" + str(packing_info[2]) + "/" + str(c) + "\n"
      + str(len(packing_info[0])) + "/" + str(n) + " items: " + str(packing_info[0]))


