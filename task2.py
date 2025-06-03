import random

def findmostBishops(m, n):
    return find_most_bishops_ori(m, n)
    # return find_most_bishops_dfs(m, n)
    return find_most_bishops_hill_climbing(m, n)
    # return find_most_bishops_random_restart_hill_climbing(m, n)
    return find_most_bishops_simulated_annealing(m, n)

def find_most_bishops_ori(m, n):
    board = [[0]*n for _ in range(m)]
    if m <= n:
        for i in range (0, n, m):
            for j in range (m):
                board[j][i] = 1
    else:
        for i in range (0, m, n):
            for j in range (n):
                board[i][j] = 1
    
    if m == n:
        for i in range (1, n-1): board[i][m-1] = 1
    # for i in range (m): print(board[i])
    print(f"find_most_bishops_ori: {sum(sum(row) for row in board)}")
    return board


def find_most_bishops_dfs(m, n):
    board = [['.']*n for _ in range(m)]
    attack_cnt = [[0]*n for _ in range(m)]
    max_found = 0
    best_board = None
    def update_diagonals(x, y, delta):
        # ↖
        i, j = x-1, y-1
        while i >= 0 and j >= 0:
            attack_cnt[i][j] += delta
            i -= 1
            j -= 1
        # ↗
        i, j = x-1, y+1
        while i >= 0 and j < n:
            attack_cnt[i][j] += delta
            i -= 1
            j += 1
        # ↙
        i, j = x+1, y-1
        while i < m and j >= 0:
            attack_cnt[i][j] += delta
            i += 1
            j -= 1
        # ↘
        i, j = x+1, y+1
        while i < m and j < n:
            attack_cnt[i][j] += delta
            i += 1
            j += 1

    def dfs(pos, num_bishops):
        nonlocal max_found, best_board
        if num_bishops > max_found:
            max_found = num_bishops
            best_board = [r[:] for r in board]
        if pos >= m * n:
            return
        for k in range(pos, m * n):
            i, j = divmod(k, n)
            if attack_cnt[i][j] == 0 and board[i][j] == '.':
                board[i][j] = 'B'
                update_diagonals(i, j, 1)
                dfs(k + 1, num_bishops + 1)
                board[i][j] = '.'
                update_diagonals(i, j, -1)
        # dfs(pos + 1, num_bishops)

    dfs(0, 0)
    print(f"最大num_bishops: {max_found}")
    return best_board if best_board else board

def find_most_bishops_hill_climbing(m, n, max_steps=1000):
    def is_valid(board, x, y):
        # 只檢查 (x, y) 這個 bishop 是否安全
        dirs = [(-1,-1), (-1,1), (1,-1), (1,1)]
        for dx, dy in dirs:
            i, j = x+dx, y+dy
            while 0 <= i < m and 0 <= j < n:
                if board[i][j] == 'B':
                    return False
                i += dx
                j += dy
        return True

    board = [['.']*n for _ in range(m)]
    best = [r[:] for r in board]
    best_count = 0

    for step in range(max_steps):
        improved = False
        # 嘗試加一個 bishop
        for i in range(m):
            for j in range(n):
                if board[i][j] == '.' and is_valid(board, i, j):
                    board[i][j] = 'B'
                    count = sum(row.count('B') for row in board)
                    if count > best_count:
                        best = [r[:] for r in board]
                        best_count = count
                        improved = True
                    else:
                        board[i][j] = '.'
        if not improved:
            break
    print(f"hill climbing 最大num_bishops: {best_count}")
    return best

def find_most_bishops_random_restart_hill_climbing(m, n, restarts=20, max_steps=1000):
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

    best_overall = None
    best_count = 0

    for _ in range(restarts):
        board = [['.']*n for _ in range(m)]
        best = [r[:] for r in board]
        count = 0
        for step in range(max_steps):
            improved = False
            for i in range(m):
                for j in range(n):
                    if board[i][j] == '.' and is_valid(board, i, j):
                        board[i][j] = 'B'
                        new_count = sum(row.count('B') for row in board)
                        if new_count > count:
                            best = [r[:] for r in board]
                            count = new_count
                            improved = True
                        else:
                            board[i][j] = '.'
            if not improved:
                break
        if count > best_count:
            best_count = count
            best_overall = [r[:] for r in best]
    print(f"random restart hill climbing 最大num_bishops: {best_count}")
    return best_overall

def find_most_bishops_simulated_annealing(m, n, max_steps=10000, start_temp=10.0, end_temp=0.01, cooling_rate=0.995):
    import math
    import random
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
    return best
