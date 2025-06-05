from task1_dfs import find_most_queens_dfs
from task1_hill_climbing import find_most_queens_hill_climbing
# def random_restart_hill_climbing(m, n):
#     best = None
#     max_queens = 0
#     restart = 20
#     for _ in range(restart):
#         currboard, count = hill_climbing(m, n)
#         if count > max_queens:
#             max_queens = count
#             best = currboard
#     return best

# def remove_conflicts(board):
#     m, n = len(board), len(board[0])
#     # 取得所有皇后座標
#     queens = [(i, row.index(1)) for i, row in enumerate(board) if 1 in row]
#     while True:
#         conflict_count = {}
#         for i in range(len(queens)):
#             cnt = 0
#             r1, c1 = queens[i]
#             for j in range(len(queens)):
#                 if i == j: continue
#                 r2, c2 = queens[j]
#                 if r1 == r2 or c1 == c2 or abs(r1 - r2) == abs(c1 - c2):
#                     cnt += 1
#             conflict_count[queens[i]] = cnt
#         max_conflict = max(conflict_count.values(), default=0)
#         if max_conflict == 0:
#             break
#         # 找出造成最多 conflict 的所有皇后
#         worst_queens = [pos for pos, cnt in conflict_count.items() if cnt == max_conflict]
#         # 隨便移除一個
#         r, c = worst_queens[0]
#         board[r][c] = 0
#         queens = [(i, row.index(1)) for i, row in enumerate(board) if 1 in row]
#     count = sum(sum(row) for row in board)
#     return board, count
# def simulated_annealing(m, n, max_steps=1000, start_temp=10.0, end_temp=0.01, cooling_rate=0.995):
#     # 狀態表示：每一列有一個皇后，state[i]=col
#     limit = min(m, n)
#     state = [random.randint(0, n-1) for _ in range(limit)]
#     def count_conflicts(state):
#         cnt = 0
#         for i in range(len(state)):
#             for j in range(i+1, len(state)):
#                 if state[i] == state[j] or abs(state[i]-state[j]) == abs(i-j):
#                     cnt += 1
#         return cnt

#     best_state = list(state)
#     best_score = count_conflicts(state)
#     temp = start_temp

#     for step in range(max_steps):
#         if best_score == 0 or temp < end_temp:
#             break
#         # 隨機選一列，換到不同列的位置
#         next_state = list(state)
#         row = random.randint(0, limit-1)
#         old_col = state[row]
#         candidates = [col for col in range(n) if col != old_col]
#         if not candidates:
#             continue
#         next_state[row] = random.choice(candidates)
#         next_score = count_conflicts(next_state)
#         delta = best_score - next_score
#         if delta > 0 or random.random() < math.exp(delta / (temp + 1e-9)):
#             state = next_state
#             best_score = next_score
#             best_state = list(state)
#         temp *= cooling_rate

#     # 轉回棋盤格式
#     board = [[0]*n for _ in range(m)]
#     for row in range(len(best_state)):
#         board[row][best_state[row]] = 1
#     return remove_conflicts(board)


def find_most_queens(m, n):
    print("m = ", m, "n = ", n)
    # board, count = dfs(m, n)
    board, count = find_most_queens_hill_climbing(m, n)
    # board = [[0]*n for _ in range(m)]
    # return dfs(board, 0, m, n, m <= n)
    # result, count = hill_climbing(board, m, n)
    # return random_restart_hill_climbing(m, n)
    # result, count = simulated_annealing(m, n)
    for row in board: print(row)
    print(count)
