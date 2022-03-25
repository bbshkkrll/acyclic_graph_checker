import queue


def get_graph(filename):
    graph = {}
    with open(filename, 'r') as f:
        size = int(f.readline())
        for i in range(1, size + 1):
            edges = list(map(int, f.readline().split()))
            graph[i] = set()
            for j in range(len(edges)):
                if edges[j]:
                    graph[i].add(j + 1)
            if len(graph[i]) == 0:
                del graph[i]

    return graph


def is_graph_acyclic(graph):
    _queue = queue.Queue()
    visited = set()
    steps = [-1] * len(graph)

    start = 1
    _queue.put(start)
    steps[start - 1] = -1

    while not _queue.empty():
        current = _queue.get()

        if current in visited:
            return get_cycle_of_graph(steps, current)

        for node in graph[current]:
            if node not in visited:
                _queue.put(node)
                if steps[node - 1] != -1:
                    steps[node - 1] = ((steps[node - 1], current))
                    return get_cycle_of_graph(steps, node)
                else:
                    steps[node - 1] = current

            visited.add(current)

    return 'A'


def get_cycle_of_graph(steps, node):
    first_part = {node}
    current = steps[node - 1][0]
    while current != -1:
        first_part.add(current)
        current = steps[current - 1]

    second_part = set()
    current = steps[node - 1][1]

    first_same_node = True  # Вершина в которой начинается цикл
    start_of_cycle = -1

    while current != -1:
        if current in first_part and first_same_node:
            first_same_node = False
            start_of_cycle = current
            continue
        second_part.add(current)
        current = steps[current - 1]

    cycle = first_part ^ second_part
    cycle.add(start_of_cycle)

    return f'N {sorted(cycle)}'.replace(',', '').replace('[', '').replace(']','')


def write_result(result):
    with open('out.txt', 'w') as f:
        f.write(result)
        f.close()


if __name__ == '__main__':
    graph = get_graph('in.txt')

    write_result(is_graph_acyclic(graph))
