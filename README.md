## Файлы

main.ipynb - пример использования supervenn

src/gen_graph.py
- gen_graph - создание графов в виде списков смежности
- calc_len - вычисление длины замкнутого пути для тестов
- если не импорт, то перезаписывает graph.txt

src/brute_force.py - наивный алгоритм через рекурсию или перестановки

src/held_karp.py - точное решение через динамическое программирование

src/held_karp_cython.pyx - аналогично, но работает в >30 раз быстрее. Требует компиляции:
  - `cd src && python setup.py build_ext --inplace`

src/faster_christofides.py - приближенный и более быстрый алгоритм Кристофидеса
 (совершенное паросочетание минимального веса ищется жадным образом),
 опционально можно подключить/отключить 2-opt
 (https://en.wikipedia.org/wiki/2-opt)

src/faster_christofides_cython.pyx - аналогично

src/unit_tests.py - юнит тесты на адекватность результатов алгоритмов, верифицируют друг друга

benchmark_on_json.py - тест на реальных данных из all_sets.json


### Что можно успеть за секунду

![alt text](https://github.com/das67333/supervenn_tsp/blob/main/plots/x100_performance_precise.png)
![alt text](https://github.com/das67333/supervenn_tsp/blob/main/plots/x100_performance_approximate.png)


### Близость к оптимальному решению

![alt text](https://github.com/das67333/supervenn_tsp/blob/main/plots/x1000_heuristics_quality_20_50.png)
![alt text](https://github.com/das67333/supervenn_tsp/blob/main/plots/x1000_heuristics_quality_20_99.png)
