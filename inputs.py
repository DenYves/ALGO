import sys
import time
from collections import deque
from openpyxl import Workbook
from search_graph import bfs_state_graph
from bidirection_search_graph import bfs_state_graph_bidirectional
from bi3_search_graph import bfs3_state_graph_bidirectional
from bi4_search_graph import bfs4_state_graph_bidirectional
from bi5_search_graph import bfs5_state_graph_bidirectional
from bi6_search_graph import bfs6_state_graph_bidirectional
from bi7_search_graph import bfs7_state_graph_bidirectional

def read_instance(filename):
    """Read an instance from filename and return all parameters + adjacency list."""
    try:
        with open(filename, "r") as f:
            tokens = f.read().split()
    except FileNotFoundError:
        print(f"Error: file '{filename}' not found.", file=sys.stderr)
        return None  # or raise an exception

    it = iter(tokens)

    try:
        # First line: n m T D
        n = int(next(it))
        m = int(next(it))
        T = int(next(it))
        D = int(next(it))

        # Second line: s_a t_a s_b t_b  (convert to 0-based)
        s_a = int(next(it)) - 1
        t_a = int(next(it)) - 1
        s_b = int(next(it)) - 1
        t_b = int(next(it)) - 1
    except StopIteration:
        print("Error: input ended unexpectedly in the header.", file=sys.stderr)
        return None

    # Adjacency list for an undirected graph
    adj = [[] for _ in range(n)]

    # Next m lines: edges u v  (convert to 0-based)
    for _ in range(m):
        try:
            u = int(next(it)) - 1
            v = int(next(it)) - 1
        except StopIteration:
            print("Error: input ended unexpectedly in the edge list.", file=sys.stderr)
            return None

        adj[u].append(v)
        adj[v].append(u)

    # Return everything
    return n, m, T, D, s_a, t_a, s_b, t_b, adj


# convert the adjacency matrix into a distance matrix
def compute_distance_matrix(n, adj):

    dist = [[-1] * n for _ in range(n)]

    for s in range(n):
        q = deque()
        q.append(s)
        dist[s][s] = 0

        while q:
            u = q.popleft()
            d_u = dist[s][u]
            for v in adj[u]:
                if dist[s][v] == -1:
                    dist[s][v] = d_u + 1
                    q.append(v)

    return dist

if __name__ == "__main__":
    folder = "testcases"

    files = sorted(f for f in os.listdir(folder) if f.endswith(".in"))

    # Excel workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Results"

    # UPDATED HEADER ROW
    ws.append([
        "File", "n", "m", "T", "D",
        "Expected Time (s)", "Actual Time (s)", "Difference (Actual - Expected)"
    ])

    for filename in files:
        full_path = os.path.join(folder, filename)

        print(f"\n===== FILE: {filename} =====")

        instance = read_instance(full_path)
        if instance is None:
            print("Skipping due to read error.")
            continue

        n, m, T, D, s_a, t_a, s_b, t_b, adj = instance
        dist = compute_distance_matrix(n, adj)

        # Run your algorithm
        start_ns = time.perf_counter_ns()
        k, path_a, path_b = bfs5_state_graph_bidirectional(
            adj, dist, s_a, t_a, s_b, t_b, D, T
        )
        end_ns = time.perf_counter_ns()

        actual_time = (end_ns - start_ns) / 1e9
        print("actual =", actual_time)

        # Read expected time from .out
        out_file = os.path.join(folder, filename.replace(".in", ".out"))

        expected_time = None
        if os.path.exists(out_file):
            with open(out_file, "r") as f:
                lines = f.readlines()
                if lines:
                    for line in reversed(lines):
                        if line.strip():
                            try:
                                expected_time = float(line.strip())
                            except ValueError:
                                expected_time = None
                            break

        print("expected =", expected_time)

        # WRITE ROW TO EXCEL
        ws.append([
            filename,
            n, m, T, D,
            expected_time,
            actual_time,
            None if expected_time is None else actual_time - expected_time
        ])

    # Save Excel file
    output_excel = "results.xlsx"
    wb.save(output_excel)
    print("\nResults written to:", output_excel)
