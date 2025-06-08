from .task1_dfs import find_most_queens_dfs
from .task1_hill_climbing import find_most_queens_hill_climbing
from .task1_simulated_annealing import find_most_queens_simulated_annealing

def find_most_queens(m, n):
    # print("m = ", m, "n = ", n)
    # board, count = dfs(m, n)
    # return find_most_queens_hill_climbing(m, n)
    return find_most_queens_simulated_annealing(m, n)
