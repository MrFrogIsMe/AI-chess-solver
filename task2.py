import random

def findmostBishops(m, n):
    # return find_most_bishops_ori(m, n)
    # return find_most_bishops_dfs(m, n)
    return find_most_bishops_hill_climbing(m, n)
    # return find_most_bishops_random_restart_hill_climbing(m, n)
    # return find_most_bishops_simulated_annealing(m, n)
    # return find_most_bishops_genetic(m, n)

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
    count = sum(sum(row) for row in board)
    return board, count


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
    if best_board:
        board = best_board
    else:
        board = board
    count = sum(row.count('B') for row in board)
    return board, count

def find_most_bishops_hill_climbing(m, n, max_steps=1000, alpha=10):
    import random
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
    count = sum(row.count('B') for row in best_overall) if best_overall else 0
    return best_overall, count

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
    count = sum(row.count('B') for row in best)
    return best, count

def find_most_bishops_genetic(m, n, population_size=50, generations=200, mutation_rate=0.1, elite_ratio=0.2):
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

    def board_fitness(board):
        # 合法bishop數量，不合法則懲罰
        count = 0
        for i in range(m):
            for j in range(n):
                if board[i][j] == 'B' and is_valid(board, i, j):
                    count += 1
                elif board[i][j] == 'B':
                    return -1000  # 不合法懲罰
        return count

    def random_board():
        board = [['.']*n for _ in range(m)]
        for _ in range(random.randint(0, m*n)):
            i, j = random.randint(0, m-1), random.randint(0, n-1)
            if board[i][j] == '.' and is_valid(board, i, j):
                board[i][j] = 'B'
        return board

    def crossover(parent1, parent2):
        # 單點交配
        cut = random.randint(0, m*n-1)
        child = [['.']*n for _ in range(m)]
        for idx in range(m*n):
            i, j = divmod(idx, n)
            if idx < cut:
                child[i][j] = parent1[i][j]
            else:
                child[i][j] = parent2[i][j]
        return child

    def mutate(board):
        # 隨機加/移除/移動 bishop
        b = [r[:] for r in board]
        action = random.choice(['add', 'remove', 'move'])
        if action == 'add':
            empties = [(i, j) for i in range(m) for j in range(n) if b[i][j] == '.']
            if empties:
                i, j = random.choice(empties)
                if is_valid(b, i, j):
                    b[i][j] = 'B'
        elif action == 'remove':
            bishops = [(i, j) for i in range(m) for j in range(n) if b[i][j] == 'B']
            if bishops:
                i, j = random.choice(bishops)
                b[i][j] = '.'
        else:  # move
            bishops = [(i, j) for i in range(m) for j in range(n) if b[i][j] == 'B']
            empties = [(i, j) for i in range(m) for j in range(n) if b[i][j] == '.']
            if bishops and empties:
                bi, bj = random.choice(bishops)
                ei, ej = random.choice(empties)
                b[bi][bj] = '.'
                if is_valid(b, ei, ej):
                    b[ei][ej] = 'B'
                else:
                    b[bi][bj] = 'B'
        return b

    # 初始化族群
    population = [random_board() for _ in range(population_size)]
    best = None
    best_score = -1000

    for gen in range(generations):
        scored = [(board_fitness(b), b) for b in population]
        scored.sort(reverse=True, key=lambda x: x[0])
        if scored[0][0] > best_score:
            best_score = scored[0][0]
            best = [r[:] for r in scored[0][1]]
        # 精英保留
        elite_n = max(1, int(elite_ratio * population_size))
        new_population = [scored[i][1] for i in range(elite_n)]
        # 交配產生新個體
        while len(new_population) < population_size:
            p1, p2 = random.choices(new_population, k=2)
            child = crossover(p1, p2)
            if random.random() < mutation_rate:
                child = mutate(child)
            new_population.append(child)
        population = new_population
    print(f"genetic algorithm 最大num_bishops: {best_score}")
    count = sum(row.count('B') for row in best) if best else 0
    return best, count
