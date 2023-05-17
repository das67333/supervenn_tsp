import matplotlib.pyplot as plt
import random
from time import perf_counter
import numpy as np

from gen_graph_faster import gen_graph
from faster_christofides_cython import faster_christofides_cython


n_min, n_limit, n_step, repetitions = 5, 5000, 500, 100
plt.title('Approximate algorithms')
plt.xlabel('number of vertices (including separator vertex)')
plt.ylabel('average time in seconds, 100 repetitions')
plt.grid(True)


# for func in (faster_christofides_cython, ):
#     random.seed(42)

#     x, y = [], []

#     for n in range(0, n_limit + 1, n_step):
#         n = max(n, n_min)
#         s1 = perf_counter()
#         dur = 0.0
#         for i in range(repetitions):
#             graph = gen_graph(n)
#             t1 = perf_counter()
#             length = func(graph)[1]
#             t2 = perf_counter()
#             dur += t2 - t1

#         s2 = perf_counter()
#         print(f'{s2-s1:>8.3f} sec\t{n=:>2}')

#         x.append(n)
#         y.append(dur / repetitions)

#     plt.plot(x, y, label=func.__name__)

#     # сохраняем на будущее
#     with open('lengths_perfomance.txt', mode='a') as file:
#         file.write(f'(\n'
#                    f'\'{func.__name__}\',\n'
#                    f'{x},\n'
#                    f'{y}\n'
#                    f'),\n\n')

for name, x, y in (
(
'faster_christofides',
[5, 15, 25, 35, 45, 55, 65, 75, 85, 95, 105, 115, 125, 135, 145, 155, 165, 175, 185, 195, 205, 215, 225, 235, 245, 255, 265, 275, 285, 295, 305, 315, 325, 335, 345, 355, 365, 375, 385, 395, 405],
[4.091300999789382e-05, 0.0005009712299761304, 0.001763049820146989, 0.00400126803009698, 0.007231934359988372, 0.011959530929962056, 0.017718098099976487, 0.02483957088988973, 0.03271447276010804, 0.0451397987000928, 0.054468355160024656, 0.06789760417997968, 0.08235333579990765, 0.09799880576008946, 0.11741820362003637, 0.1376123831300356, 0.15811421545995472, 0.18105887342999266, 0.20200583598994853, 0.2297198752598888, 0.26332986426996285, 0.28418148441011, 0.31256375635006406, 0.3523860108900044, 0.3919793866300097, 0.42080266199000105, 0.48471372669997437, 0.515005844629959, 0.5347718867400363, 0.5825225586700618, 0.6401105153699064, 0.6748039576000338, 0.7295352602699858, 0.7908848458898683, 0.8765727403600795, 0.9376088783199884, 0.9746463760599363, 1.0450306225501118, 1.0961560383501092, 1.1775898335800958, 1.247519387979737]
),

(
'faster_christofides_cython',
[5, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000],
[3.6696709867101165e-05, 0.00866878201981308, 0.03445111237917445, 0.0831726893800078, 0.14678629757923772, 0.23200776903133374, 0.33504147389016, 0.4583133657580765, 0.6101914628203667, 0.7827836222898622, 0.99123371473921]
),
):
    plt.plot(x, y, label=name)

plt.legend()
plt.show()
