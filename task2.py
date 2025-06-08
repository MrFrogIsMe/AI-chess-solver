import random

bishop_moves = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

def findmostBishops(m, n):
    return find_most_bishops_hill_climbing(m, n)

def find_most_bishops_hill_climbing(
        m, n, 
        max_steps=None, alpha=10, beta=10):
    if max_steps is None:
        max_steps = m * n * 200

    def is_valid_board(board):
        for i in range(m):
            for j in range(n):
                if board[i][j] == 'B':
                    # Check diagonals for conflicts
                    for dx, dy in bishop_moves:
                        x, y = i + dx, j + dy
                        while 0 <= x < m and 0 <= y < n:
                            if board[x][y] != '.':
                                return False
                            x += dx
                            y += dy
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

    def cost(board, attack_cnt):
        num_bishops = sum(row.count('B') for row in board)
        # 用 attack_cnt 計算攻擊衝突數：
        conflict = 0
        conflict = 0
        for i in range(m):
            for j in range(n):
                if board[i][j] != '.' and attack_cnt[i][j] > 0:
                    conflict += attack_cnt[i][j]
        safe_count = 0
        for i in range(m):
            for j in range(n):
                if board[i][j] == '.' and attack_cnt[i][j] == 0:
                    safe_count += 1
        return -num_bishops + alpha * conflict + beta * safe_count

    # 隨機產生初始解（可放一些 bishop）
    board = [['.']*n for _ in range(m)]
    for _ in range(random.randint(0, m*n)):
        i, j = random.randint(0, m-1), random.randint(0, n-1)
        board[i][j] = 'B'
    attack_cnt = init_attack_cnt(board)
    curr_cost = cost(board, attack_cnt)
    best = [r[:] for r in board]
    best_attack_cnt = [row[:] for row in attack_cnt]
    best_cost = curr_cost

    for step in range(max_steps):
        neighbors = []

        # 先找出有衝突的棋子
        conflict_bishops = [(i, j) for i in range(m) for j in range(n) if board[i][j] == 'B' and attack_cnt[i][j] > 0]
        empties = [(i, j) for i in range(m) for j in range(n) if board[i][j] == '.']

        # 1. 新增：隨機選一個空格，隨機放 K
        if empties:
            i, j = random.choice(empties)
            piece = 'B'
            new_board = [r[:] for r in board]
            new_attack_cnt = [row[:] for row in attack_cnt]
            new_board[i][j] = piece
            update_attack_cnt(new_attack_cnt, i, j, 1, piece)
            neighbors.append((new_board, new_attack_cnt))
        
        # 2. 刪除：隨機選一個有衝突的棋子刪除
        if conflict_bishops:
            i, j = random.choice(conflict_bishops)
            piece = board[i][j]
            new_board = [r[:] for r in board]
            new_attack_cnt = [row[:] for row in attack_cnt]
            new_board[i][j] = '.'
            update_attack_cnt(new_attack_cnt, i, j, -1, piece)
            neighbors.append((new_board, new_attack_cnt))
        
        # 3. 移動：隨機選一個有衝突的棋子，移動到隨機空格
        if conflict_bishops and empties:
            from_i, from_j = random.choice(conflict_bishops)
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
        neighbor_costs = [(cost(nb, ac), nb, ac) for nb, ac in neighbors]
        neighbor_costs.sort(key=lambda x: x[0])
        # print(f"Step {step+1}: current cost={curr_cost}, best cost={best_cost}, neighbors found={len(neighbor_costs)}")
        # for state in neighbors:
        #     for b in state[0]:
        #         print(' '.join(b))
        #     print()
        if neighbor_costs and neighbor_costs[0][0] < curr_cost:
            curr_cost, board, attack_cnt = neighbor_costs[0]
            if curr_cost < best_cost:
                best_cost = curr_cost
                best = [r[:] for r in board]
                best_attack_cnt = [row[:] for row in attack_cnt]
        elif is_valid_board(best):
            # print("valid board found")
            break
    # cost = -bishop數量 + alpha*conflict，所以答案是 -best_cost 當conflict=0時
    # num_bishops = sum(row.count('B') for row in best)
    return best
