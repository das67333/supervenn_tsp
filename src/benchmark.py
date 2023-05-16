import numpy as np
import matplotlib.pyplot as plt
from time import perf_counter
from held_karp_cython import held_karp_cython
import random
from gen_graph import gen_graph, calc_len

random.seed(42)

funcs = [held_karp_cython]
n_limits = [20]
n_start, repetitions = 5, 1
plt.title('Exponential algorithms')
plt.yscale('log')

for func, n_limit in zip(funcs, n_limits):
    x, y = [], []

    for n in range(n_start, n_limit + 1):
        graph = gen_graph(n)
        t1 = perf_counter()

        for _ in range(repetitions):
            length, path = func(graph)

        t2 = perf_counter()
        dur = (t2 - t1) / repetitions
        x.append(n)
        y.append(dur)
    plt.plot(x, y, label=func.__name__)

    print(length, calc_len(graph, path), path)
    # сохраняем на будущее
    with open('graphs_data.txt', mode='a') as file:
        file.write(f'{func.__name__}:\n{x}\n{y}\n\n')

plt.legend()
plt.show()
