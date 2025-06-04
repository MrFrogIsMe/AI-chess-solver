from sys import argv
import task2
from team0 import printboard
import time

# calculate the average number of bishops placed on the board
# run 20 times and return the average
def validate_bishops(m, n, runs=20):
    total_bishops = []
    for i in range(runs):
        print(f"Run {i+1}/{runs} for {m}x{n} board: ", end="")
        start_time = time.time()
        board, count = task2.findmostBishops(m, n)
        elapsed = time.time() - start_time
        total_bishops.append(count)
        print(f"{count} bishops placed, ", end="")
        print(f"mean: {sum(total_bishops) / len(total_bishops):.2f}, ", end="")
        print(f"time: {elapsed:.4f}s")
        # print("Board:")
        # printboard(board, count)
    average_bishops = sum(total_bishops) / runs
    print(f"Average number of bishops placed on a {m}x{n} board: {average_bishops}")
    # print max and min bishops placed
    print(f"Max bishops placed: {max(total_bishops)}")
    print(f"Min bishops placed: {min(total_bishops)}")
    return average_bishops

if __name__ == "__main__":
    # Example usage
    m, n = 10, 10
    m, n = int(argv[1].strip()), int(argv[2].strip())
    validate_bishops(m, n)