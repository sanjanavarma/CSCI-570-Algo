
import sys
import time
import psutil

# Constants
delta_e = 30 #gap penalty
alpha = {
    'A': {'A': 0,   'C': 110, 'G': 48,  'T': 94},
    'C': {'A': 110, 'C': 0,   'G': 118, 'T': 48},
    'G': {'A': 48,  'C': 118, 'G': 0,   'T': 110},
    'T': {'A': 94,  'C': 48,  'G': 110, 'T': 0}
}

# ----------------------------
# Input string generation
# ----------------------------
def parse_input(input_path):
    with open(input_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    s1 = lines[0]
    j = 0
    while lines[1 + j].isdigit():
        j += 1
    idx1 = list(map(int, lines[1:1 + j]))

    s2 = lines[1 + j]
    idx2 = list(map(int, lines[2 + j:]))

    return generate_string(s1, idx1), generate_string(s2, idx2)

def generate_string(base, indices):
    s = base
    for idx in indices:
        s = s[:idx+1] + s + s[idx+1:]
    return s

# ---------------------------------------------------
# Dynammic Programming & Divide and Conquer Algorithm
# ---------------------------------------------------
def align(x, y):
    if len(x) == 0:
        return '_' * len(y), y
    elif len(y) == 0:
        return x, '_' * len(x)
    elif len(x) == 1 or len(y) == 1:
        return basic_alignment(x, y)
    else:
        xlen = len(x)
        xmid = xlen // 2

        score_left = compute_cost(x[:xmid], y)
        score_right = compute_cost(x[xmid:][::-1], y[::-1])
        ysplit = argmin_index([l + r for l, r in zip(score_left, score_right[::-1])])

        x_left, y_left = align(x[:xmid], y[:ysplit])
        x_right, y_right = align(x[xmid:], y[ysplit:])

        return x_left + x_right, y_left + y_right

def compute_cost(x, y):
    prev = [i * delta_e for i in range(len(y) + 1)]
    for i in range(1, len(x) + 1):
        curr = [i * delta_e] + [0] * len(y)
        for j in range(1, len(y) + 1):
            match = prev[j-1] + alpha[x[i-1]][y[j-1]]
            delete = prev[j] + delta_e
            insert = curr[j-1] + delta_e
            curr[j] = min(match, delete, insert)
        prev = curr
    return prev

def basic_alignment(x, y):
    m, n = len(x), len(y)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i * delta_e
    for j in range(n + 1):
        dp[0][j] = j * delta_e
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            match = dp[i-1][j-1] + alpha[x[i-1]][y[j-1]]
            delete = dp[i-1][j] + delta_e
            insert = dp[i][j-1] + delta_e
            dp[i][j] = min(match, delete, insert)
    i, j = m, n
    aligned_x, aligned_y = '', ''
    while i > 0 and j > 0:
        score = dp[i][j]
        if score == dp[i-1][j-1] + alpha[x[i-1]][y[j-1]]:
            aligned_x = x[i-1] + aligned_x
            aligned_y = y[j-1] + aligned_y
            i -= 1
            j -= 1
        elif score == dp[i-1][j] + delta_e:
            aligned_x = x[i-1] + aligned_x
            aligned_y = '_' + aligned_y
            i -= 1
        else:
            aligned_x = '_' + aligned_x
            aligned_y = y[j-1] + aligned_y
            j -= 1
    while i > 0:
        aligned_x = x[i-1] + aligned_x
        aligned_y = '_' + aligned_y
        i -= 1
    while j > 0:
        aligned_x = '_' + aligned_x
        aligned_y = y[j-1] + aligned_y
        j -= 1
    return aligned_x, aligned_y

def alignment_cost(x, y):
    return sum(delta_e if a == '_' or b == '_' else alpha[a][b] for a, b in zip(x, y))

def argmin_index(lst):
    return min(range(len(lst)), key=lambda i: lst[i])

# ----------------------------
# Recording memory
# ----------------------------
def get_memory_kb():
    process = psutil.Process()
    return process.memory_info().rss / 1024

# ----------------------------
# Main function Execution
# ----------------------------
def main():
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    x, y = parse_input(input_file)

    start_time = time.time()
    aligned_x, aligned_y = align(x, y)
    end_time = time.time()

    cost = alignment_cost(aligned_x, aligned_y)
    time_taken = (end_time - start_time) * 1000
    memory_used = get_memory_kb()

    with open(output_file, 'w') as f:
        f.write(str(cost) + '\n')
        f.write(aligned_x + '\n')
        f.write(aligned_y + '\n')
        f.write(f"{time_taken:.3f}" + '\n')
        f.write(f"{memory_used:.3f}" + '\n')

if __name__ == '__main__':
    main()