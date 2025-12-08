import sys
import time
from collections import deque
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
    folder = "testcases"  # folder with your .in files

    # list all files ending with .in
    files = sorted(f for f in os.listdir(folder) if f.endswith(".in"))

    for filename in files:
        full_path = os.path.join(folder, filename)

        print(f"\n===== FILE: {filename} =====")

        instance = read_instance(full_path)
        if instance is None:
            print("Skipping due to read error.")
            continue

        n, m, T, D, s_a, t_a, s_b, t_b, adj = instance
        dist = compute_distance_matrix(n, adj)

        start_ns = time.perf_counter_ns()
        k, path_a, path_b = bfs5_state_graph_bidirectional(
            adj, dist, s_a, t_a, s_b, t_b, D, T
        )
        end_ns = time.perf_counter_ns()

        # Print the output in assignment format, but with filename first
        print("n =", n, "m =", m, "T =", T, "D =", D)
        print("k =", k)

        if k <= T:
            print("path_a =", " ".join(map(str, path_a)))
            print("path_b =", " ".join(map(str, path_b)))

        print("elapsed_seconds =", (end_ns - start_ns) / 1e9)
        print("==============================")
