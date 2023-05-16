import matplotlib.pyplot as plt
import random

from gen_graph import gen_graph
from held_karp_cython import held_karp_cython
from faster_christofides_cython import faster_christofides_cython

random.seed(42)

n_start, n_step, repetitions = 5, 1, 1000
plt.title('Heuristics quality')
plt.xlabel('number of vertices (including separator vertex)')
plt.ylabel('path length divided by optimal,\n average of 1000 repetitions')
plt.ylim((1.0, 1.1))
plt.grid(True)

def two_opt(graph):
    return faster_christofides_cython(graph, 0)

two_opt.__name__ = 'random path + two_opt'

for func, n_limit in ((two_opt, 18), ):
    x, y = [], []

    for n in range(n_start, n_limit + n_step, n_step):
        ratio_sum = 0
        for _ in range(repetitions):
            graph = gen_graph(n)

            length_best = held_karp_cython(graph)[1]
            length = func(graph)[1]
            assert length >= length_best
            ratio_sum += length / length_best

        x.append(n)
        y.append(ratio_sum / repetitions)
        print(f'{n=}')

    plt.plot(x, y, label=func.__name__)

    # сохраняем на будущее
    with open('lengths_comparison.txt', mode='a') as file:
        file.write(f'(\n'
                   f'\'{func.__name__}\',\n'
                   f'{x},\n'
                   f'{y}\n'
                   f')\n\n')

plt.legend()
plt.show()
