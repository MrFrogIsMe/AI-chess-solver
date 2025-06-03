from sys import argv
from task1 import findmostQueens
from task2 import findmostBishops

print(argv)
def printboard(board):
    for row in board:
        print(*row)

if __name__ == "__main__":
    task = 0
    m, n = 0, 0
    if len(argv) > 1:
        task = int(argv[1].strip(','))
        m, n = int(argv[2].strip(',')), int(argv[3].strip(','))
    else: 
        with open('input.txt', 'r') as f:
            lines = f.readline().strip().split(',')
            print(lines)
            task = int(lines[0])
            m, n = int(lines[1]), int(lines[2])
    print(task, m, n)
    if m <= 0 or n <= 0 :
        raise ValueError("Invalid input")
    # board = [[0]*n for _ in range(m)]
    match(task):
        # Task 1: Find most Queens
        case 1:
            board = findmostQueens(m, n)
            printboard(board)
            pass
        # Task 2: Find most Bishops
        case 2:
            board = findmostBishops(m, n)
            printboard(board)
            pass
        # Task 3: Find most Knights
        case 3:
            pass
        # Task 4: Find most Bishops and Knights
        case 4:
            pass
        # Task 5: Find most Bishops and Knights with a given Queens
        case 5:
            pass
        case _:
            raise ValueError("Invalid task number")
