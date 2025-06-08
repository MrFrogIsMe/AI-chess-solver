from task2_simulated_annealing import find_most_bishops_simulated_annealing

def findmostBishops(m, n):
    return find_most_bishops_simulated_annealing(m, n, k=100, alpha=2, beta=1)