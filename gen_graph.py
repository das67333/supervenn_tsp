import random
import numpy as np


def gen_vertex(sets_num: int):
    return b''.join(map(lambda _: random.choice([b'0', b'1']), range(sets_num)))


def hamming_distance(v1: bytes, v2: bytes):
    assert (len(v1) == len(v2))
    t = 0
    for (x, y) in zip(v1, v2):
        if x != y:
            t += 1
    return t


def gen_graph(sets_num: int, elems_num: int):
    # предполагается, что алгоритмы не вставляют виртуальную вершину
    # самостоятельно и просто ищут замкнутый путь 
    vertices = [gen_vertex(sets_num) for _ in range(elems_num)]
    graph = np.zeros((elems_num, elems_num), dtype=np.uint64)
    for i in range(elems_num):
        for j in range(elems_num):
            graph[i, j] = hamming_distance(vertices[i], vertices[j])
    return graph

def calc_len(graph: np.array, path: list):
    n = graph.shape[0]
    result = graph[path[0], path[n-1]]
    for i in range(n-1):
        result += graph[path[i], path[i+1]]
    return result


if __name__ == '__main__':
    sets_num = 40
    elems_num = 11
    np.savetxt('graph.txt', gen_graph(sets_num, elems_num), '%d')
