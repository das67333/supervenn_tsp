import numpy as np

DIST_MAX = 10**9

# сложность алгоритма без 2-opt (https://en.wikipedia.org/wiki/2-opt) -
# O(n^2), с 2-opt - O(n^3)
# за секунду отрабатывает: 0 => n=2000, 10 => n=600
TWO_OPT_ITERS_MAX = 10


class Christofides:
    def __init__(self, graph: np.array):
        self.n = graph.shape[0]
        self.odds = []
        self.adjlist = [[] for _ in range(self.n)]
        self.graph = np.array(graph, dtype=np.int64)

    def find_mst(self):
        key = [DIST_MAX] * self.n
        parent = [0] * self.n
        in_mst = [False] * self.n
        key[0] = 0
        parent[0] = -1
        for i in range(self.n-1):
            key_min, v = DIST_MAX, 0
            for j in range(self.n):
                if not in_mst[j] and key[j] < key_min:
                    key_min, v = key[j], j

            in_mst[v] = True
            for u in range(self.n):
                if self.graph[v, u] and not in_mst[u] and self.graph[v, u] < key[u]:
                    parent[u] = v
                    key[u] = self.graph[v, u]

        for v1 in range(self.n):
            v2 = parent[v1]
            if v2 != -1:
                self.adjlist[v1].append(v2)
                self.adjlist[v2].append(v1)

    def perfect_matching(self):
        for r in range(self.n):
            if len(self.adjlist[r]) % 2 == 1:
                self.odds.append(r)
        closest = DIST_MAX
        while self.odds:
            length, first = DIST_MAX, self.odds.pop()
            for v in self.odds:
                if length > self.graph[first, v]:
                    length = self.graph[first, v]
                    closest = v

            self.adjlist[first].append(closest)
            self.adjlist[closest].append(first)
            self.odds.remove(closest)

    def find_euler_cycle(self, pos: int):
        adjlist = self.adjlist[:]
        path, stk = [], []
        stk = []
        while stk or adjlist[pos]:
            if adjlist[pos]:
                stk.append(pos)
                neighbor = adjlist[pos].pop()
                adjlist[neighbor].remove(pos)
                pos = neighbor
            else:
                path.append(pos)
                pos = stk.pop()

        path.append(pos)
        return path

    def make_hamilton_cycle(self, path: list):
        assert path
        length = 0
        curr, next = 0, 1
        visited = [False] * self.n
        root = path[0]
        visited[root] = True
        while next != len(path):
            if visited[path[next]]:
                path.pop(next)
            else:
                length += self.graph[path[curr], path[next]]
                visited[path[next]] = True
                curr, next = next, next + 1

        length += self.graph[path[curr], path[root]]
        return path, length

    def two_opt(self, path: list[int], length: int):
        for i in range(1, self.n-3):
            for j in range(i+2, self.n-1):
                delta = self.graph[path[i-1], path[j-1]] + \
                    self.graph[path[i], path[j]] - \
                    self.graph[path[i-1], path[i]] - \
                    self.graph[path[j-1], path[j]]
                if delta < 0:
                    length += delta
                    path[i:j] = path[j-1:i-1:-1]
        return path, length

    def find_path(self):
        self.find_mst()
        self.perfect_matching()

        # оставшуюся часть функции можно запускать
        # несколько раз и рандомить стартовую вершину
        start_pos = 0
        path = self.find_euler_cycle(start_pos)
        path, length = self.make_hamilton_cycle(path)

        length_prev = DIST_MAX
        iters_left = TWO_OPT_ITERS_MAX
        while length < length_prev and iters_left > 0:
            length_prev = length
            path, length = self.two_opt(path, length)
            iters_left -= 1
        return length, path


if __name__ == '__main__':
    from brute_force import *
    from held_karp import *
    from gen_graph import *

    # Сравнение с точным решением
    graph = gen_graph(sets_num=300, elems_num=16)

    t1 = perf_counter()
    a = Christofides(graph).find_path()
    t2 = perf_counter()
    assert a[0] == calc_len(graph, a[1])
    print(f'Christofides (approximate)\n'
          f'Duration:\t{t2-t1:.6f} sec\tLength:\t{a[0]}')

    t1 = perf_counter()
    b = held_karp(graph)
    t2 = perf_counter()
    assert b[0] == calc_len(graph, b[1])
    print(f'Held-Karp (precise)\n'
          f'Duration:\t{t2-t1:.6f} sec\tLength:\t{b[0]}')
