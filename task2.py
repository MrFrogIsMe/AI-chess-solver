import random

def findmostBishops(m, n):
    return find_most_bishops_hill_climbing(m, n)

def find_most_bishops_hill_climbing(m, n, max_steps=1000, alpha=10):
    # 新增：維護 attack_cnt
    def init_attack_cnt(board):
        attack_cnt = [[0]*n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                if board[i][j] == 'B':
                    update_attack_cnt(attack_cnt, i, j, 1)
        return attack_cnt

    def update_attack_cnt(attack_cnt, i, j, delta):
        # 四個斜線方向
        for dx, dy in [(-1,-1), (-1,1), (1,-1), (1,1)]:
            x, y = i+dx, j+dy
            while 0 <= x < m and 0 <= y < n:
                attack_cnt[x][y] += delta
                x += dx
                y += dy

    def cost(board, attack_cnt):
        num_bishops = sum(row.count('B') for row in board)
        # 用 attack_cnt 計算攻擊衝突數：
        conflict = 0
        for i in range(m):
            for j in range(n):
                if board[i][j] == 'B':
                    # attack_cnt[i][j] 表示這顆 bishop 被其他 bishop 攻擊的次數
                    conflict += attack_cnt[i][j]
        conflict //= 2  # 每對衝突會被算兩次
        # 用 attack_cnt 計算安全格數：
        safe_count = 0
        for i in range(m):
            for j in range(n):
                if board[i][j] == '.' and attack_cnt[i][j] == 0:
                    safe_count += 1
        # print(f"cost: num_bishops={num_bishops}, conflict={conflict}, safe_count={safe_count}")
        return -num_bishops + alpha * conflict + safe_count  # safe_count 權重可再調整

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
        # 可能的行動：加、移除、移動 bishop
        for i in range(m):
            for j in range(n):
                if board[i][j] == '.' and attack_cnt[i][j] == 0:
                    new_board = [r[:] for r in board]
                    new_attack_cnt = [row[:] for row in attack_cnt]
                    new_board[i][j] = 'B'
                    update_attack_cnt(new_attack_cnt, i, j, 1)
                    neighbors.append((new_board, new_attack_cnt))
        for i in range(m):
            for j in range(n):
                if board[i][j] == 'B':
                    new_board = [r[:] for r in board]
                    new_attack_cnt = [row[:] for row in attack_cnt]
                    new_board[i][j] = '.'
                    update_attack_cnt(new_attack_cnt, i, j, -1)
                    neighbors.append((new_board, new_attack_cnt))
        for i in range(m):
            for j in range(n):
                if board[i][j] == 'B':
                    for x in range(m):
                        for y in range(n):
                            if board[x][y] == '.' and attack_cnt[x][y] == 0 and (x != i or y != j):
                                new_board = [r[:] for r in board]
                                new_attack_cnt = [row[:] for row in attack_cnt]
                                new_board[i][j] = '.'
                                update_attack_cnt(new_attack_cnt, i, j, -1)
                                new_board[x][y] = 'B'
                                update_attack_cnt(new_attack_cnt, x, y, 1)
                                neighbors.append((new_board, new_attack_cnt))
        neighbor_costs = [(cost(nb, ac), nb, ac) for nb, ac in neighbors]
        neighbor_costs.sort(key=lambda x: x[0])
        print(f"Step {step+1}: current cost={curr_cost}, best cost={best_cost}, neighbors found={len(neighbor_costs)}")
        if neighbor_costs and neighbor_costs[0][0] < curr_cost:
            curr_cost, board, attack_cnt = neighbor_costs[0]
            if curr_cost < best_cost:
                best_cost = curr_cost
                best = [r[:] for r in board]
                best_attack_cnt = [row[:] for row in attack_cnt]
        else:
            break
    # cost = -bishop數量 + alpha*conflict，所以答案是 -best_cost 當conflict=0時
    num_bishops = sum(row.count('B') for row in best)
    return best, num_bishops
