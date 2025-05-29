KnightsMove = [(2, 1), (2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]

def ClearKnights(board, m, n, row, col):
    for dr, dc in KnightsMove:
        nr, nc = row + dr, col + dc 
        if 0 <= nr < m and 0 <= nc < n and board[nr][nc] == 0: board[nr][nc] = -1
def is_safe_knights(board, m, n,row, col):
    for dr, dc in KnightsMove:
        nr, nc = row + dr, col + dc 
        if 0 <= nr < m and 0 <= nc < n and board[nr][nc] > 0: return False
    return True
def is_safe_bishops(board, m, n, row, col):
    for d in range(1, max(m, n)):
        for dr, dc in [(-d, -d), (-d, d), (d, -d), (d, d)]:
            nr, nc = row + dr, col + dc
            if 0 <= nr < m and 0 <= nc < n and board[nr][nc] > 0: return False
    return True
def placeKnights(board, m, n, ismainDiagonal):
    for i in range(m):
        for j in range(i % 2 if ismainDiagonal else (i + 1) % 2, n, 2):
            if board[i][j] == 0 and is_safe_knights(board, m, n, i, j): 
                board[i][j] = 2
                ClearKnights(board, m, n, i, j)
    return board

def placeBishops(board, m, n):
    nr, nc = -1, -1
    minNKnightsonLine = float('inf')
    for i in range(m):
        for j in range(n):
            if board[i][j] != 1 and board[i][j] != -1:
                NKnightsonLine = 0
                for d in range(1, max(m, n)):
                    for dr, dc in [(-d, -d), (-d, d), (d, -d), (d, d)]:
                        r, c = i + dr, j + dc
                        if 0 <= r < m and 0 <= c < n: NKnightsonLine += 1
                if NKnightsonLine == 0: board[i][j] = 3
                if NKnightsonLine < minNKnightsonLine:
                    minNKnightsonLine = NKnightsonLine
                    nr, nc = i, j
    # no place to put bishops
    if nr == -1 and nc == -1: return board
    # bishops can put without erasing knights
    if minNKnightsonLine == 0: return board
    # place bishops with replacing knights
    board[nr][nc] = 3
    return board
def findMostBishopsAndKnightswithQueens(m, n, QueensPos):
    # queens = 1, Knights = 2, Bishops = 3, can't put -1
    board = [[0] * n for _ in range(m)]
    # place queens
    for qr, qc in QueensPos:
        if qr < 0 or qr >= m or qc < 0 or qc >= n:
            print("Invalid Queen position")
            return
        board[qr][qc] = 1
        for i in range(m): 
            if board[i][qc] == 0: board[i][qc] = -1
        for i in range(n): 
            if board[qr][i] == 0:board[qr][i] = -1
        for d in range(1, max(m, n)):
            for dr, dc in [(-d, -d), (-d, d), (d, -d), (d, d)]:
                r, c = qr + dr, qc + dc
                if 0 <= r < m and 0 <= c < n: board[r][c] = -1
    # determine which diagonal can put more knights
    NmainDiagonal = NantiDiagonal = 0
    for i in range(m):
        for j in range(n):
            if (i + j)%2 == 0 and board[i][j] == 0:
                if is_safe_knights(board, m, n, i, j) : NmainDiagonal += 1
            elif (i - j)%2 == 1 and board[i][j] == 0: 
                if is_safe_knights(board, m, n, i, j): NantiDiagonal += 1
    # place knights
    board = placeKnights(board, m, n, NmainDiagonal >= NantiDiagonal)
    # place bishops
    board = placeBishops(board, m, n)
    # for i in range(m): print(board[i])
    return board
# findMostBishopsAndKnightswithQueens(4, 6, [(0, 0), (2, 3)])
    