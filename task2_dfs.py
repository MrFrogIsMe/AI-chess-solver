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