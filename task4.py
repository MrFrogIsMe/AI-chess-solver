from task4_simulated_annealing import find_most_bishops_and_knights_simulated_annealing

def find_most_bishops_and_knights(m, n):
    return find_most_bishops_and_knights_simulated_annealing(m, n, alpha=20, beta=10, cooling_rate=0.999)
