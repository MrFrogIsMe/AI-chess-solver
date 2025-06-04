import math
import random

def findmostBishops(m, n):
    return find_most_bishops_simulated_annealing(m, n)

def find_most_bishops_simulated_annealing(m, n, max_steps=10000, start_temp=10.0, end_temp=0.01, cooling_rate=0.995):
    def is_valid(board, x, y):
        dirs = [(-1,-1), (-1,1), (1,-1), (1,1)]
        for dx, dy in dirs:
            i, j = x+dx, y+dy
            while 0 <= i < m and 0 <= j < n:
                if board[i][j] == 'B':
                    return False
                i += dx
                j += dy
        return True

    # 隨機產生初始解
    board = [['.']*n for _ in range(m)]
    # 隨機放一些 bishop
    for _ in range(min(m, n)):
        i, j = random.randint(0, m-1), random.randint(0, n-1)
        if board[i][j] == '.' and is_valid(board, i, j):
            board[i][j] = 'B'
    best = [r[:] for r in board]
    best_count = sum(row.count('B') for row in board)
    curr_count = best_count
    temp = start_temp

    for step in range(max_steps):
        # 隨機選一個 bishop 移除，或隨機嘗試加一個 bishop
        new_board = [r[:] for r in board]
        action = random.choice(['add', 'remove', 'move'])
        if action == 'add':
            empties = [(i, j) for i in range(m) for j in range(n) if new_board[i][j] == '.']
            if empties:
                i, j = random.choice(empties)
                if is_valid(new_board, i, j):
                    new_board[i][j] = 'B'
        elif action == 'remove':
            bishops = [(i, j) for i in range(m) for j in range(n) if new_board[i][j] == 'B']
            if bishops:
                i, j = random.choice(bishops)
                new_board[i][j] = '.'
        else:  # move
            bishops = [(i, j) for i in range(m) for j in range(n) if new_board[i][j] == 'B']
            empties = [(i, j) for i in range(m) for j in range(n) if new_board[i][j] == '.']
            if bishops and empties:
                bi, bj = random.choice(bishops)
                ei, ej = random.choice(empties)
                new_board[bi][bj] = '.'
                if is_valid(new_board, ei, ej):
                    new_board[ei][ej] = 'B'
                else:
                    new_board[bi][bj] = 'B'  # move fail, revert
        new_count = sum(row.count('B') for row in new_board) if all(
            is_valid(new_board, i, j) for i in range(m) for j in range(n) if new_board[i][j] == 'B') else -1
        delta = new_count - curr_count
        if delta >= 0 or random.random() < math.exp(delta / (temp + 1e-9)):
            board = [r[:] for r in new_board]
            curr_count = new_count if new_count >= 0 else curr_count
            if curr_count > best_count:
                best = [r[:] for r in board]
                best_count = curr_count
        temp *= cooling_rate
        if temp < end_temp:
            break
    print(f"simulated annealing 最大num_bishops: {best_count}")
    count = sum(row.count('B') for row in best)
    return best, count