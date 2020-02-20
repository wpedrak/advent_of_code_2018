from Point import Point
from collections import defaultdict


def get_lines():
    file = open("input.txt", "r")
    lines = [line.rstrip('\n') for line in file]
    return lines


def is_on_edge(size, point):
    return point.x == 0 or point.y == 0 or point.x == size-1 or point.y == size-1


def get_closest_location(coordinates, point):
    dists = [Point.manhattan_distance(coord, point) for coord in coordinates]
    all_min = min(dists)
    many_winners = sum(map(
        lambda x: x == all_min,
        dists
    )) > 1

    if many_winners:
        return -1

    return dists.index(all_min)


coordinates = []
for_max = []


for line in get_lines():
    coords = [int(num) for num in line.split(',')]
    for_max += coords
    coordinates.append(Point(*coords))

above_max_coord = max(for_max) + 3

areas_size = defaultdict(lambda: 0)
on_edge = set()

for x in range(above_max_coord):
    for y in range(above_max_coord):
        this_point = Point(x, y)
        closest_location_id = get_closest_location(coordinates, this_point)

        if is_on_edge(above_max_coord, this_point):
            on_edge.add(closest_location_id)

        areas_size[closest_location_id] += 1


areas_not_on_edge = filter(
    lambda x: x[0] not in on_edge,
    areas_size.items()
)

result = max(areas_not_on_edge, key=lambda x: x[1])

print(result)
