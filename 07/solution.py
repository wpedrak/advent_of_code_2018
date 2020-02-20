from re import search
from collections import defaultdict


def parse_instruction(instruction):
    search_result = search(
        r'Step ([A-Z]) must be finished before step ([A-Z]) can begin.',
        instruction
    )

    return [search_result.group(i) for i in range(1, 3)]


def get_lines():
    file = open("input.txt", "r")
    lines = [line.rstrip('\n') for line in file]
    return lines


lines = get_lines()
edges = defaultdict(lambda: [])
in_deg = defaultdict(lambda: 0)
vertices = set()

for line in lines:
    v_from, v_to = parse_instruction(line)
    vertices.add(v_from)
    vertices.add(v_to)
    edges[v_from].append(v_to)
    in_deg[v_to] += 1

result = []

while vertices:
    all_possible = filter(
        lambda x: in_deg[x] == 0,
        vertices
    )
    next_vertex = min(all_possible)
    result.append(next_vertex)
    vertices.remove(next_vertex)

    for neighbour in edges[next_vertex]:
        in_deg[neighbour] -= 1


print(''.join(result))
