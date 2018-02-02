import random

# 初始化一组数据，如果地表数据就不需要
def initialize_population(popSize, chromLen):
    pops = [[]]
    for popNum in range(popSize):
        temp = []
        for chromNum in range(chromLen):
            temp.append(random.randint(0, 1))
        pops.append(temp)
    return pops[1:]

# 进行解码，就是之前的2进制转换成10进制，并得到相应的限制值和价值
def decoding(populations):
    dic = {0: (1, 3), 1: (2, 5), 2: (3, 4), 3: (4, 2), 4: (5, 6), 5: (6, 1), 6: (7, 2), 7: (8, 3)}
    Fit = []
    for individual in populations:
        fitness = 0
        weight = 0
        position = 0
        for i in individual:
            if i == 1:
                fitness += dic[position][1]
                weight += dic[position][0]
                position += 1
            else:
                position += 1
        Fit.append((weight, fitness))
    return Fit

# 选择要进行适应度的计算 背包的capacity不超过15
def selection(fitness, populations):
    # capacity超过15的项先删除
    pos = 0
    dic_pos = 0
    fitness_pop = {}
    fitness_new = []

    while pos < len(fitness):
        if fitness[pos][0] <= 15:
            fitness_pop[dic_pos] = populations[pos]
            dic_pos += 1
            fitness_new.append(fitness[pos])
        pos += 1

    fitness_total = 0
    fitness_cum = []
    fitness_ave = []
    # fitness总和 这里都是value的总和
    for i in fitness_new:
        fitness_total += i[1]
    # 新fitness jijijijji
    for i in fitness_new:
         fitness_ave.append(i[1]/fitness_total)
    # fitness积累值
    i = 0
    while i < len(fitness_new)-2:           # 最后一项单独赋值，确保正确
        j = 0
        cum = 0
        while j <= i:                       # 累加i之前的所有项的概率
            cum += fitness_ave[j]
            j += 1
        fitness_cum.append(cum)
        i += 1
    fitness_cum.append(1.0)   # 累加到最后一项的概率肯定是1


    # 轮盘赌的方式进行重复生成新的种群pops
    populations_new = []
    i = 0
    while len(populations_new) < len(populations):         # 要得到原始populations的个数
        rand_num = random.uniform(0, 1)                     # 随机生成0到1之间的数，
        if rand_num > 0:                                    # 如果不是0，
            while i < len(fitness_pop):                     # 则循环去确认小于哪个累积量，则提取该累积量i+1的原始种群
                if rand_num <= fitness_cum[i]:
                    populations_new.append(fitness_pop[i])
                    i = 0
                    break
                else:
                    i += 1
        else:
            populations_new.append(fitness_pop[0])
    return(populations_new)

# 进行交叉 前一个和后一个交叉 本试验用单点交叉
def crossover(select_populations, crossoverRatio):
    for i in range(len(select_populations)-1):
        px = random.uniform(0, 1)
        if px < crossoverRatio:
            cPoint = random.randint(0, 8)                    # 单点交叉的位置
            temp1 = []
            temp2 = []
            temp1.extend(select_populations[i][0:cPoint])
            temp1.extend(select_populations[i+1][cPoint:len(select_populations[i])])
            temp2.extend(select_populations[i+1][0:cPoint])
            temp2.extend(select_populations[i][cPoint:len(select_populations[i])])
            select_populations[i] = temp1
            select_populations[i+1] = temp2
    return select_populations

# 进行变异 随机基因的随机位数进行变异
def mutation(cross_populations, mutationRatio):
       for i in range(len(cross_populations)):
           if random.uniform(0, 1) < mutationRatio:
               mPoint = random.randint(0, 7)                # 这里有8个染色体，就应该是0-7
               if cross_populations[i][mPoint] == 1:
                   cross_populations[i][mPoint] = 0
               else:
                   cross_populations[i][mPoint] = 1
       return cross_populations

# 剔除“限制”大于期望的项目(这里的期望为15)，对剩下的项目按“收益”排序，取最大收益的个体
def findbest(Fitness):
    pos = 0
    fitness_new = []
    while pos < len(Fitness):
        if Fitness[pos][0] <= 15:
            fitness_new.append(Fitness[pos])
        pos += 1

    fitness_new.sort(key=lambda x:x[1])

    return fitness_new[len(fitness_new)-1]