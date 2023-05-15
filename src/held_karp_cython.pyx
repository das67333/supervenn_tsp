from itertools import combinations
import numpy as np
cimport cython

DIST_MAX = 10**9

@cython.boundscheck(False)
@cython.wraparound(False)
def held_karp_cython(int[:, ::1] graph):
    '''
    Bellman-Held-Karp algorithm (dynamic programming approach)

    Time complexity: O(n^2 * 2^n)
    Memory consumption: O(n * 2^n)
    '''
    cdef Py_ssize_t n = graph.shape[0]
    assert n < 25, 'Algorithm would occupy more that 2GB of RAM'

    dp = np.full((n-1, 1 << (n-1)), DIST_MAX, dtype=np.int32)
    cdef int[:, :] dp_view = dp
    prev = np.zeros((n-1, 1 << (n-1)), dtype=np.uint8)
    cdef unsigned char[:, :] prev_view = prev

    cdef Py_ssize_t v, k
    cdef int bitset1, bitset2, v1, v2
    for v in range(n-1):
        dp_view[v, 1 << v] = graph[n-1, v]
        prev_view[v, 1 << v] = n-1
    for k in range(2, n):
        for comb_tuple in combinations(range(n-1), k):
            comb_int = 0
            for x in comb_tuple:
                comb_int ^= 1 << x
            bitset1 = comb_int
            for v1 in range(n-1):
                if bitset1 & (1 << v1):
                    bitset2 = bitset1 ^ (1 << v1)
                    for v2 in range(n-1):
                        if bitset2 & (1 << v2) and dp_view[v1, bitset1] > dp_view[v2, bitset2] + graph[v2, v1]:
                            dp_view[v1, bitset1] = dp_view[v2, bitset2] + graph[v2, v1]
                            prev_view[v1, bitset1] = v2
    cdef int len_best = DIST_MAX, v_last = -1, s_last = (1 << (n-1)) - 1
    for k in range(n-1):
        if len_best > dp_view[k, s_last] + graph[k, n-1]:
            len_best = dp_view[k, s_last] + graph[k, n-1]
            v_last = k
    assert v_last != -1
    path_best = [n-1]
    while v_last != n-1:
        path_best.append(v_last)
        s_last ^= 1 << v_last
        v_last = prev[v_last, s_last ^ (1 << v_last)]
    return int(len_best), path_best
