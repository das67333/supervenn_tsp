from itertools import combinations
import numpy as np
from time import perf_counter

def held_karp(graph: np.array):
    n = graph.shape[0] - 1
    dp = np.full((n, 1 << n), np.inf, dtype=np.float64)
    prev = np.full((n, 1 << n), -1, dtype=np.int8)
    for v in range(n):
        dp[v, 1 << v] = graph[n, v]
        prev[v, 1 << v] = n
    for k in range(2, n+1):
        for comb_tuple in combinations(range(n), k):
            comb_int = 0
            for x in comb_tuple:
                comb_int ^= 1 << x
            for v in comb_tuple:
                # val = np.inf
                for u in comb_tuple:
                    if u == v:
                        continue
                    if dp[v, comb_int] > dp[u, comb_int ^ (1 << v)] + graph[u, v]:
                        dp[v, comb_int] = dp[u, comb_int ^
                                             (1 << v)] + graph[u, v]
                        prev[v, comb_int] = u
                # dp[v, comb_int] = val
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

    # for i in range(1000):
    #     print(i)
    #     graph = gen_graph(2000, 7)
    #     a = held_karp(graph)
    #     b = brute_force_permutative(graph)
    #     assert a[0] == b[0]
    #     assert a[0] == calc_len(graph, a[1])
    #     assert b[0] == calc_len(graph, b[1])

    graph = gen_graph(30, 18)
    # graph = np.loadtxt('graph.txt')
    t1 = perf_counter()
    a = held_karp(graph)
    t2 = perf_counter()
    print(t2-t1)
    print(a)
