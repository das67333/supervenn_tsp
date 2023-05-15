from itertools import permutations
import numpy as np

DIST_MAX = 10**9


def brute_force_recursive(graph: np.array):
    def inner(v, visited, len_curr, path_curr):
        visited[v] = True
        if len(path_curr) == n:
            nonlocal len_best, path_best
            if len_best > len_curr + graph[v, 0]:
                len_best = len_curr + graph[v, 0]
                path_best = path_curr[:]
            return
        for j in range(n):
            if visited[j]:
                continue
            visited[j] = True
            path_curr.append(j)
            inner(j, visited, len_curr + graph[v, j], path_curr)
            path_curr.pop()
            visited[j] = False

    n = graph.shape[0]
    len_best = DIST_MAX
    path_curr = [0]
    path_best = None
    visited = [False] * n
    visited[0] = True
    inner(0, visited, 0, path_curr)
    assert path_best is not None
    return len_best, path_best


def brute_force_permutative(graph: np.array):
    n = graph.shape[0]
    len_best = DIST_MAX
    path_best = None
    for perm in permutations(range(n-1)):
        len_curr = graph[perm[n-2], n-1] + graph[n-1, perm[0]]
        for i in range(n-2):
            len_curr += graph[perm[i], perm[i+1]]
        if len_best > len_curr:
            len_best = len_curr
            path_best = [*perm, n-1]
    return len_best, path_best
