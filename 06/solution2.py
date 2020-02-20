from Point import Point
from collections import defaultdict

SAFE_DIST = 10000


def get_lines():
    file = open("input.txt", "r")
    lines = [line.rstrip('\n') for line in file]
    return lines


def get_dists_sum(coordinates, point):
    dists = [Point.manhattan_distance(coord, point) for coord in coordinates]
    return sum(dists)

coordinates = []
for_max = []


for line in get_lines():
    coords = [int(num) for num in line.split(',')]
    for_max += coords
    coordinates.append(Point(*coords))

safe_margin = int(SAFE_DIST / len(coordinates))
max_coord = max(for_max)
result = 0

for x in range(-safe_margin, max_coord + safe_margin):
    for y in range(-safe_margin, max_coord + safe_margin):
        this_point = Point(x, y)
        dists_sum = get_dists_sum(coordinates, this_point)
        result += dists_sum < SAFE_DIST

print(result)
