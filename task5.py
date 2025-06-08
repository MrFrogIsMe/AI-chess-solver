
from task5_observation import find_most_bishops_and_knights_with_queens_observation
from task5_hill_climbing import find_most_bishops_and_knights_with_queens_hill_climbing
from task5_simulated_annealing import find_most_bishops_and_knights_with_queens_simulated_annealing
def find_most_bishops_and_knights_with_queens(m, n, QueensPos):
    # board, count_bishops, count_knights = find_most_bishops_and_knights_with_queens_observation(m, n, QueensPos)
    # board = find_most_bishops_and_knights_with_queens_hill_climbing(m, n, QueensPos)
    board = find_most_bishops_and_knights_with_queens_simulated_annealing(m, n, QueensPos)
    bishops = [(j, i) for j in range(n) for i in range(m) if board[i][j] == 'B']
    knights = [(j, i) for j in range(n) for i in range(m) if board[i][j] == 'K']
    # for row in board: print(*row)
    return board, bishops, knights