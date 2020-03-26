from collections import defaultdict
import itertools

def get_lines():
    filename = 'input'
    file = open(f"{filename}.txt", "r")
    lines = [line.rstrip('\n') for line in file]
    return lines


def parse_points(lines):
    return [parse_point(line) for line in lines]


def parse_point(line):
    return tuple(map(
        int,
        line.split(',')
    ))


def manhattan(p1, p2):
    return sum(map(
        lambda p: abs(p[0] - p[1]),
        zip(p1, p2)
    ))

def are_close(p1, p2):
    return manhattan(p1, p2) <= 3

def discover_constelation(root, edges):
    to_visit = [root]
    visited = set()

    while to_visit:
        current = to_visit.pop()

        if current in visited:
            continue

        visited.add(current)
        to_visit += [n for n in edges[current] if n not in visited]

    return visited


def solve(points):
    edges = defaultdict(lambda: [])

    for p1, p2 in itertools.combinations(points, 2):
        if not are_close(p1, p2):
            continue

        edges[p1].append(p2)
        edges[p2].append(p1)

    # for k, v in edges.items():
    #     print(k, v)

    global_to_visit = set(points)

    constelations_number = 0

    while global_to_visit:
        constelations_number += 1

        root_of_new_constelation = list(global_to_visit)[0]
        points_in_constelation = discover_constelation(root_of_new_constelation, edges)
        global_to_visit -= points_in_constelation

    return constelations_number

lines = get_lines()
points = parse_points(lines)
result = solve(points)
print(result)
