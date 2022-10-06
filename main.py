from branch_and_bound import branchAndBound
from TSP import TSP

if __name__ == '__main__':
    tsp = TSP()
    fichero = "ulysses16.tsp"
    tsp.get_graph_from_file(fichero)
    tsp.draw()
    tsp.solution_from_file()
    tsp.draw_with_solution()
    tsp.shuffle()

    print("----------------------------------------------------------------------------------")
    print("-------------------------- PRUEBAS BACKTRACKING ----------------------------------")
    print("----------------------------------------------------------------------------------")
    for _ in range(10):
        print(".................. Iteracion: " + str(_) + "..............................")
        for i in range(2, 13):
            tsp = TSP()
            tsp.get_random(i)
            tsp.backtracking_solve()
            # tsp.draw_with_solution()

    print("----------------------------------------------------------------------------------")
    print("---------------------------- PRUEBAS BRANCH & BOUND ------------------------------")
    print("----------------------------------------------------------------------------------")
    for _ in range(10):
        print(".................. Iteracion: " + str(_) + "..............................")
        for i in range(2,15):
            tsp = TSP()
            tsp.get_random(i)
            branchAndBound(tsp)
            # tsp.draw_with_solution()

    print("----------------------------------------------------------------------------------")
    print("---------------------------- PRUEBAS GREEDY --------------------------------------")
    print("----------------------------------------------------------------------------------")
    for i in range(100,2000, 100):
        tsp = TSP()
        tsp.get_random(i)
        tsp.greedy_solve()
        # tsp.draw_with_solution()

    print("----------------------------------------------------------------------------------")
    print("------------------------------ PRUEBAS OPT ---------------------------------------")
    print("----------------------------------------------------------------------------------")
    for _ in range(10):
        print(".................. Iteracion: " + str(_) + "..............................")
        for i in range(10, 110, 10):
            tsp = TSP()
            tsp.get_random(i)
            tsp.opt2_solve()
            # tsp.draw_with_solution()