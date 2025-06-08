import math
import random

bishop_moves = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
knight_moves = [(-1, -2), (-1, 2), (1, -2), (1, 2), (-2, -1), (-2, 1), (2, -1), (2, 1)]

def find_most_bishops_and_knights_simulated_annealing(m, n, max_steps=100000, alpha=10, beta=10, start_temp=10.0, end_temp=0.01, cooling_rate=0.995):
    start_temp = m * n
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
                elif board[i][j] == 'K':
                    # Check knight moves for conflicts
                    for dx, dy in knight_moves:
                        x, y = i + dx, j + dy
                        if 0 <= x < m and 0 <= y < n and board[x][y] != '.':
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
                if board[i][j] != '.' and attack_cnt[i][j] > 0:
                    conflict += attack_cnt[i][j]
        safe_count = 0
        for i in range(m):
            for j in range(n):
                if board[i][j] == '.' and attack_cnt[i][j] == 0:
                    safe_count += 1
        return - 0.1 * num_bishops - 2 * num_knights + alpha * conflict + beta * safe_count

    # 隨機產生初始解
    board = [['.']*n for _ in range(m)]
    for _ in range(random.randint(0, m*n)):
        i, j = random.randint(0, m-1), random.randint(0, n-1)
        board[i][j] = random.choice(['B', 'K'])
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
        safes = [(i, j) for i in range(m) for j in range(n) if board[i][j] == '.' and attack_cnt[i][j] == 0]


        # 1. 新增：隨機選一個空格，隨機放 B 或 K
        if safes:
            i, j = random.choice(safes)
            piece = random.choice(['B', 'K'])
            new_board = [r[:] for r in board]
            new_attack_cnt = [row[:] for row in attack_cnt]
            new_board[i][j] = piece
            update_attack_cnt(new_attack_cnt, i, j, 1, piece)
            neighbors.append((new_board, new_attack_cnt))

        # 2. 刪除：隨機選一個有衝突的棋子刪除
        conflict_all = conflict_bishops + conflict_knights
        if conflict_all:
            i, j = random.choice(conflict_all)
            piece = board[i][j]
            new_board = [r[:] for r in board]
            new_attack_cnt = [row[:] for row in attack_cnt]
            new_board[i][j] = '.'
            update_attack_cnt(new_attack_cnt, i, j, -1, piece)
            neighbors.append((new_board, new_attack_cnt))

        # 3. 移動：隨機選一個有衝突的棋子，移動到隨機空格
        if conflict_all and safes:
            from_i, from_j = random.choice(conflict_all)
            to_i, to_j = random.choice(safes)
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
            print("No valid neighbors found, stopping.")
            print(f"Valid Board Found: {is_valid_board(best)}")
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
        temp *= cooling_rate
        print(f"Step {step+1}, Best Cost: {best_cost}, Save Count: {sum(row.count(0) for row in attack_cnt)}, Temperature: {temp:.4f}")
        # print(f"Current Board:")
        # for row in board:
        #     print(*row)
        if temp < end_temp:
            if is_valid_board(best):
                break
            else:
                temp = start_temp  # Reset temperature if no valid board found
    return best