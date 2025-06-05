import math
import random

def findmostBishops(m, n):
    return find_most_bishops_simulated_annealing(m, n, k=100, alpha=2, beta=1)

def find_most_bishops_simulated_annealing(m, n, max_steps=100000, alpha=10, beta=10, k=10, start_temp=10.0, end_temp=0.01, cooling_rate=0.995):
    def is_valid_board(board):
        for i in range(m):
            for j in range(n):
                if board[i][j] == 'B':
                    # Check diagonals for conflicts
                    for dx, dy in [(-1,-1), (-1,1), (1,-1), (1,1)]:
                        x, y = i+dx, j+dy
                        while 0 <= x < m and 0 <= y < n:
                            if board[x][y] == 'B':
                                return False
                            x += dx
                            y += dy
        return True

    def init_attack_cnt(board):
        attack_cnt = [[0]*n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                if board[i][j] == 'B':
                    update_attack_cnt(attack_cnt, i, j, 1)
        return attack_cnt

    def update_attack_cnt(attack_cnt, i, j, delta):
        for dx, dy in [(-1,-1), (-1,1), (1,-1), (1,1)]:
            x, y = i+dx, j+dy
            while 0 <= x < m and 0 <= y < n:
                attack_cnt[x][y] += delta
                x += dx
                y += dy

    def cost(board, attack_cnt):
        num_bishops = sum(row.count('B') for row in board)
        conflict = 0
        for i in range(m):
            for j in range(n):
                if board[i][j] == 'B':
                    conflict += attack_cnt[i][j]
        conflict //= 2
        safe_count = 0
        for i in range(m):
            for j in range(n):
                if board[i][j] == '.' and attack_cnt[i][j] == 0:
                    safe_count += 1
        return -num_bishops + alpha * conflict + beta * safe_count

    # 隨機產生初始解
    board = [['.']*n for _ in range(m)]
    for _ in range(random.randint(0, m*n)):
        i, j = random.randint(0, m-1), random.randint(0, n-1)
        board[i][j] = 'B'
    attack_cnt = init_attack_cnt(board)
    curr_cost = cost(board, attack_cnt)
    best = [r[:] for r in board]
    best_attack_cnt = [row[:] for row in attack_cnt]
    best_cost = curr_cost
    temp = start_temp

    for step in range(max_steps):
        neighbors = []
        # 隨機產生 k 個鄰居（加、移除、移動 bishop）
        empties = [(i, j) for i in range(m) for j in range(n) if board[i][j] == '.']
        bishops = [(i, j) for i in range(m) for j in range(n) if board[i][j] == 'B']
        # 根據棋盤大小動態調整三種行動的權重
        total = len(empties) + len(bishops)
        weights = [m * n / total, 1 / total, 1 / total]  # [move, add, remove]
        action_type = random.choices(['move', 'add', 'remove'], weights=weights, k=1)[0]
        if action_type == 'add':
            if empties:
                i, j = random.choice(empties)
                new_board = [r[:] for r in board]
                new_attack_cnt = [row[:] for row in attack_cnt]
                new_board[i][j] = 'B'
                update_attack_cnt(new_attack_cnt, i, j, 1)
                neighbors.append((new_board, new_attack_cnt))
        elif action_type == 'remove':
            if bishops:
                i, j = random.choice(bishops)
                new_board = [r[:] for r in board]
                new_attack_cnt = [row[:] for row in attack_cnt]
                new_board[i][j] = '.'
                update_attack_cnt(new_attack_cnt, i, j, -1)
                neighbors.append((new_board, new_attack_cnt))
        elif action_type == 'move':
            if bishops and empties:
                from_i, from_j = random.choice(bishops)
                to_i, to_j = random.choice(empties)
                new_board = [r[:] for r in board]
                new_attack_cnt = [row[:] for row in attack_cnt]
                new_board[from_i][from_j] = '.'
                update_attack_cnt(new_attack_cnt, from_i, from_j, -1)
                new_board[to_i][to_j] = 'B'
                update_attack_cnt(new_attack_cnt, to_i, to_j, 1)
                neighbors.append((new_board, new_attack_cnt))
        if not neighbors:
            break
        # 隨機選一個鄰居
        new_board, new_attack_cnt = random.choice(neighbors)
        new_cost = cost(new_board, new_attack_cnt)
        delta = new_cost - curr_cost
        if delta < 0 or random.random() < math.exp(-delta / (temp + 1e-9)):
            board = [r[:] for r in new_board]
            attack_cnt = [row[:] for row in new_attack_cnt]
            curr_cost = new_cost
            if curr_cost < best_cost:
                best_cost = curr_cost
                best = [r[:] for r in board]
                # best_attack_cnt = [row[:] for row in attack_cnt]
        temp *= cooling_rate
        # print(f"Step {step+1}, Current Cost: {curr_cost}, Best Cost: {best_cost}, Temperature: {temp:.4f}")
        if temp < end_temp and is_valid_board(best):
            break
    num_bishops = sum(row.count('B') for row in best)
    return best, num_bishops