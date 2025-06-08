from sys import argv
from task5 import find_most_bishops_and_knights_with_queens
# print(argv)

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
    else: 
        with open('input.txt', 'r') as f:
            lines = f.readline().strip().split(',')
            # print(lines)
            task = int(lines[0])
            m, n = int(lines[1]), int(lines[2])
            if task == 5 and len(lines) > 3:
                queens_str = ','.join(lines[3:]).strip()
                QueensPos = eval(queens_str)
                if QueensPos == '': QueensPos = []
    
    # print(task, m, n)
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
            # 輸入 Queens Postion 時請記得加上雙引號
            board, bishops, knights = find_most_bishops_and_knights_with_queens(m, n, QueensPos)
            print("bishops:", bishops)
            print("knights:", knights)
            pass
        case _:
            raise ValueError("Invalid task number")
