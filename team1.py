from sys import argv
from task1.task1 import find_most_queens
from task2.task2 import find_most_bishops
from task3.task3 import find_most_knights
from task4.task4 import find_most_bishops_and_knights
from task5.task5 import find_most_bishops_and_knights_with_queens

def print_board(board):
    for row in board:
        print(*row)
    bishops = sum(row.count('B') for row in board)
    knights = sum(row.count('K') for row in board)
    queens = sum(row.count('Q') for row in board)
    print(f"Bishops: {bishops}, Knights: {knights}, Queens: {queens}")

def print_result(board):
    bishops_positions = [(i, j) for i in range(len(board)) for j in range(len(board[0])) if board[i][j] == 'B']
    knights_positions = [(i, j) for i in range(len(board)) for j in range(len(board[0])) if board[i][j] == 'K']
    queens_positions = [(i, j) for i in range(len(board)) for j in range(len(board[0])) if board[i][j] == 'Q']
    if bishops_positions:
        print("bishops:", bishops_positions)
    if knights_positions:
        print("knights:", knights_positions)
    if queens_positions:
        print("queens:", queens_positions)

# print(argv)
def printboard(board):
    for row in board:
        print(row)

if __name__ == "__main__":
    task = 0
    m, n = 0, 0
    QueensPos = []
    if len(argv) > 1:
        task = int(argv[1].strip(','))
        m, n = int(argv[2].strip(',')), int(argv[3].strip(','))
        if task == 5 and len(argv) > 4:
            queens_str = ' '.join(argv[4:])
            QueensPos = eval(queens_str)
    # print(task, m, n)
    if m <= 0 or n <= 0 :
        raise ValueError("Invalid input")
    match(task):
        # Task 1: Find most Queens
        case 1:
            board = find_most_queens(m, n)
            print_result(board)
        case 2:
            board = find_most_bishops(m, n)
            print_result(board)
        # Task 3: Find most Knights
        case 3:
            board = find_most_knights(m, n)
            print_result(board)
        # Task 4: Find most Bishops and Knights
        case 4:
            board = find_most_bishops_and_knights(m, n)
            print_result(board)
        # Task 5: Find most Bishops and Knights with a given Queens
        case 5:
            # !! 輸入 Queens Postion 時請記得加上雙引號 !! 
            board, bishops, knights = find_most_bishops_and_knights_with_queens(m, n, QueensPos)
            print_result(board)
        case _:
            raise ValueError("Invalid task number")
