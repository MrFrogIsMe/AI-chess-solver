import random

bishop_moves = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
knight_moves = [(-1, -2), (-1, 2), (1, -2), (1, 2), (-2, -1), (-2, 1), (2, -1), (2, 1)]

def find_most_bishops_and_knights_with_queens_hill_climbing(m, n, QueensPos, max_steps=1000, alpha=5):
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
                if board[i][j] != '.' and attack_cnt[i][j] > 0:
                    conflict += attack_cnt[i][j]
        safe_count = 0
        for i in range(m):
            for j in range(n):
                if board[i][j] == '.' and attack_cnt[i][j] == 0:
                    safe_count += 1
        # return -num_bishops - num_knights + alpha * conflict - safe_count
        return -num_bishops - num_knights + alpha * conflict
        # return - 10 * num_bishops - 8 *num_knights + alpha * conflict + safe_count
    
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
    # random place knights and bishops
    for _ in range(random.randint(0, m*n)):
        i, j = random.randint(0, m-1), random.randint(0, n-1)
        if board[i][j] == 'Q' or board[i][j] == 'X': continue
        board[i][j] = random.choice(['B', 'K'])
        # board[i][j] = random.choices(['B', 'K'], weights=[0.7, 0.3])[0]
    attack_cnt = init_attack_cnt(board)
    curr_cost = cost(board, attack_cnt)
    best = [r[:] for r in board]
    best_attack_cnt = [row[:] for row in attack_cnt]
    best_cost = curr_cost

    for step in range(max_steps):
        neighbors = []
        empties = []
        bishops = []
        knights = []
        for i in range (m):
            for j in range(n):
                if board[i][j] == '.':
                    empties.append((i, j))
                elif board[i][j] == 'B':
                    bishops.append((i, j))
                elif board[i][j] == 'K':
                    knights.append((i, j))
        
        # 可能的行動：加、移除、移動 bishop
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
        neighbor_costs = [(cost(nb, ac), nb, ac) for nb, ac in neighbors]
        neighbor_costs.sort(key=lambda x: x[0])
        print(f"Step {step+1}: current cost={curr_cost}, best cost={best_cost}, neighbors found={len(neighbor_costs)}")
        # for row in best:
        #     print(row)
        # num_bishops = sum(row.count('B') for row in best)
        # num_knights = sum(row.count('K') for row in best)
        # print(f"Bishops: {num_bishops}, Knights: {num_knights}")
        # print("\n")
        if neighbor_costs and neighbor_costs[0][0] < curr_cost:
            curr_cost, board, attack_cnt = neighbor_costs[0]
            if curr_cost < best_cost:
                best_cost = curr_cost
                best = [r[:] for r in board]
                best_attack_cnt = [row[:] for row in attack_cnt]
        elif is_valid_board(best):
            break
    # cost = -bishop數量 + alpha*conflict，所以答案是 -best_cost 當conflict=0時
    num_bishops = sum(row.count('B') for row in best)
    num_knights = sum(row.count('K') for row in best)
    return best, num_bishops, num_knights