import matplotlib.pyplot as p
from pyamaze import maze, agent
from random import randint
from copy import deepcopy
def rand():
    for i in population:
        i[-1] = randint(0, 1)
def generate_pop():
    roww,col= rows,columns
    if rows > columns:
        roww, col = col, roww
    for _ in range(pop_size):
        pop = []
        pop.append(1)
        for _ in range(1, col-1):
            pop.append(randint(1, roww))
        pop.append(roww)
        pop.append(randint(0, 1))
        population.append(pop)
def mutation():
    roww,col= rows,columns
    if rows > columns:
        roww, col = col, roww
    for i in range(0, pop_size):
        index = randint(1, col-2)
        population[i][index] = randint(1, roww)
def crossover():
    roww,col= rows,columns
    if rows > columns:
        roww, col = col, roww
    for i in range(0, (pop_size//2), 2):
        a = deepcopy(population[i])
        b = deepcopy(population[i+1])
        r = randint(1, col-2)
        for j in range(r, col):
            a[j], b[j] = b[j], a[j]
        population[(pop_size//2)+(i)] = a
        population[(pop_size//2)+(i+1)] = b
def turns():
    roww,col= rows,columns
    if rows > columns:
        roww, col = col, roww
    for i in population:
        turns = 0
        for j in range(0, col-2):
            if i[j] != i[j+1]:
                turns += 1
        turns_list.append(turns+1)
def Fitness():
    turns()
    p = []
    if rows <= columns:
        for i in population:
            for j in range(columns-1):
                if i[j+1]-i[j] >= 0:
                    for k in range(i[j], i[j+1]+1):
                        if i[-1] == 0:
                            p.append((k, j+1))  # col_col
                        elif i[-1] == 1:
                            p.append((k, j+2))  # col_row
                if i[j+1]-i[j] < 0:
                    for k in range(i[j], i[j+1]-1, -1):
                        if i[-1] == 0:
                            p.append((k, j+1))
                        elif i[-1] == 1:
                            p.append((k, j+2))
            if i[-1] == 0:
                p.append((rows, columns))
            if i[-1] == 1:
                p.insert(0, (1, 1))
            path.append(p)
            p = []
    if rows > columns:
        for i in population:
            for j in range(rows-1):
                if i[j+1]-i[j] >= 0:
                    for k in range(i[j], i[j+1]+1):
                        if i[-1] == 0:
                            p.append((j+1, k))  # row_row
                        elif i[-1] == 1:
                            p.append((j+2, k))  # row_col
                if i[j+1]-i[j] < 0:
                    for k in range(i[j], i[j+1]-1, -1):
                        if i[-1] == 0:
                            p.append((j+1, k))
                        elif i[-1] == 1:
                            p.append((j+2, k))
            if i[-1] == 0:
                p.append((rows, columns))
            if i[-1] == 1:
                p.insert(0, (1, 1))
            path.append(p)
            p = []
# **********************************************
    obs = 0
    for i in path:
        for j in range(len(i)-1):
            a, b = i[j]
            c, d = i[j+1]
            # For rows obstacles
            if c-a > 0 and b == d:
                if MAP[(a, b)]["S"] == 0:
                    obs += 1
            if c-a < 0 and b == d:
                if MAP[(a, b)]["N"] == 0:
                    obs += 1
            # For columns obstacles
            if d-b > 0 and c == a:
                if MAP[(a, b)]["E"] == 0:
                    obs += 1
            if d-b < 0 and c == a:
                if MAP[(a, b)]["W"] == 0:
                    obs += 1
        obstacles.append(obs)
        obs = 0
# **********************************************
    # steps
    for i in path:
        no_of_steps.append(len(i)-1)
# **********************************************
    w_obs = 3
    w_turn = 2
    w_path = 2
    for i in range(pop_size):
        f1 = 1-((obstacles[i]-min(obstacles))/(max(obstacles)-min(obstacles)))
        f2 = 1-((turns_list[i]-min(turns_list)) /
                (max(turns_list)-min(turns_list)))
        f3 = 1 - ((no_of_steps[i]-min(no_of_steps)) /
                  (max(no_of_steps)-min(no_of_steps)))
        f4 = (100 * w_obs * f1) * \
            (((w_path * f3) + (w_turn * f2)) / (w_path + w_turn))
        final_fitness.append(f4)
def Parent():
    for i in range(pop_size-1):
        for j in range(i+1, pop_size):
            if final_fitness[j] > final_fitness[i]:
                final_fitness[i], final_fitness[j] = final_fitness[j], final_fitness[i]
                population[i], population[j] = population[j], population[i]
def solution():
    paath = []
    for i in range(pop_size):
        if final_fitness[i] >= 0 and obstacles[i] == 0:
            paath = path[i]
            for m in range(len(paath)-1):
                final_path.update({paath[m+1]: paath[m]})
            return 1
    return 0
# **********************************************************
rows = 10
columns = 10
pop_size = 400
# ****************************************
m = maze(rows, columns)
m.CreateMaze(pattern=None, loopPercent=100, theme="dark")
a = agent(m, filled=True, footprints=True, shape="arrow", color="yellow")
MAP = m.maze_map
i = 0
population = []
generate_pop()
while True:
    path = [];obstacles=[];no_of_steps=[];turns_list=[];final_path={};final_fitness=[]
    i += 1
    Fitness()
    if solution():
        print(f"Solution found in iteration = {i}")
        m.tracePath({a: final_path})
        m.run()
        break
    Parent()
    crossover()
    mutation()
    rand()


x = [i for i in range(1, 401)]
# p.plot(x, turns_list, color="r")
# p.plot(x, obstacles, color="y")
# p.plot(x, no_of_steps, color="g")
# p.xlabel("Population")
# p.ylabel("Red->Turns   Yellow->Obstacles    Green->Number-of-Steps")
# p.title("Graph Between Population and Turns, Obstacles and Number-of-steps")
# p.show()

# p.plot(x, turns_list, color="b")
# p.xlabel("Population")
# p.ylabel("Number of Turns")
# p.title("Graph Between Population vs Turns")
# p.show()

# p.plot(x, obstacles, color="b")
# p.xlabel("Population")
# p.ylabel("Obstacles")
# p.title("Graph Between Population vs Obstacles")
# p.show()

# p.plot(x, no_of_steps, color="b")
# p.xlabel("Population")
# p.ylabel("Number of Steps")
# p.title("Graph Between Population vs Number of steps")
# p.show()
