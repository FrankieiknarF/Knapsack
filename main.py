from defunc import initialize_population
from defunc import decoding
from defunc import selection
from defunc import crossover
from defunc import mutation
from defunc import findbest

popSize = 50            # 种群数量
chromLen = 8            # 染色体长度
generation = 100        # 遗传代数

crossoverRatio = 0.8    # 交叉概率
mutationRatio = 0.2     # 变异概率

# 初始化一个种群
populations = initialize_population(popSize, chromLen)

i = 0
while i < generation:
    # 各个个体适应度的计算
    fitness = decoding(populations)
    # 选择
    select_populations = selection(fitness, populations)
    # 交叉
    cross_populations = crossover(select_populations, crossoverRatio)
    # 变异
    mutat_populations = mutation(cross_populations, mutationRatio)
    # 重赋值 进行循环
    populations = mutat_populations
    i += 1

# 对最后一次的种群转化为10进制，剔除“限制”大于期望的项目，对剩下的项目按“收益”排序，取最大收益的个体
Fitness = decoding(populations)
best = findbest(Fitness)

print(best)




