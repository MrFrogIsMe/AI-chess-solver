from task2_dfs import find_most_bishops_dfs
from task2_hill_climbing import find_most_bishops_hill_climbing
from task2_simulated_annealing import find_most_bishops_simulated_annealing

def find_most_bishops(m, n):
    # return find_most_bishops_dfs(m, n)
    # return find_most_bishops_hill_climbing(m, n)
    return find_most_bishops_simulated_annealing(m, n, alpha=2, beta=1)