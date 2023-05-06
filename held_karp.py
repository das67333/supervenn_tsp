import numpy as np
from time import perf_counter
from itertools import combinations

DIST_MAX = 10**9


def held_karp(graph: np.array):
    n = graph.shape[0]
    dp = np.full((n, 1 << (n-1)), DIST_MAX, dtype=np.int32)
    prev = np.zeros((n-1, 1 << (n-1)), dtype=np.uint8)
    for v in range(n-1):
        dp[v, 1 << v] = graph[n-1, v]
        prev[v, 1 << v] = n-1
    for k in range(2, n):
        for comb_tuple in combinations(range(n-1), k):
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
    len_best, v_last = DIST_MAX, -1
    for k in range(k):
        if len_best > dp[k, -1] + graph[k, n-1]:
            len_best = dp[k, -1] + graph[k, n-1]
            v_last = k
    assert v_last != -1
    path_best = [n-1]
    s_last = (1 << (n-1)) - 1
    while v_last != (n-1):
        path_best.append(v_last)
        s_last ^= 1 << v_last
        v_last = prev[v_last, s_last ^ (1 << v_last)]
        assert v_last != -1
    return len_best, path_best


if __name__ == '__main__':
    from brute_force import *
    from gen_graph import *

    graph = gen_graph(10)

    t1 = perf_counter()
    a = brute_force_recursive(graph)
    t2 = perf_counter()
    assert a[0] == calc_len(graph, a[1])
    print(f'Brute force recursive (precise)\n'
          f'Duration:\t{t2-t1:.6f} sec\tLength:\t{a[0]}\n')

    t1 = perf_counter()
    a = brute_force_permutative(graph)
    t2 = perf_counter()
    assert a[0] == calc_len(graph, a[1])
    print(f'Brute force permutative (precise)\n'
          f'Duration:\t{t2-t1:.6f} sec\tLength:\t{a[0]}\n')

    t1 = perf_counter()
    b = held_karp(graph)
    t2 = perf_counter()
    assert b[0] == calc_len(graph, b[1])
    print(f'Held-Karp (precise)\n'
          f'Duration:\t{t2-t1:.6f} sec\tLength:\t{b[0]}\n')
