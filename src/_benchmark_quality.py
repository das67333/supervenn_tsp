import matplotlib.pyplot as plt
import random
import numpy as np
from time import perf_counter

from gen_graph import gen_graph, calc_len
from faster_christofides import faster_christofides, faster_multichristofides
from faster_christofides_cython import faster_christofides_cython, faster_multichristofides_cython


percentile = 99
lengths_precomputed = np.loadtxt('lengths_precomputed.txt', dtype=np.int32)
n_limit = lengths_precomputed.shape[0]
n_start, n_limit, n_step, repetitions = 5, 20, 1, 1000
plt.title(f'Heuristics quality ({percentile} percentile)')
plt.xlabel('number of vertices (including separator vertex)')
plt.ylabel('path length divided by the shortest,\n1000 repetitions')
plt.ylim((1.0, 1.1))
plt.grid(True)


def func1(graph):
    n = graph.shape[0]
    visited = [False] * n
    visited[0] = True
    path = [0]
    while not all(visited):
        closest = 10**9
        dist = 10**9
        for i in range(n):
            if not visited[i] and dist > graph[path[-1]][i]:
                dist = graph[path[-1]][i]
                closest = i
        visited[closest] = True
        path.append(closest)
    return path, calc_len(graph, path)


def func2(graph):
    return faster_christofides_cython(graph, 0)


def func3(graph):
    return faster_christofides_cython(graph)

def func4(graph):
    return faster_multichristofides_cython(graph)


func1.__name__ = 'greedy'
func2.__name__ = 'faster_chrisofides (no two-opt)'
func3.__name__ = 'faster_chrisofides (default)'
func4.__name__ = 'faster_multichrisofides (default)'

for func in (func1, func2, func3, func4,):
    random.seed(42)

    x, y = [], []
    t1 = perf_counter()

    for n in range(n_start, n_limit + n_step, n_step):
        ratios = np.zeros(repetitions, dtype=np.float64)
        for i in range(repetitions):
            graph = gen_graph(n)
            length_best = lengths_precomputed[n, i]
            length = func(graph)[1]
            assert length >= length_best
            ratios[i] = length / length_best

        t2 = perf_counter()
        print(f'{t2-t1:>8.3f} sec\t{n=:>2}')
        t1 = t2

        x.append(n)
        y.append(np.percentile(ratios, percentile))

    plt.plot(x, y, label=func.__name__)

plt.legend()
plt.show()
