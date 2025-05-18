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
# findmostKnights(9, 2)