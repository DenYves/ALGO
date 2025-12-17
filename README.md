# README

## What’s in this repository
This repository contains a Python program that solves the provided input instances (the `*.in` files). The code is split into three main files:

- **main.py**: entry point. Reads the input instances, calls the selected algorithm, writes output files, and measures running times.
- **solver_methods.py**: implementation of **Algorithm 1**.
- **initial_solver.py**: implementation of **Algorithm 2**.

The program supports running **many instances at once** by giving it a folder name (it will run all instances inside that folder).

---

## How to run the code (run all instances from a folder)
1. Put all instance files in a folder, for example `folder_name/`.
2. Make sure `folder_name/` is in the **same directory** as `main.py` (and the other Python files).
3. Open a terminal and go to the directory where `main.py` is located.
4. Run:

```bash
python main.py -f folder_name
```
## Output
For each input instance file the program writes a separate output file:
```bash
alg_<input_filename>.out
```

Each instance output file contains the solution produced by the algorithm in the required `.out` format (as printed by the program for that instance).

In addition, the program creates **one Excel file** that summarizes all instances in the folder, including:
- the running time(s)
- the value of `k` found for each instance

The results for the official testcases from Canvas are already included in the report.

---

## Switching from Algorithm 1 to Algorithm 2

By default, `main.py` currently executes **Algorithm 1**.

If you want to execute **Algorithm 2**, change lines **152, 153, 154** in `main.py` to:

```python
dist = compute_distance_matrix0(n, adj)
#dist = compute_distance_matrix1(n, adj, D, t_a, t_b)
k, path_a, path_b = bfs_bidirectional(n, adj, dist, s_a, t_a, s_b, t_b, D, T)
```
