## Файлы

main.ipynb - пример использования supervenn

gen_graph.py
- gen_graph - создание графов в виде списков смежности
- calc_len - вычисление длины замкнутого пути для тестов
- если не импорт, то перезаписывает graph.txt

brute_force.py - наивный алгоритм через рекурсию или перестановки

held_karp.py - точное решение через динамическое программирование

faster_christofides.py - приближенный и более быстрый алгоритм Кристофидеса
 (совершенное паросочетание минимального веса ищется жадным образом) 


### Что можно успеть за секунду

brute_force_permutative => n=10

brute_force_recursive => n=10

held_karp => n=16

faster_christofides => n=2000

faster_christofides + 2-opt => n=600
