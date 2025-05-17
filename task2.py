def findmostBishops(m, n):
    if m < n : m, n = n, m
    board = [[0]*n for _ in range(m)]
    for col in range(n): board[0][col] = 1
    for col in range(1, n-1): board[m-1][col] = 1
    for row in range(m):
        print(board[row])
    return board
# findmostBishops(4, 3)