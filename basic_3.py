
import sys
import time
import psutil

# Constants
delta_e = 30
alpha = {
    'A': {'A': 0,   'C': 110, 'G': 48,  'T': 94},
    'C': {'A': 110, 'C': 0,   'G': 118, 'T': 48},
    'G': {'A': 48,  'C': 118, 'G': 0,   'T': 110},
    'T': {'A': 94,  'C': 48,  'G': 110, 'T': 0}
}

# ----------------------------------
# Input String Generation
# ----------------------------------
def parse_input(input_path):
    with open(input_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    s1 = lines[0]
    j = 0
    while lines[1 + j].isdigit():
        j += 1
    idx1 = list(map(int, lines[1:1 + j]))

    s2 = lines[1 + j]
    k = len(lines) - (2 + j)
    idx2 = list(map(int, lines[2 + j:]))

    # Generate strings
    full_s1 = generate_string(s1, idx1)
    full_s2 = generate_string(s2, idx2)
    return full_s1, full_s2

def generate_string(base, indices):
    s = base
    for idx in indices:
        s = s[:idx+1] + s + s[idx+1:]
    return s

# -----------------------------------------------------
# Dynamic Programming Algorithm for sequence alignment
# -----------------------------------------------------
def sequence_alignment(x, y):
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

  
    aligned_x, aligned_y = '', ''
    i, j = m, n
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

    return dp[m][n], aligned_x, aligned_y

# ---------------------------
# Recording Memory
# ---------------------------
def get_memory_kb():
    process = psutil.Process()
    mem_info = process.memory_info()
    return mem_info.rss / 1024  # memory used in KB

# ---------------------------
# Main Function Execution
# ---------------------------
def main():
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    x, y = parse_input(input_file)

    start_time = time.time()
    cost, aligned_x, aligned_y = sequence_alignment(x, y)
    end_time = time.time()
    elapsed_time = (end_time - start_time) * 1000  # elapse time in ms
    memory_used = get_memory_kb()

    with open(output_file, 'w') as f:
        f.write(str(cost) + '\n')
        f.write(aligned_x + '\n')
        f.write(aligned_y + '\n')
        f.write(f"{elapsed_time:.3f}" + '\n')
        f.write(f"{memory_used:.3f}" + '\n')

if __name__ == '__main__':
    main()
