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

def dfs(board, row, m, n):
    if row == min(m, n):
        return board
    for col in range(n):
        if is_safe(row, col):
            board[row][col] = 1
            attacked[0].add(row)
            attacked[1].add(col)
            attacked[2].add(row + col)
            attacked[3].add(row - col)
            result = dfs(board, row+1, m, n)
            if result: return result
            board[row][col] = 0
            attacked[0].remove(row)
            attacked[1].remove(col)
            attacked[2].remove(row + col)
            attacked[3].remove(row - col)
    return None

def findmostQueens(m, n):
    board = [[0]*n for _ in range(m)]
    result = dfs(board, 0, m, n)
    return result
