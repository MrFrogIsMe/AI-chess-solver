def is_safe(board, row, col, n, m):
    for i in range(n):
        if board[i][col] == 1: return False
    for i in range(m):
        if board[row][i] == 1: return False
    i, j = row - 1, col - 1
    while i >= 0 and j >= 0:
        if board[i][j] == 1: return False
        i -= 1
        j -= 1
    i, j = row - 1, col + 1
    while i >= 0 and j < n:
        if board[i][j] == 1: return False
        i -= 1
        j += 1
    return True

def dfs(board, row, n, m):
    if row == n: 
        return board
    for col in range(n):
        if is_safe(board, row, col, n, m):
            board[row][col] = 1
            result = dfs(board, row+1, n, m)
            if result: return result
            board[row][col] = 0
    return None

def findmostQueens(m, n):
    board = [[0]*n for _ in range(m)]
    result = dfs(board, 0, n, m)
    return result
