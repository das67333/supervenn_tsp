import numpy as np

DIST_MAX = 10**9


def faster_christofides(graph: np.array, two_opt_iters_max=10):
    '''
    Faster christofides (with approximate minimum-weight perfect matching)

    Complexity: (without 2-opt https://en.wikipedia.org/wiki/2-opt) - O(n^2),
    single 2-opt iteration - O(n^2) ... O(n^3);
    '''
    return Christofides(graph, two_opt_iters_max).find_path()


def faster_multichristofides(graph: np.array, two_opt_iters_max=10):
    '''
    Faster christofides (with approximate minimum-weight perfect matching)
    which runs n times and chooses the shortest path found

    Complexity: (without 2-opt https://en.wikipedia.org/wiki/2-opt) - O(n^2),
    single 2-opt iteration - O(n^2) ... O(n^3);
    '''
    return Christofides(graph, two_opt_iters_max).find_path(multi=True)


class Christofides:
    def __init__(self, graph: np.array, two_opt_iters_max: int):
        self.n = graph.shape[0]
        self.odds = []
        self.adjlist = [[] for _ in range(self.n)]
        self.graph = np.array(graph, dtype=np.int32)
        self.two_opt_iters_max = two_opt_iters_max

    def find_mst(self):
        # prim's algorithm
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
        adjlist = [x[:] for x in self.adjlist]
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

        length += self.graph[path[curr], root]
        return path, length

    def two_opt(self, path: list, length: int):
        for _ in range(self.two_opt_iters_max):
            length_prev = length
            for i in range(1, self.n-3):
                for j in range(i+2, self.n-1):
                    delta = self.graph[path[i-1], path[j-1]] + \
                        self.graph[path[i], path[j]] - \
                        self.graph[path[i-1], path[i]] - \
                        self.graph[path[j-1], path[j]]
                    if delta < 0:
                        length += delta
                        path[i:j] = path[j-1:i-1:-1]
            if length == length_prev:
                break
        return path, length

    def find_path(self, multi=False):
        self.find_mst()
        self.perfect_matching()

        path_best, length_best = None, DIST_MAX
        start_pos = 0
        while (not path_best or multi) and start_pos != self.n:
            path = self.find_euler_cycle(start_pos)
            path, length = self.make_hamilton_cycle(path)
            path, length = self.two_opt(path, length)
            if length_best > length:
                length_best = length
                path_best = path[:]
            start_pos += 1
        assert path_best
        return path_best, length_best
