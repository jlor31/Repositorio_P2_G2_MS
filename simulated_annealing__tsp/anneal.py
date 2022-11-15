import math
import random
import plot
import matplotlib.pyplot as plt


class Model(object):
    """
        Este objeto modela y guarda las variables para poder llevar a cabo a simulacion
    """
    def __init__(self, coords, alpha=0.995, stopping_T=1e-8, stopping_iter=100000):
        self.coords = coords
        self.N = len(coords)
        self.T = math.sqrt(self.N)
        self.stopping_T = stopping_T
        self.stopping_iter = stopping_iter
        self.alpha = alpha
        self.T_Val = self.T
        self.iteration = 1
        self.nodes = [i for i in range(self.N)]
        self.best_solution = None
        self.all_solutions = []
        self.best_fitness = float("inf")
        self.fitness_list = []
        self.cur_fitness = None
        self.cur_solution = None

def dist_nodes(node1, node2, coords):
    """
        Funcion que calcula la distancia entre dos nodos
    """
    coord_0, coord_1 = coords[node1], coords[node2]
    return math.sqrt((coord_0[0] - coord_1[0]) ** 2 + (coord_0[1] - coord_1[1]) ** 2)

def fitness(solution, model: Model):
    """
        Distancia total entre los nodos de la solucion actual
    """
    cur_fit = 0
    for i in range(model.N):
        cur_fit += dist_nodes(solution[i % model.N], solution[(i + 1) % model.N], model.coords)
    return cur_fit

def calc_initial_solution(model: Model):
    """
        Esta funcion calcula una solucion inicial para el problema, se usa el algoritmo de Greedy
    """
    rand_index = random.randint(0, model.N - 1)
    current = model.nodes[rand_index]
    sol = [model.nodes[rand_index]]
    free = [node for index, node in enumerate(model.nodes) if index != rand_index]

    while free:
        next_node = min(free, key=lambda x: dist_nodes(current, x, model.coords))
        free.remove(next_node)
        sol.append(next_node)
        current = next_node

    actual_fit = fitness(sol, model)
    if actual_fit < model.best_fitness:
        model.best_fitness = actual_fit
        model.best_solution = sol
    model.fitness_list.append(actual_fit)
    return sol, actual_fit

def accept_p(fitness, model: Model):
    """
        Este metodo calcula la probabilidad de aceptar si el candidato actual es peor que el anterior,
        este depende de la temperatura actual y la diferencia de puntuacion entre el candidato y el actual
    """
    return math.exp(-abs(fitness - model.cur_fitness) / model.T)

def accept(candidate, model: Model):
    """
        En esta funcion se comprueba si el candidato es mejor que la solucion actual, si es mejor se acepta con probabilidad 1,
        si no, se acepta con probabilidad p dependiendo de la temperatura actual y la diferencia entre el candidato y la solucion actual
    """
    candidate_fitness = fitness(candidate, model)
    if candidate_fitness < model.cur_fitness:
        model.cur_fitness, model.cur_solution = candidate_fitness, candidate

        if candidate_fitness < model.best_fitness:
            model.best_fitness, model.best_solution = candidate_fitness, candidate
    else:
        if random.random() < accept_p(candidate_fitness, model):
            model.cur_fitness, model.cur_solution = candidate_fitness, candidate

def anneal(model: Model):
    """
        Funcion que ejecuta la simulacion
    """
    model.cur_solution, model.cur_fitness = calc_initial_solution(model)

    plot_obj = plot.PlotRefresh()

    c = 1
    while model.T >= model.stopping_T and model.iteration < model.stopping_iter:
        candidate = list(model.cur_solution)
        l = random.randint(2, model.N - 1)
        i = random.randint(0, model.N - l)
        candidate[i : (i + l)] = reversed(candidate[i : (i + l)])
        accept(candidate, model)
        plot_obj.refresh([candidate], model.coords, model)
        model.T *= model.alpha
        model.iteration += 1
        model.fitness_list.append(model.cur_fitness)
        c += 1

    print("\n\nMejor puntiacion obtenida: ", model.best_fitness)
    improvement = 100 * (model.fitness_list[0] - model.best_fitness) / (model.fitness_list[0])
    print(f"mejora: {improvement : .2f}%")

def batch_anneal(model: Model, times=10):
    for i in range(1, times + 1):
        print(f"Iteration {i}/{times} -------------------------------")
        model.T = model.T_Val
        model.iteration = 1
        model.cur_solution, model.cur_fitness = calc_initial_solution(model)
        anneal(model)

def visualize_routes(model: Model):
    plot.plotTSP([model.best_solution], model.coords)

def plot_learning(model: Model):
    plt.plot([i for i in range(len(model.fitness_list))], model.fitness_list)
    plt.ylabel("Puntuacion")
    plt.xlabel("Iteraciones")
    plt.show()

def simulate(coords, alpha=0.995, stopping_T=1e-8, stopping_iter=100000):
    model = Model(coords, alpha, stopping_T, stopping_iter)
    # batch_anneal(model, 1000)
    anneal(model)
    # visualize_routes(model)
    # plot_learning(model)
    input()
