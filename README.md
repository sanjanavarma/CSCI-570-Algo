# CSCI-570-Algo

Algorithm Performance Summary Contributors

Parvathi Sanjana Pericherla – USC ID: 6075279768

Keerthi Sankaralingam – USC ID: 6628249966

Shireen Chand – USC ID: 8152137082

Overview
This document presents a performance comparison between two algorithms — a Basic and an Efficient version for sequence alignment problem— using runtime and memory metrics across varying input sizes.

Data Points Collected
Metrics were collected for combined input sizes (M + N) from 16 to 3968, including:

Execution Time (ms) for both Basic and Efficient algorithms

Memory Usage (KB) for both Basic and Efficient algorithms

Performance Analysis
Memory vs Problem Size
Basic Algorithm:
Displays a polynomial memory growth pattern, indicating O(M × N) space complexity.

Memory usage increases significantly with problem size.

Efficient Algorithm:
Exhibits a linear growth pattern, indicating O(N) space complexity.

Maintains almost constant memory usage even as input size increases.

Time vs Problem Size
Basic Algorithm:
Shows a polynomial growth in time, approximately O(N²).

Efficient Algorithm:
Also shows a polynomial time complexity, around O(N²).

While memory-efficient, the time complexity increases due to repeated recomputation of the opt array.

Graph Insights
Graph 1 (Memory vs Problem Size):
Confirms the Efficient algorithm's superior memory optimization.

Graph 2 (Time vs Problem Size):
While both algorithms show polynomial growth, the Basic algorithm performs better in time for larger inputs.

Conclusion
The Efficient algorithm excels in memory performance with linear space complexity, but has a higher time cost for large inputs due to recomputation overhead.
The Basic algorithm is less memory-efficient but offers faster execution at scale.
