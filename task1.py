import random
# attacked[0]: row
# attacked[1]: col
# attacked[2]: main diagonal
# attacked[3]: anti diagonal
attacked = [set() for _ in range(4)]

def is_safe(row, col):
    if row in attacked[0]: return False         # check row
    if col in attacked[1]: return False         # check col
    if row + col in attacked[2]: return False   # check main diagonal
    if row - col in attacked[3]: return False   # check anti diagonal
    return True

def hill_climbing(board, m, n):
    by_row = m <= n
    limit = m if by_row else n
    # random put min(m,n) queens
    queens = []
    for i in range(limit):
        j = random.randint(0, n-1) if by_row else random.randint(0, m-1)
        row = i if by_row else j
        col = j if by_row else i
        board[row][col] = 1
        queens.append((row, col))
    def conflicts(row, col, queens):
        for qr, qc in queens:
            if qr == row or qc == col or qr+qc == row+col or qr-qc == row-col:
                return True
        return False
    max_steps = 1000
    for step in range(max_steps):
        conflict_queens = []
        for idx, (row, col) in enumerate(queens):
            board[row][col] = 0
            if conflicts(row, col, [q for i, q in enumerate(queens) if i != idx]):
                conflict_queens.append(idx)
            board[row][col] = 1
        if not conflict_queens:
            break
        idx = random.choice(conflict_queens)
        row, col = queens[idx]
        board[row][col] = 0
        # 移動到新位置
        candidates = [(r, c) for r in range(m) for c in range(n) if board[r][c] == 0 and not conflicts(r, c, [q for i, q in enumerate(queens) if i != idx])]
        if not candidates:
            board[row][col] = 1
            continue
        new_row, new_col = random.choice(candidates)
        queens[idx] = (new_row, new_col)
        board[new_row][new_col] = 1
    count = sum(1 for i in range(m) for j in range(n) if board[i][j] == 1)
    return board, count

def random_restart_hill_climbing(board, m, n):
    best = None
    max_queens = 0
    restart = 20
    for _ in range(restart):
        board, count = hill_climbing(board, m, n)
        if count > max_queens:
            max_queens = count
            best = board
    return best

def simulated_annealing(board, m, n):
    start_temp = 10.0
    end_temp = 0.01
    cooling_rate = 0.995
    max_steps = 1000
    by_row = m <= n
    limit = m if by_row else n
    def conflicts(row, col, queens):
        for qr, qc in queens:
            if qr == row or qc == col or qr+qc == row+col or qr-qc == row-col:
                return True
        return False
     # random put min(m,n) queens
    queens = []
    for i in range(limit):
        j = random.randint(0, n-1) if by_row else random.randint(0, m-1)
        row = i if by_row else j
        col = j if by_row else i
        board[row][col] = 1
        queens.append((row, col))
    best = board
    best_count = sum(1 for i in range(m) for j in range(n) if board[i][j] == 1)
    curr_count = best_count
    temp = start_temp
    for step in range(max_steps):
        new_board = [[0]*n for _ in range(m)]
        action = random.choice(['add', 'remove', 'move'])
        
    pass

def dfs(board, idx, m, n, by_row):
    by_row = m <= n
    limit = m if by_row else n
    if idx == limit: return board
    for i in range(n if by_row else m):
        row = idx if by_row else i
        col = i if by_row else idx
        if is_safe(row, col):
            board[row][col] = 1
            attacked[0].add(row)
            attacked[1].add(col)
            attacked[2].add(row + col)
            attacked[3].add(row - col)
            result = dfs(board, idx+1, m, n, by_row)
            if result: return result
            board[row][col] = 0
            attacked[0].remove(row)
            attacked[1].remove(col)
            attacked[2].remove(row + col)
            attacked[3].remove(row - col)
    return None

def findmostQueens(m, n):
    print("m = ", m, "n = ", n)
    board = [[0]*n for _ in range(m)]
    # return dfs(board, 0, m, n, m <= n)
    # result, count = hill_climbing(board, m, n)
    return random_restart_hill_climbing(board, m, n)
    # return simulated_annealing(board, m, n)
    for row in result: print(row)
    print(count)

findmostQueens(100, 100)