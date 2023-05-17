import matplotlib.pyplot as plt
import random
from time import perf_counter
import numpy as np

from gen_graph_faster import gen_graph
from faster_christofides_cython import faster_christofides_cython, faster_multichristofides_cython


n_min, n_limit, n_step, repetitions = 350, 350, 1, 10
plt.title('Approximate algorithms')
plt.xlabel('number of vertices (including separator vertex)')
plt.ylabel('average time in seconds, 100 repetitions')
plt.grid(True)


for func in (faster_multichristofides_cython, ):
    random.seed(42)

    x, y = [], []

    for n in range(n_min, n_limit + 1, n_step):
        s1 = perf_counter()
        dur = 0.0
        for i in range(repetitions):
            graph = gen_graph(n)
            t1 = perf_counter()
            length = func(graph)[1]
            t2 = perf_counter()
            dur += t2 - t1

        s2 = perf_counter()
        print(f'{s2-s1:>8.3f} sec\t{n=:>2}')

        x.append(n)
        y.append(dur / repetitions)

    plt.plot(x, y, label=func.__name__)

    # сохраняем на будущее
    with open('lengths_perfomance.txt', mode='a') as file:
        file.write(f'(\n'
                   f'\'{func.__name__}\',\n'
                   f'{x},\n'
                   f'{y}\n'
                   f'),\n\n')

plt.legend()
plt.show()
