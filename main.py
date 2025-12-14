import sys
import time
import os
import argparse
from collections import deque
from openpyxl import Workbook
from solver_methods import bfs_on_new_graph

def read_instance(filename):

    try:
        with open(filename, "r") as f:
            tokens = f.read().split()
    except FileNotFoundError:
        print(f"Error: file '{filename}' not found.", file=sys.stderr)
        return None

    # we use a iterator
    it = iter(tokens)
    try:
        n = int(next(it))
        m = int(next(it))
        T = int(next(it))
        D = int(next(it))

        # we index from 0
        s_a = int(next(it)) - 1
        t_a = int(next(it)) - 1
        s_b = int(next(it)) - 1
        t_b = int(next(it)) - 1
    except StopIteration:
        print("Error: input ended unexpectedly in the header.", file=sys.stderr)
        return None

    # We create the adjacency list
    adj = [[] for _ in range(n)]
    for _ in range(m):
        try:
            u = int(next(it)) - 1
            v = int(next(it)) - 1
        except StopIteration:
            print("Error: input ended unexpectedly in the edge list.", file=sys.stderr)
            return None

        adj[u].append(v)
        adj[v].append(u)

    return n, m, T, D, s_a, t_a, s_b, t_b, adj


# converts the adjacency matrix into a distance matrix
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

    # getting the argument for the folder
    parser = argparse.ArgumentParser(
        description="Run the solver on all .in files in a folder and write results to an Excel file."
    )
    parser.add_argument(
        "-f", "--folder", default="testcases",
        help="Folder containing input .in files (and optional matching .out files). Default: testcases"
    )
    args = parser.parse_args()

    folder = args.folder
    if not os.path.isdir(folder):
        print(f"Error: folder '{folder}' does not exist.", file=sys.stderr)
        sys.exit(1)

    # all the input files
    files = sorted(f for f in os.listdir(folder) if f.endswith(".in"))

    # creating the workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Results"

    # the header row
    ws.append([
        "File", "n", "m", "T", "D", "k - algorithm", "k - solution",
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

        # run the algorithm
        start_ns = time.perf_counter_ns()

        dist = compute_distance_matrix(n, adj)
        k, path_a, path_b = bfs_on_new_graph( n, adj, dist, s_a, t_a, s_b, t_b, D, T )

        end_ns = time.perf_counter_ns()

        running_time = (end_ns - start_ns) / 1e9
        print("Running time =", running_time)

        # retrieving the example running time from .out file
        out_file = os.path.join(folder, filename.replace(".in", ".out"))

        k_out = None
        expected_time = None

        if os.path.exists(out_file):
            with open(out_file, "r") as f:
                lines = f.readlines()

                if len(lines) >= 1:
                    first_line = lines[0].strip()
                    if first_line:
                        k_token = first_line.split()[0]
                        k_str = k_token
                        try:
                            k_out = float(k_str)
                        except ValueError:
                            k_out = None

                expected_time = None
                for raw in reversed(lines):
                    line = raw.strip()
                    if not line:
                        continue  # skip empty trailing lines
                    first_token = line.split()[0]
                    number_str = first_token.replace(",", ".")  # "8,9" -> "8.9"
                    try:
                        expected_time = float(number_str)  # 8.9
                    except ValueError:
                        expected_time = None
                    break

        print("expected =", expected_time)

        # write the row in excel
        ws.append([
            filename,
            n, m, T, D, k, k_out,
            expected_time,
            running_time,
            None if expected_time is None else running_time - expected_time
        ])

    # writes an excel file with the results from each of the files in that folder
    output_excel = "results_trash.xlsx"
    wb.save(output_excel)
    print("\nResults written to:", output_excel)