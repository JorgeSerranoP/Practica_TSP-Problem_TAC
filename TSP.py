import math
import random
import time

from matplotlib import pyplot as plt
from tools import read_file


class TSP:
    # Constructor de la clase
    def __init__(self):
        self.name = ""
        self.filename = ""
        self.dimension = 0
        self.problem = {}
        self.solution = []
        self.figures = 0
        self.graph = []

    # Calcula y almacena en graph las aristas (carreteras) entre ciudades (todas, dado que es un nodo completo)
    def generate_graph(self):
        self.graph = [
            [self.distance(city1, city2) for city2 in list(self.problem.keys())]
            for city1 in list(self.problem.keys())]

    # Genera un escenario a partir de un archivo .tsp.
    # Debe estar en la carpeta test y se espera que sea un archivo tsp de vertices (coordenadas), no de aristas.
    def get_graph_from_file(self, tsp_name):
        tsp_file = f"./test/{tsp_name}"
        lines = read_file(tsp_file)
        self.name = [line.partition("NAME:")[2] for line in lines if "NAME: " in line][0].strip()
        self.filename = tsp_name
        self.dimension = int([line.partition("DIMENSION:")[2]for line in lines if "DIMENSION: " in line][0])
        index_for_search = [index for index, line in enumerate(lines) if "NODE_COORD_SECTION" in line][0] + 1
        cities_data = lines[index_for_search : index_for_search + self.dimension]
        self.problem = {}
        for city in cities_data:
            idx, x, y = map(float, city.split(" "))
            self.problem[int(idx)] = (x, y)

        self.generate_graph()
        self.solution = list(self.problem.keys())
        print(f"Fichero {tsp_name} parseado con exito")

    # Si el escenario proviene de un fichero tsp, lee la solucion del archivo de
    # solucion correspondiente
    def solution_from_file(self):
        if ".tsp" not in self.filename:
            print(f"El escenario {self.name} no fue generado apartir de un archivo .tsp")
            return
        solution_file = "./test/" + self.filename.replace(".tsp", "") + ".opt.tour"
        lines = read_file(solution_file)
        index_for_search = [index for index, line in enumerate(lines) if "TOUR_SECTION" in line][0] + 1

        next_line = lines[index_for_search]
        # if else porque a veces la solucion a parece en una sola linea y a veces en varias
        if sum([str(city) in next_line for city in self.solution]) == self.dimension:
            self.solution = list(map(int, next_line.split(" ")))
        else:
            self.solution = list(map(int, lines[index_for_search : index_for_search + self.dimension]))
            print(self.solution)
        self.sort_solution()
        print(f"Solucion desde archivo: {self.compute_dist()} m")

    # Genera un escenario aleatorio de {dimension} ciudades
    def get_random(self, dimension):
        self.name = f"Aleatorio {dimension} dimensiones"
        self.dimension = dimension
        self.problem = {}
        for i in range(1, dimension + 1):
            self.problem[i] = round(random.random() * 50, 2), round(random.random() * 50, 2)
        self.generate_graph()
        self.solution = list(self.problem.keys())

    # Método para desordenar las ciudades de la solución.
    # Puede ser util para evaluar varias soluciones sobre un mismo escenario
    # pero que una soluciones no influyan sobre las otras
    def shuffle(self):
        random.shuffle(self.solution)
        self.sort_solution()

    # Solucion con algoritmo greedy
    # Devuelve el tiempo de ejecucion del algoritmo
    def greedy_solve(self):
        start = time.time()
        to_put = set(self.solution)
        new_solution = [self.solution[0]]
        to_put.remove(self.solution[0])
        while len(to_put) > 1:
            current = new_solution[-1]
            current_distance = float("inf")
            current_best = -1

            for city in to_put:
                dist = self.distance(current, city)
                if dist < current_distance:
                    current_distance = dist
                    current_best = city

            new_solution.append(current_best)
            to_put.remove(current_best)

        new_solution.append(to_put.pop())
        self.solution = new_solution
        end = time.time()
        self.sort_solution()
        print(end - start)
        return end - start

    # Solucion con 2opt
    # Devuelve el tiempo de ejecucion del algoritmo
    def opt2_solve(self):
        start = time.time()
        improved = True
        while improved:
            improved = False
            best_distance = self.compute_dist()
            for i in range(1, self.dimension - 2):
                for j in range(i + 2, self.dimension):
                    new_route = self.solution.copy()
                    new_route[i:j] = self.solution[j - 1 : i - 1 : -1]
                    new_distance = sum([self.distance(new_route[index],new_route[(index + 1) % len(new_route)],)for index in range(len(new_route))])

                    if new_distance < best_distance:
                        self.solution = new_route
                        best_distance = new_distance
                        improved = True
                    if improved:
                        break
                if improved:
                    break
        end = time.time()
        self.sort_solution()
        print(str(end - start))
        return end - start

    # Solucion con algoritmo de backtracking
    # Devuelve el tiempo de ejecucion del algoritmo
    def backtracking_solve(self):
        answer = []
        paths = []
        graph = self.graph.copy()

        v = [False for i in range(self.dimension)]
        v[0] = True

        start = time.time()
        self.tsp_backtracking(graph, v, 0, self.dimension, 1, 0, answer, "1", paths)
        self.solution = [int(x) for x in paths[answer.index(min(answer))].split("->")]
        end = time.time()

        self.sort_solution()
        print(str(end - start))
        return end - start

    def tsp_backtracking(self, graph, v, currPos, n, count, cost, answer, path, all_paths):
        """
        :param graph: matriz representando el grafo del problema
        :param v: vector booleano de nodos, true si han sido visitados, false si no.
        :param currPos: nodo actual
        :param n: número total de nodos
        :param count: número de nodos visitados
        :param cost: coste acumulado
        :param answer: lista con el coste de todas las soluciones encontradas
        :param path: recorrido local de la rama
        :param all_paths: lista con los recorridos de todas las soluciones encontradas
        :return:
        """
        if count == n and graph[currPos][0]:
            answer.append(cost + graph[currPos][0])
            all_paths.append(path)
            return
        for i in range(self.dimension):
            if v[i] is False and graph[currPos][i]:
                v[i] = True
                self.tsp_backtracking(graph, v, i, n, count + 1, cost + graph[currPos][i], answer, path + "->" + str(i + 1), all_paths,)
                v[i] = False

    def compute_dist(self):
        total_dist = 0
        for index in range(len(self.solution)):
            total_dist += self.distance(self.solution[index], self.solution[(index + 1) % len(self.solution)])
        return total_dist

    # Devuelve la distancia entre dos ciudades
    def distance(self, city1, city2):
        return math.sqrt((self.problem[city1][0] - self.problem[city2][0]) ** 2 + (self.problem[city1][1] - self.problem[city2][1]) ** 2)

    # Desplaza la solucion para que la ruta comience por la primera ciudad
    def sort_solution(self):
        primero = None
        while primero != list(self.problem.keys())[0]:
            primero = self.solution.pop(0)
            self.solution.append(primero)

        self.solution = self.solution[:-1]
        self.solution.insert(0, primero)

    # Dibuja el problema
    def draw(self):
        x = [coord[0] for coord in self.problem.values()]
        y = [coord[1] for coord in self.problem.values()]
        names = list(self.problem.keys())

        width = 9.6
        height = 7.2
        bool_dim = self.dimension > 20
        figsize = [width + (width * bool_dim), height + (height * bool_dim)]
        plt.figure(self.figures, figsize=figsize)

        self.figures += 1
        plt.scatter(x, y, s=15, marker="x", c="black")
        for txt, x_coord, y_coord in zip(names, x, y):
            plt.annotate(txt, (x_coord, y_coord))
        plt.xlim(min(x) - 1, max(x) + 1)
        plt.suptitle(f"{self.name} sin solucion", fontsize=14)

    # Dibuja el problema con la solucion actual
    def draw_with_solution(self):
        self.draw()
        for index in range(len(self.solution)):
            x_values = (self.problem[self.solution[index]][0],self.problem[self.solution[(index + 1) % len(self.solution)]][0],)
            y_values = (self.problem[self.solution[index]][1],self.problem[self.solution[(index + 1) % len(self.solution)]][1],)
            plt.plot(x_values, y_values, "red")
        plt.suptitle(f"{self.name} con solucion", fontsize=14)
        plt.title("Ruta: " + ", ".join(map(str, self.solution + [self.solution[0]])),fontsize=10,)
        plt.show()

    # Devuelve un string del problema, con el nombre, la dimension y la solucion
    def __str__(self):
        result = f"Problema {self.name}\n\t-{self.dimension} ciudades"
        result += f"\n\t-Actual solucion:\t{', '.join(map(str, self.solution))}"
        return result
