from time import perf_counter
from src.faster_christofides import faster_multichristofides
from src.faster_christofides_cython import faster_multichristofides_cython
import json
import numpy as np
from collections import defaultdict


def break_into_chunks(sets):
    all_items = set.union(*sets)
    chunks_dict = defaultdict(set)
    for item in all_items:
        occurrence_pattern = frozenset(
            {i for i, set_ in enumerate(sets) if item in set_})
        chunks_dict[occurrence_pattern].add(item)
    return dict(chunks_dict)


def get_chunks_and_composition_array(sets):
    chunks_dict = break_into_chunks(sets)
    chunks_count = len(chunks_dict)
    chunks = []
    arr = np.zeros((len(sets), chunks_count), dtype=np.int32)

    for idx, (sets_indices, items) in enumerate(chunks_dict.items()):
        chunks.append(items)
        arr[list(sets_indices), idx] = 1

    return chunks, arr


s1 = perf_counter()
with open('all_sets.json') as file:
    data = json.loads(file.read())

time_tsp = 0
for dataset_idx, dataset_name in enumerate(sorted(data)):
    sets = [set(set_elems) for set_elems in data[dataset_name].values()]
    table_T = get_chunks_and_composition_array(sets)[1].T
    n = table_T.shape[0]
    # последняя вершина в графе - разделитель между первым и последним столбцом,
    # поэтому расстояние между ней и любой другой равно 0
    graph = np.zeros((n+1, n+1), dtype=np.int32)
    for i in range(n):
        for j in range(n):
            graph[i, j] = np.sum(np.bitwise_xor(table_T[i], table_T[j]))
    # graph - матрица смежности

    t1 = perf_counter()

    # length = faster_multichristofides(graph)[1]
    length = faster_multichristofides_cython(graph)[1]

    t2 = perf_counter()
    time_tsp += t2 - t1
    print(f'{dataset_idx:>3} {dataset_name:<25} => {length}')

s2 = perf_counter()
print(f'time_total\t=\t{s2-s1}')
print(f'time_tsp  \t=\t{time_tsp}')
