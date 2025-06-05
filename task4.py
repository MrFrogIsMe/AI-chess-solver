import math
import random

bishop_moves = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
knight_moves = [(-1, -2), (-1, 2), (1, -2), (1, 2), (-2, -1), (-2, 1), (2, -1), (2, 1)]

def find_most_bishops_and_knights(m, n):
    return find_most_bishops_and_knights_simulated_annealing(m, n, alpha=30, beta=30)

def find_most_bishops_and_knights_simulated_annealing(m, n, max_steps=100000, alpha=10, beta=10, start_temp=10.0, end_temp=0.01, cooling_rate=0.995):
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
        return -num_bishops + alpha * conflict + beta * safe_count

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
        # 隨機產生 k 個鄰居（加、移除、移動 bishop）
        empties = []
        bishops = []
        knights = []
        for i in range(m):
            for j in range(n):
                if board[i][j] == '.':
                    empties.append((i, j))
                elif board[i][j] == 'B':
                    bishops.append((i, j))
                elif board[i][j] == 'K':
                    knights.append((i, j))
        for i in range(m):
            for j in range(n):
                new_board = [r[:] for r in board]
                new_attack_cnt = [row[:] for row in attack_cnt]
                if new_board[i][j] == '.':
                    piece = random.choice(['B', 'K'])
                    new_board[i][j] = piece
                    update_attack_cnt(new_attack_cnt, i, j, 1, piece)
                    neighbors.append((new_board, new_attack_cnt))
                elif new_board[i][j] == 'B':
                    piece = 'B'
                    new_board[i][j] = '.'
                    update_attack_cnt(new_attack_cnt, i, j, -1, piece)
                    neighbors.append((new_board, new_attack_cnt))
                elif new_board[i][j] == 'K':
                    piece = 'K'
                    new_board[i][j] = '.'
                    update_attack_cnt(new_attack_cnt, i, j, -1, piece)
                    neighbors.append((new_board, new_attack_cnt))
        for i in range(m):
            for j in range(n):
                if board[i][j] == 'B':
                    for x in range(m):
                        for y in range(n):
                            if board[x][y] == '.' and (x != i or y != j):
                                new_board = [r[:] for r in board]
                                new_attack_cnt = [row[:] for row in attack_cnt]
                                new_board[i][j] = '.'
                                update_attack_cnt(new_attack_cnt, i, j, -1, 'B')
                                new_board[x][y] = 'B'
                                update_attack_cnt(new_attack_cnt, x, y, 1, 'B')
                                neighbors.append((new_board, new_attack_cnt))
        for i in range(m):
            for j in range(n):
                if board[i][j] == 'K':
                    for x, y in empties:
                        if (x != i or y != j):
                            new_board = [r[:] for r in board]
                            new_attack_cnt = [row[:] for row in attack_cnt]
                            new_board[i][j] = '.'
                            update_attack_cnt(new_attack_cnt, i, j, -1, 'K')
                            new_board[x][y] = 'K'
                            update_attack_cnt(new_attack_cnt, x, y, 1, 'K')
                            neighbors.append((new_board, new_attack_cnt))
        if not neighbors:
            print("No valid neighbors found, stopping.")
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
        print(f"Step {step+1}, Current Cost: {curr_cost}, Best Cost: {best_cost}, Temperature: {temp:.4f}")
        # print(f"Current Board:")
        # for row in board:
        #     print(*row)
        if temp < end_temp:
            if is_valid_board(best):
                break
            else:
                temp = start_temp  # Reset temperature if no valid board found
    return best