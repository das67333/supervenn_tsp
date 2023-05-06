import numpy as np
from time import perf_counter
from itertools import combinations

DIST_MAX = 1e9


def held_karp(graph: np.array):
    n = graph.shape[0] - 1
    dp = np.full((n, 1 << n), DIST_MAX, dtype=np.float64)
    prev = np.zeros((n, 1 << n), dtype=np.uint8)
    for v in range(n):
        dp[v, 1 << v] = graph[n, v]
        prev[v, 1 << v] = n
    for k in range(2, n+1):
        for comb_tuple in combinations(range(n), k):
            comb_int = 0
            for x in comb_tuple:
                comb_int ^= 1 << x
            for v in comb_tuple:
                for u in comb_tuple:
                    if u == v:
                        continue
                    if dp[v, comb_int] > dp[u, comb_int ^ (1 << v)] + graph[u, v]:
                        dp[v, comb_int] = dp[u, comb_int ^
                                             (1 << v)] + graph[u, v]
                        prev[v, comb_int] = u
    len_best = np.inf
    v_last = -1
    for k in range(k):
        if len_best > dp[k, -1] + graph[k, n]:
            len_best = dp[k, -1] + graph[k, n]
            v_last = k
    assert v_last != -1
    path_best = [n]
    s_last = (1 << n) - 1
    while v_last != n:
        path_best.append(v_last)
        s_last ^= 1 << v_last
        v_last = prev[v_last, s_last ^ (1 << v_last)]
        assert v_last != -1
    return len_best, path_best


if __name__ == '__main__':
    from brute_force import *
    from gen_graph import *

    graph = gen_graph(30, 16)
    # graph = np.loadtxt('graph.txt')

    t1 = perf_counter()
    a = held_karp(graph)
    t2 = perf_counter()

    print(t2-t1)
    print(a)
