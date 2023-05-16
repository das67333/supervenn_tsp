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

src/faster_christofides.pyx - аналогично

src/unit_tests.py - юнит тесты на адекватность результатов алгоритмов, верифицируют друг друга


### Что можно успеть за секунду

![alt text](https://github.com/das67333/supervenn_tsp/blob/main/x100_precise.png)
![alt text](https://github.com/das67333/supervenn_tsp/blob/main/x100_approximate.png)
