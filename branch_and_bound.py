import time

from TSP import TSP


def copyToFinal(curr_path, final_path, N):
    final_path[: N + 1] = curr_path[:]
    final_path[N] = curr_path[0]


# Funcion heuristica, para podar las ramas del algoritmo en profundidad
def heuristics(tsp: TSP, visited):
    nodosTotales = tsp.dimension
    visitados = 0
    for i in range(nodosTotales):
        if visited[i]:
            visitados += 1
    bound = nodosTotales - visitados
    return bound


def TSPRec(tsp: TSP, curr_weight, level, curr_path, visited, final_path, final_res):
    if level == tsp.dimension:
        curr_res = curr_weight + tsp.graph[curr_path[level - 1]][curr_path[0]]
        if curr_res < final_res[0]:
            copyToFinal(curr_path, final_path, tsp.dimension)
            final_res[0] = curr_res
        return

    for i in range(tsp.dimension):
        if tsp.graph[curr_path[level - 1]][i] != 0 and visited[i] == False:
            curr_weight += tsp.graph[curr_path[level - 1]][i]
            curr_bound = heuristics(tsp, visited)  # Aqui se hace la llamada a la heuristica

            if curr_bound + curr_weight < final_res[0]:
                curr_path[level] = i
                visited[i] = True
                TSPRec(tsp, curr_weight, level + 1, curr_path, visited, final_path, final_res,)

            curr_weight -= tsp.graph[curr_path[level - 1]][i]
            visited = [False] * len(visited)
            for j in range(level):
                if curr_path[j] != -1:
                    visited[curr_path[j]] = True


# Ejecuta el algoritmo de ramificacion y poda (branch and bound) con heuristica
def branchAndBound(tsp):
    start = time.time()
    final_path = [None] * (tsp.dimension + 1)
    curr_path = [-1] * (tsp.dimension + 1)
    visited = [False] * tsp.dimension
    visited[0] = True
    curr_path[0] = 0
    final_res = [float("inf")]
    TSPRec(tsp, 0, 1, curr_path, visited, final_path, final_res)
    tsp.solution = list(map(lambda x: x + 1, final_path[:-1]))
    end = time.time()

    print(str(end - start))
    return end - start
