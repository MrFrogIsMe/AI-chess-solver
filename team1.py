from sys import argv

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
        print("Bishops positions:", bishops_positions)
    if knights_positions:
        print("Knights positions:", knights_positions)
    if queens_positions:
        print("Queens positions:", queens_positions)

if __name__ == "__main__":
    task = 0
    m, n = 0, 0
    if len(argv) > 1:
        task = int(argv[1].strip(','))
        m, n = int(argv[2].strip(',')), int(argv[3].strip(','))
    else: 
        with open('input.txt', 'r') as f:
            lines = f.readline().strip().split(',')
            task = int(lines[0])
            m, n = int(lines[1]), int(lines[2])
    match(task):
        # Task 1: Find most Queens
        case 1:
            pass
        # Task 2: Find most Bishops
        case 2:
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