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
        if count == n and graph[currPos][0]:  # 3 + 5 = 8
            answer.append(cost + graph[currPos][0])  # 3
            all_paths.append(path)  # 1
            return  # 1
        for i in range(self.dimension):  # 1 + 1 + n(1 + 1 + 8 + n!) = n*n! + 10n + 2
            if v[i] is False and graph[currPos][i]:  # 4 + 4 + n! = n! + 8
                v[i] = True  # 2
                self.tsp_backtracking(graph, v, i, n, count + 1, cost + graph[currPos][i], 
                                      answer, path + "->" + str(i + 1), all_paths,) # n!
                v[i] = False  # 2
        # T(n) = n * n! + 10n + 10  =====> O (n * n!)