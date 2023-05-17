import random
import numpy as np


def gen_graph(elems_num: int, sets_num=300):
    # уже содержит виртуальную вершину-разделитель среди elems_num
    # random.getrandbits(sets_num) не быстрее
    vertices = [random.randint(0, 2**sets_num-1) for _ in range(elems_num - 1)]
    graph = np.zeros((elems_num, elems_num), dtype=np.int32)
    cdef int[:, :] graph_view = graph
    # вершина (elems_num-1) - разделитель

    cdef int i, j, n = elems_num - 1
    for i in range(n):
        for j in range(i):
            graph_view[i, j] = graph_view[j, i]
        for j in range(i+1, n):
            graph_view[i, j] = (vertices[i] ^ vertices[j]).bit_count()

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
