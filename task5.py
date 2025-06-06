
from observation import find_most_bishops_and_knights_with_queens_observation

def find_most_bishops_and_knights_with_queens(m, n, QueensPos):
    board, count_bishops, count_knights = find_most_bishops_and_knights_with_queens_observation(m, n, QueensPos)
    for i in range(m): print(board[i])
    print("number of bishops:", count_bishops)
    print("number of knights:", count_knights)
    return board