def findmostBishops(m, n):
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
    return board
# findmostBishops(6, 6)