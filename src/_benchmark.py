import numpy as np
import matplotlib.pyplot as plt
from time import perf_counter
import random

from gen_graph import gen_graph, calc_len
from faster_christofides_cython import faster_christofides_cython, get_timer

random.seed(42)

funcs = [faster_christofides_cython]
n_limits = [2000]
n_start, n_step, repetitions = 5, 50, 100
plt.title('Faster-Christofides')
# plt.yscale('log')

for func, n_limit in zip(funcs, n_limits):
    x, y = [], []

    for n in range(n_start, n_limit + n_step + 1, n_step): # (2_000, ):
        timer_total = 0.0

        for _ in range(repetitions):
            graph = gen_graph(n)

            t1 = perf_counter()
            path, length = func(graph)
            t2 = perf_counter()
            timer_total += t2 - t1

        x.append(n)
        y.append(timer_total / repetitions)
        print(f'{n=}')
        print(timer_total / repetitions)
        print(get_timer() / repetitions)

    plt.plot(x, y, label=func.__name__)

    print(length, calc_len(graph, path), path)
    # сохраняем на будущее
    with open('graphs_data.txt', mode='a') as file:
        file.write(f'{func.__name__}:\n{x}\n{y}\n\n')

plt.legend()
plt.show()
