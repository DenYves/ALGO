from collections import deque

def bfs_on_new_graph(n, adj, dist, s_a, t_a, s_b, t_b, D, T):
    # state = (pair << 1) | person, where pair = x * n + y, person in {0, 1}
    # player = 0 : end of real step
    # player = 1 : A has moved, B still has to move

    N_states = n * n * 2

    start_pair = s_a * n + s_b
    goal_pair  = t_a * n + t_b

    # start and goal must be valid pairs (aka distance > D)
    d_start = dist[s_a][s_b]
    if d_start <= D:
        return T + 1, [], []

    d_goal = dist[t_a][t_b]
    if d_goal != -1 and d_goal <= D:
        return T + 1, [], []

    # initial and final states are at the end of a time step (player = 0)
    start = (start_pair << 1) | 0
    goal  = (goal_pair << 1) | 0

    if start == goal:
        return 0, [s_a + 1], [s_b + 1]


    dist_state = [-1] * N_states
    parent = [-1] * N_states

    q = deque([start])
    dist_state[start] = 0

    #start bfs
    while q:

        # current node and distance till there
        cur = q.popleft()
        d_cur = dist_state[cur]

        # stop if we reached the goal
        if cur == goal:
            break

        # each bfs step is a micro-step, at most 2*T micro-steps
        if d_cur >= 2 * T:
            continue

        #decoding
        pair = cur >> 1
        player = cur & 1
        x = pair // n
        y = pair % n

        # ------ pruning if already unreachable ------
        real_so_far = d_cur // 2

        dx = dist[t_a][x]
        dy = dist[t_b][y]

        # analyzing each of the two cases
        if player == 0:
            lb_real = max(dx, dy)
        else:
            lb_real = max(dx, dy - 1)

        if real_so_far + lb_real > T:
            continue
        # ------------------------------------------

        # which person has to move?
        if player == 0:
            # A moves, B stays
            for nx in [x] + adj[x]:

                #encoding
                nxt_pair = nx * n + y
                nxt = (nxt_pair << 1) | 1

                # if not reached yet, add in the queue
                if dist_state[nxt] != -1:
                    continue
                dist_state[nxt] = d_cur + 1
                parent[nxt] = cur
                q.append(nxt)

        else:
            # B moves, A stays
            for ny in [y] + adj[y]:

                # distance constraint
                d_xy = dist[x][ny]
                if d_xy <= D:
                    continue

                # encoding
                nxt_pair = x * n + ny
                nxt = (nxt_pair << 1) | 0

                # if not reached, add in the queue
                if dist_state[nxt] != -1:
                    continue
                dist_state[nxt] = d_cur + 1
                parent[nxt] = cur
                q.append(nxt)

    # if we never reached goal, or we exceeded T real steps, no solution
    if dist_state[goal] == -1:
        return T + 1, [], []

    # real nr of steps
    k = dist_state[goal] // 2

    # recreating the path
    states = []
    cur = goal
    while cur != -1:
        states.append(cur)
        cur = parent[cur]
    states.reverse()

    # we need only the positions from person = 0
    path_a = []
    path_b = []
    for st in states:
        pair = st >> 1
        player = st & 1
        if player != 0:
            continue
        x = pair // n
        y = pair % n
        path_a.append(x + 1)
        path_b.append(y + 1)

    return k, path_a, path_b

