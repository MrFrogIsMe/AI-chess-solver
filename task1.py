# attacked[0]: row
# attacked[1]: col
# attacked[2]: main diagonal
# attacked[3]: anti diagonal
attacked = [set() for _ in range(4)]

def is_safe(row, col):
    if row in attacked[0]: return False         # check row
    if col in attacked[1]: return False         # check col
    if row + col in attacked[2]: return False   # check main diagonal
    if row - col in attacked[3]: return False   # check anti diagonal
    return True

def dfs(board, idx, m, n, by_row):
    limit = m if by_row else n
    if idx == limit: return board
    for i in range(n if by_row else m):
        row = idx if by_row else i
        col = i if by_row else idx
        if is_safe(row, col):
            board[row][col] = 1
            attacked[0].add(row)
            attacked[1].add(col)
            attacked[2].add(row + col)
            attacked[3].add(row - col)
            result = dfs(board, idx+1, m, n, by_row)
            if result: return result
            board[row][col] = 0
            attacked[0].remove(row)
            attacked[1].remove(col)
            attacked[2].remove(row + col)
            attacked[3].remove(row - col)
    return None

def findmostQueens(m, n):
    board = [[0]*n for _ in range(m)]
    by_row = m <= n
    result = dfs(board, 0, m, n, by_row)
    for row in board:
        print(row)
    return result
findmostQueens(8, 3)
