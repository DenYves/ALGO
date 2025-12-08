from collections import deque

def bfs_state_graph(adj, dist, s_a, t_a, s_b, t_b, D, T):
    """
    BFS in the state graph whose nodes are pairs (x, y), with:
      - x, y are vertices of the original graph
      - (x, y) is a valid state iff dist[x][y] > D, where
        dist[x][y] is the shortest-path distance in the original graph
        (dist[x][y] == -1 is treated as 'infinite', so also > D)

    An edge ((x1, y1), (x2, y2)) exists iff:
      - x2 in N(x1) ∪ {x1}
      - y2 in N(y1) ∪ {y1}
      - and (x1, y1) != (x2, y2) (no self-loop)

    We find the shortest path from (s_a, s_b) to (t_a, t_b) with BFS.

    Returns:
      k, path_a, path_b
    where:
      - k is the minimum number of time steps (edges in state graph),
        or T+1 if no solution with k <= T
      - path_a is the sequence of vertices for A (1-based indices)
      - path_b is the sequence of vertices for B (1-based indices)
        (empty lists if no solution)
    """
    n = len(adj)

    # Helper to test if a pair (x, y) is allowed: dist[x][y] > D,
    # treating dist == -1 as 'infinite' (also allowed).
    def valid_pair(x, y):
        d_xy = dist[x][y]
        return (d_xy == -1) or (d_xy > D)

    # Check if start / target states are valid
    if not valid_pair(s_a, s_b) or not valid_pair(t_a, t_b):
        return T + 1, [], []

    # Encode (x, y) as a single integer x * n + y
    def encode(x, y):
        return x * n + y

    def decode(state):
        return divmod(state, n)  # (x, y)

    start = encode(s_a, s_b)
    goal = encode(t_a, t_b)

    # Standard BFS arrays on the state graph
    N_states = n * n
    visited = [False] * N_states
    dist_state = [-1] * N_states
    parent = [-1] * N_states

    q = deque()
    q.append(start)
    visited[start] = True
    dist_state[start] = 0

    while q:
        cur = q.popleft()
        d_cur = dist_state[cur]

        # If we already reached the target, we can stop (BFS guarantees minimality)
        if cur == goal:
            break

        # We can optionally prune by T here; if we exceed T there is no valid solution
        if d_cur == T:
            continue

        x, y = decode(cur)

        # Possible moves for A and B: stay or move to a neighbour
        # (we include x and y themselves in the lists)
        neigh_x = [x] + adj[x]
        neigh_y = [y] + adj[y]

        for nx in neigh_x:
            for ny in neigh_y:
                # No self loop: skip (x, y) -> (x, y)
                if nx == x and ny == y:
                    continue

                # Pair must be at distance > D (or unreachable)
                if not valid_pair(nx, ny):
                    continue

                nxt = encode(nx, ny)
                if not visited[nxt]:
                    visited[nxt] = True
                    dist_state[nxt] = d_cur + 1
                    parent[nxt] = cur
                    q.append(nxt)

    # If we never reached goal, no solution
    if not visited[goal]:
        return T + 1, [], []

    k = dist_state[goal]
    if k > T:
        # Path exists but is too long
        return T + 1, [], []

    # Reconstruct the path in the state graph: sequence of (x, y)
    states = []
    cur = goal
    while cur != -1:
        states.append(cur)
        cur = parent[cur]
    states.reverse()

    # Extract the individual paths for A and B (convert back to 1-based indices)
    path_a = []
    path_b = []
    for st in states:
        x, y = decode(st)
        path_a.append(x + 1)
        path_b.append(y + 1)

    return k, path_a, path_b
