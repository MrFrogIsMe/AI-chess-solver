# from task3 import findmostKnights
def findmostKnights(m, n):
    board = [[0]*n for _ in range(m)]
    if m == 1:
        for i in range (n): board[0][i] = 1
    elif n == 1:
        for i in range (m): board[i][0] = 1
    elif m == 2:
         for i in range (n): 
            if i % 4 == 2 or i % 4 == 3: continue
            board[0][i] = 1
            board[1][i] = 1
    elif n == 2:
        for i in range (m): 
            if i % 4 == 2 or i % 4 == 3: continue
            board[i][0] = 1
            board[i][1] = 1
    else:
        for i in range (m):
            start_col = 0 if i % 2 == 0 else 1
            for j in range (start_col, n, 2):
                board[i][j] = 1
    # for i in range (m): print(board[i])
    return board
def ClearKnights(board, m, n, row, col):
    KnightsMove = [(2, 1), (2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
    for dr, dc in KnightsMove:
        nr, nc = row + dr, col + dc 
        if 0 <= nr < m and 0 <= nc < n: board[nr][nc] = 0
def replaceKnightswithBishops(board, m, n, Nreplace):
    if m < n:
        for col in range(n):
            for row in range(1, m, 2):
                if Nreplace == 0: return board
                board[row][col] = 2
                Nreplace -= 1
                ClearKnights(board, m, n, row, col)
    else:
        for row in range (m):
            for col in range(1, n, 2):
                if Nreplace == 0: return board
                board[row][col] = 2
                Nreplace -= 1
                ClearKnights(board, m, n, row, col)
def findMostBishopsAndKnights(m, n):
    board = [[0] * n for _ in range(m)]
    board = findmostKnights(m, n)
    board = replaceKnightswithBishops(board, m, n, 1)
    # for i in range (m): print(board[i])
    return board

# findMostBishopsAndKnights(7, 5)