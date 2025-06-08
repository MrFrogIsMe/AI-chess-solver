import math
import random

bishop_moves = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
knight_moves = [(-1, -2), (-1, 2), (1, -2), (1, 2), (-2, -1), (-2, 1), (2, -1), (2, 1)]

def find_most_bishops_and_knights_with_queens_simulated_annealing(
        m, n, QueensPos, 
        max_steps=None, alpha=10, beta=10, 
        start_temp=None, end_temp=None, cooling_rate=None
):
    # 動態參數調整
    if start_temp is None or start_temp == -1:
        start_temp = m * n * 2
    if end_temp is None or end_temp == -1:
        end_temp = max(1, m * n * 0.01)
    if cooling_rate is None:
        cooling_rate = 0.9995 if m * n > 100 else 0.999
    if max_steps is None:
        max_steps = m * n * 300

    def is_valid_board(board):
        for i in range(m):
            for j in range(n):
                if board[i][j] == 'B':
                    # Check diagonals for conflicts
                    for dx, dy in bishop_moves:
                        x, y = i + dx, j + dy
                        while 0 <= x < m and 0 <= y < n:
                            if board[x][y] != '.' and board[x][y] != 'X':
                                return False
                            x += dx
                            y += dy
                elif board[i][j] == 'K' :
                    # Check knight moves for conflicts
                    for dx, dy in knight_moves:
                        x, y = i + dx, j + dy
                        if 0 <= x < m and 0 <= y < n and board[x][y] != '.' and board[x][y] != 'X':
                            return False
        return True
    def init_attack_cnt(board):
        attack_cnt = [[0]*n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                if board[i][j] != '.':
                    update_attack_cnt(attack_cnt, i, j, 1, board[i][j])
        return attack_cnt

    def update_attack_cnt(attack_cnt, i, j, delta, piece):
        if piece == 'B':
            for dx, dy in bishop_moves:
                x, y = i + dx, j + dy
                while 0 <= x < m and 0 <= y < n:
                    attack_cnt[x][y] += delta
                    x += dx
                    y += dy
        elif piece == 'K':
            for dx, dy in knight_moves:
                x, y = i + dx, j + dy
                if 0 <= x < m and 0 <= y < n:
                    attack_cnt[x][y] += delta
    def cost(board, attack_cnt):
        num_bishops = sum(row.count('B') for row in board)
        num_knights = sum(row.count('K') for row in board)
        conflict = 0
        for i in range(m):
            for j in range(n):
                if board[i][j] in ['B', 'K'] and attack_cnt[i][j] > 0:
                    conflict += attack_cnt[i][j]
        safe_count = 0
        for i in range(m):
            for j in range(n):
                if board[i][j] in ['B', 'K'] and attack_cnt[i][j] == 0:
                    safe_count += 1
        return -num_bishops - num_knights + alpha * conflict + beta * safe_count

    board = [['.'] * n for _ in range(m)]
    # place queens
    for qc, qr in QueensPos:
        if qr < 0 or qr >= m or qc < 0 or qc >= n:
            print("Invalid Queen position")
            return
        board[qr][qc] = 'Q'
        for i in range(m): 
            if board[i][qc] == '.': board[i][qc] = 'X'
        for i in range(n): 
            if board[qr][i] == '.':board[qr][i] = 'X'
        for d in range(1, max(m, n)):
            for dr, dc in [(-d, -d), (-d, d), (d, -d), (d, d)]:
                r, c = qr + dr, qc + dc
                if 0 <= r < m and 0 <= c < n and board[r][c] == '.': board[r][c] = 'X'

    # bishop_max_count = max(m, n) // 3
    bishop_max_count = sum(cell == '.' for row in board for cell in row) // min(m, n) // 3
    # print("bishop_max_count = ", bishop_max_count)
    # random place knights and bishops
    for _ in range(bishop_max_count):
        i, j = random.randint(0, m-1), random.randint(0, n-1)
        while board[i][j] == 'Q' or board[i][j] == 'X': 
            i, j = random.randint(0, m-1), random.randint(0, n-1)
        board[i][j] = 'B'
    for _ in range(random.randint(0, m*n//2)):
        i, j = random.randint(0, m-1), random.randint(0, n-1)
        if board[i][j] == 'Q' or board[i][j] == 'X': continue
        board[i][j] = 'K'

    attack_cnt = init_attack_cnt(board)
    curr_cost = cost(board, attack_cnt)
    best = [r[:] for r in board]
    best_attack_cnt = [row[:] for row in attack_cnt]
    best_cost = curr_cost
    temp = start_temp

    for step in range(max_steps):
        neighbors = []

        # 先找出有衝突的棋子
        conflict_bishops = [(i, j) for i in range(m) for j in range(n) if board[i][j] == 'B' and attack_cnt[i][j] > 0]
        conflict_knights = [(i, j) for i in range(m) for j in range(n) if board[i][j] == 'K' and attack_cnt[i][j] > 0]
        empties = [(i, j) for i in range(m) for j in range(n) if board[i][j] == '.']

        # 1. 新增：隨機選一個空格，隨機放 K
        if empties:
            i, j = random.choice(empties)
            piece = random.choice(['K'])
            new_board = [r[:] for r in board]
            new_attack_cnt = [row[:] for row in attack_cnt]
            new_board[i][j] = piece
            update_attack_cnt(new_attack_cnt, i, j, 1, piece)
            neighbors.append((new_board, new_attack_cnt))
        # 2. 刪除：隨機選一個有衝突的棋子刪除
        if conflict_knights:
            i, j = random.choice(conflict_knights)
            piece = board[i][j]
            new_board = [r[:] for r in board]
            new_attack_cnt = [row[:] for row in attack_cnt]
            new_board[i][j] = '.'
            update_attack_cnt(new_attack_cnt, i, j, -1, piece)
            neighbors.append((new_board, new_attack_cnt))
        # 3. 移動：隨機選一個有衝突的棋子，移動到隨機空格
        conflict_all = conflict_bishops + conflict_knights
        if conflict_all and empties:
            from_i, from_j = random.choice(conflict_all)
            to_i, to_j = random.choice(empties)
            if (from_i, from_j) != (to_i, to_j):
                piece = board[from_i][from_j]
                new_board = [r[:] for r in board]
                new_attack_cnt = [row[:] for row in attack_cnt]
                new_board[from_i][from_j] = '.'
                update_attack_cnt(new_attack_cnt, from_i, from_j, -1, piece)
                new_board[to_i][to_j] = piece
                update_attack_cnt(new_attack_cnt, to_i, to_j, 1, piece)
                neighbors.append((new_board, new_attack_cnt))
        
        if not neighbors:
            # print("No valid neighbors found, stopping.")
            # print(f"Valid Board Found: {is_valid_board(best)}")
            break
        # 隨機選一個鄰居
        new_board, new_attack_cnt = random.choice(neighbors)
        new_cost = cost(new_board, new_attack_cnt)
        delta = new_cost - curr_cost
        if delta < 0 or random.random() < math.exp(-delta / (temp + 1e-9)):
            board = [r[:] for r in new_board]
            attack_cnt = [r[:] for r in new_attack_cnt]
            curr_cost = new_cost
            if curr_cost < best_cost:
                best_cost = curr_cost
                best = [r[:] for r in board]
        # temp *= cooling_rate
        temp = max(temp * cooling_rate, 1e-8)
        bishop_cnt = sum(row.count('B') for row in board)
        knight_cnt = sum(row.count('K') for row in board)
        save_cnt = sum(row.count(0) for row in attack_cnt)
        # print(f"Step {step+1}, Best Cost: {best_cost}, Bishop: {bishop_cnt}, Knight: {knight_cnt}, Save: {save_cnt - bishop_cnt - knight_cnt}, Temp: {temp:.4f}, delta: {delta}, AcceptProb: {math.exp(-delta / (temp + 1e-9))}")
        if temp < end_temp:
            if is_valid_board(best):
                # print("Valid Board Found")
                break
    return best