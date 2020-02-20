from re import search
from itertools import chain


def parse_claim(claim):
    search_result = search(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)', claim)

    return [int(search_result.group(i)) for i in range(1, 6)]


def flatten(lst):
    return list(chain(*lst))


def mark_on_fabric(fabric, x, y, width, height):
    for y_delta in range(height):
        for x_delta in range(width):
            fabric[y+y_delta][x+x_delta] += 1


file = open("input.txt", "r")
lines = [line.rstrip('\n') for line in file]

fabric_edge_size = 1000
fabric = [[0] * fabric_edge_size for _ in range(fabric_edge_size)]

for claim in lines:
    _, from_left, from_top, width, height = parse_claim(claim)
    mark_on_fabric(fabric, from_left, from_top, width, height)

result = sum(map(
    lambda x: x > 1,
    flatten(fabric)
))

print(result)
