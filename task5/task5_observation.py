bishop_moves = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
knight_moves = [(-1, -2), (-1, 2), (1, -2), (1, 2), (-2, -1), (-2, 1), (2, -1), (2, 1)]

def ClearKnights(board, m, n, row, col):
    for dr, dc in knight_moves:
        nr, nc = row + dr, col + dc 
        if 0 <= nr < m and 0 <= nc < n and board[nr][nc] == '.': board[nr][nc] = 'X'
def is_safe_knights(board, m, n,row, col):
    for dr, dc in knight_moves:
        nr, nc = row + dr, col + dc 
        if 0 <= nr < m and 0 <= nc < n and board[nr][nc] != '.' and board[nr][nc] != 'X': return False
    return True
def is_safe_bishops(board, m, n, row, col):
    for d in range(1, max(m, n)):
        for dr, dc in [(-d, -d), (-d, d), (d, -d), (d, d)]:
            nr, nc = row + dr, col + dc
            if 0 <= nr < m and 0 <= nc < n and board[nr][nc] != '.' and board[nr][nc] != 'X': return False
    return True
def placeKnights(board, m, n, ismainDiagonal):
    for i in range(m):
        for j in range(i % 2 if ismainDiagonal else (i + 1) % 2, n, 2):
            if board[i][j] == '.' and is_safe_knights(board, m, n, i, j): 
                board[i][j] = 'K'
                ClearKnights(board, m, n, i, j)
    return board

def placeBishops(board, m, n):
    nr, nc = -1, -1
    minNKnightsonLine = float('inf')
    for i in range(m):
        for j in range(n):
            if board[i][j] != 'Q' and board[i][j] != 'X':
                # check whether there is knights on bishop's line
                NKnightsonLine = 0
                for d in range(1, max(m, n)):
                    for dr, dc in [(-d, -d), (-d, d), (d, -d), (d, d)]:
                        r, c = i + dr, j + dc
                        if 0 <= r < m and 0 <= c < n and (board[r][c] == 'K' or board[r][c] == 'B'): NKnightsonLine += 1
                if NKnightsonLine == '.': board[i][j] = 3
                if NKnightsonLine < minNKnightsonLine:
                    minNKnightsonLine = NKnightsonLine
                    nr, nc = i, j
    # no place to put bishops
    if nr == -1 and nc == -1: return board
    # bishops can put without erasing knights
    if minNKnightsonLine == 0: return board
    # place bishops with replacing knights
    board[nr][nc] = 'B'
    return board
def find_most_bishops_and_knights_with_queens_observation(m, n, QueensPos):
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
    # determine which diagonal can put more knights
    NmainDiagonal = NantiDiagonal = 0
    for i in range(m):
        for j in range(n):
            if (i + j)%2 == '.' and board[i][j] == '.':
                if is_safe_knights(board, m, n, i, j) : NmainDiagonal += 1
            elif (i - j)%2 == '.' and board[i][j] == '.':  
                if is_safe_knights(board, m, n, i, j): NantiDiagonal += 1
    # place knights
    board = placeKnights(board, m, n, NmainDiagonal >= NantiDiagonal)
    # place bishops
    board = placeBishops(board, m, n)

    count_bishops = sum(row.count('B') for row in board)
    count_knights = sum(row.count('K') for row in board)
    # for i in range(m): print(board[i])
    return board, count_bishops, count_knights
