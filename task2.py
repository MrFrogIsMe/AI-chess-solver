def findmostBishops(m, n):
    board = [[0]*n for _ in range(m)]
    if m <= n: 
        board[0] = [1] * n
    else:
        for row in range(m): board[row][0] = 1
    if m == n:
        for col in range(1, n-1): board[m-1][col] = 1
    for row in range(m):
        print(board[row])
    return board
findmostBishops(4, 5)