import unittest
from brute_force import brute_force_permutative, brute_force_recursive
from held_karp import held_karp
from held_karp_cython import held_karp_cython
from faster_christofides import faster_christofides
from faster_christofides_cython import faster_christofides_cython

from gen_graph import *


class Tests(unittest.TestCase):
    def setUp(self):
        random.seed(42)

    def test_precise(self):
        elems_num, graphs_num = 7, 100
        for graph in map(lambda _: gen_graph(elems_num), range(graphs_num)):
            len_best = -1

            for func in (brute_force_permutative, brute_force_recursive, held_karp, held_karp_cython):
                path, length = func(graph)
                if len_best == -1:
                    len_best = length
                self.assertEqual(elems_num, len(path))
                real_length = calc_len(graph, path)
                self.assertEqual(length, real_length, f'{func.__name__}')
                self.assertEqual(len_best, length, f'{func=}')

    def test_approximate(self):
        elems_num, graphs_num = 13, 100
        for graph in map(lambda _: gen_graph(elems_num), range(graphs_num)):
            len_best = held_karp_cython(graph)[1]

            for func in (faster_christofides, faster_christofides_cython):
                path, length = func(graph)
                self.assertEqual(elems_num, len(path))
                real_length = calc_len(graph, path)
                self.assertEqual(length, real_length, f'{func.__name__}')
                self.assertLessEqual(len_best, length, f'{func=}')


if __name__ == '__main__':
    unittest.main()
