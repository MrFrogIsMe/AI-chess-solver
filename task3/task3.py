def rule_based(m, n):
    board = [['.']*n for _ in range(m)]
    if m == 1:
        for i in range (n): board[0][i] = 'K'
    elif n == 1:
        for i in range (m): board[i][0] = 'K'
    elif m == 2:
         for i in range (n): 
            if i % 4 == 2 or i % 4 == 3: continue
            board[0][i] = 'K'
            board[1][i] = 'K'
    elif n == 2:
        for i in range (m): 
            if i % 4 == 2 or i % 4 == 3: continue
            board[i][0] = 'K'
            board[i][1] = 'K'
    else:
        for i in range (m):
            start_col = 0 if i % 2 == 0 else 1
            for j in range (start_col, n, 2):
                board[i][j] = 'K'
    return board

def find_most_knights(m, n):
    board = rule_based(m, n)
    return board