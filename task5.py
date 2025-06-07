
from task5_observation import find_most_bishops_and_knights_with_queens_observation
from task5_hill_climbing import find_most_bishops_and_knights_with_queens_hill_climbing
from task5_simulated_annealing import find_most_bishops_and_knights_with_queens_simulated_annealing
def find_most_bishops_and_knights_with_queens(m, n, QueensPos):
    # board, count_bishops, count_knights = find_most_bishops_and_knights_with_queens_observation(m, n, QueensPos)
    # board, count_bishops, count_knights = find_most_bishops_and_knights_with_queens_hill_climbing(m, n, QueensPos)
    board, count_bishops, count_knights = find_most_bishops_and_knights_with_queens_simulated_annealing(m, n, QueensPos)
    # for row in board:
    #     print(*row)
    # print("number of bishops:", count_bishops)
    # print("number of knights:", count_knights)
    return board
find_most_bishops_and_knights_with_queens(10, 10, [(0, 0), (3, 1)])