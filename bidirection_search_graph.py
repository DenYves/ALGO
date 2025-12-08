from collections import deque
# just goes from s to t directly
def bfs_state_graph_bidirectional(adj, dist, s_a, t_a, s_b, t_b, D, T):
    n = len(adj)
    N_states = n * n

    # encode (x, y) as single index
    start = s_a * n + s_b
    goal  = t_a * n + t_b

    # start and goal must be valid pairs
    d_start = dist[s_a][s_b]
    if d_start != -1 and d_start <= D:
        return T + 1, [], []

    d_goal = dist[t_a][t_b]
    if d_goal != -1 and d_goal <= D:
        return T + 1, [], []

    if start == goal:
        return 0, [s_a + 1], [s_b + 1]

    dist_s   = [-1] * N_states
    dist_t   = [-1] * N_states
    parent_s = [-1] * N_states
    parent_t = [-1] * N_states

    q_s = deque([start])
    q_t = deque([goal])

    dist_s[start] = 0
    dist_t[goal]  = 0

    meeting_state = -1

    while q_s or q_t:
        # choose side: expand smaller frontier
        if not q_s:
            side = 1
        elif not q_t:
            side = 0
        elif len(q_s) <= len(q_t):
            side = 0
        else:
            side = 1

        if side == 0:
            # expand from start side
            cur = q_s.popleft()
            d_cur = dist_s[cur]
            if d_cur >= T:
                continue

            x = cur // n
            y = cur % n

            # A moves, B moves
            for nx in adj[x]:
                for ny in adj[y]:
                    if nx == x and ny == y:
                        continue
                    d_xy = dist[nx][ny]
                    if d_xy != -1 and d_xy <= D:
                        continue
                    nxt = nx * n + ny
                    if dist_s[nxt] != -1:
                        continue
                    dist_s[nxt]   = d_cur + 1
                    parent_s[nxt] = cur
                    q_s.append(nxt)
                    if dist_t[nxt] != -1:
                        meeting_state = nxt
                        q_s.clear()
                        q_t.clear()
                        break
                if meeting_state != -1:
                    break

            if meeting_state != -1:
                break

            # A moves, B stays
            for nx in adj[x]:
                ny = y
                if nx == x and ny == y:
                    continue
                d_xy = dist[nx][ny]
                if d_xy != -1 and d_xy <= D:
                    continue
                nxt = nx * n + ny
                if dist_s[nxt] != -1:
                    continue
                dist_s[nxt]   = d_cur + 1
                parent_s[nxt] = cur
                q_s.append(nxt)
                if dist_t[nxt] != -1:
                    meeting_state = nxt
                    q_s.clear()
                    q_t.clear()
                    break

            if meeting_state != -1:
                break

            # A stays, B moves
            nx = x
            for ny in adj[y]:
                if nx == x and ny == y:
                    continue
                d_xy = dist[nx][ny]
                if d_xy != -1 and d_xy <= D:
                    continue
                nxt = nx * n + ny
                if dist_s[nxt] != -1:
                    continue
                dist_s[nxt]   = d_cur + 1
                parent_s[nxt] = cur
                q_s.append(nxt)
                if dist_t[nxt] != -1:
                    meeting_state = nxt
                    q_s.clear()
                    q_t.clear()
                    break

            if meeting_state != -1:
                break

            # A stays, B stays (self loop) -> always skip

        else:
            # expand from target side
            cur = q_t.popleft()
            d_cur = dist_t[cur]
            if d_cur >= T:
                continue

            x = cur // n
            y = cur % n

            # A moves, B moves
            for nx in adj[x]:
                for ny in adj[y]:
                    if nx == x and ny == y:
                        continue
                    d_xy = dist[nx][ny]
                    if d_xy != -1 and d_xy <= D:
                        continue
                    nxt = nx * n + ny
                    if dist_t[nxt] != -1:
                        continue
                    dist_t[nxt]   = d_cur + 1
                    parent_t[nxt] = cur
                    q_t.append(nxt)
                    if dist_s[nxt] != -1:
                        meeting_state = nxt
                        q_s.clear()
                        q_t.clear()
                        break
                if meeting_state != -1:
                    break

            if meeting_state != -1:
                break

            # A moves, B stays
            for nx in adj[x]:
                ny = y
                if nx == x and ny == y:
                    continue
                d_xy = dist[nx][ny]
                if d_xy != -1 and d_xy <= D:
                    continue
                nxt = nx * n + ny
                if dist_t[nxt] != -1:
                    continue
                dist_t[nxt]   = d_cur + 1
                parent_t[nxt] = cur
                q_t.append(nxt)
                if dist_s[nxt] != -1:
                    meeting_state = nxt
                    q_s.clear()
                    q_t.clear()
                    break

            if meeting_state != -1:
                break

            # A stays, B moves
            nx = x
            for ny in adj[y]:
                if nx == x and ny == y:
                    continue
                d_xy = dist[nx][ny]
                if d_xy != -1 and d_xy <= D:
                    continue
                nxt = nx * n + ny
                if dist_t[nxt] != -1:
                    continue
                dist_t[nxt]   = d_cur + 1
                parent_t[nxt] = cur
                q_t.append(nxt)
                if dist_s[nxt] != -1:
                    meeting_state = nxt
                    q_s.clear()
                    q_t.clear()
                    break

            if meeting_state != -1:
                break

    if meeting_state == -1:
        return T + 1, [], []

    # reconstruct
    path_s_states = []
    cur = meeting_state
    while cur != -1:
        path_s_states.append(cur)
        cur = parent_s[cur]
    path_s_states.reverse()

    path_t_states = []
    cur = meeting_state
    while cur != -1:
        path_t_states.append(cur)
        cur = parent_t[cur]

    full_states = path_s_states + path_t_states[1:]
    k = len(full_states) - 1
    if k > T:
        return T + 1, [], []

    path_a = []
    path_b = []
    for st in full_states:
        x = st // n
        y = st % n
        path_a.append(x + 1)
        path_b.append(y + 1)

    return k, path_a, path_b
