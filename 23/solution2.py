from collections import defaultdict
import numpy as np


def get_lines():
    filename = 'input'
    file = open(f"{filename}.txt", "r")
    lines = [line.rstrip('\n') for line in file]
    return lines


def parse_line(line):
    left_brace_idx = line.find('<')
    right_brace_idx = line.find('>')

    coordinates = line[left_brace_idx + 1:right_brace_idx]
    x, y, z = map(int, coordinates.split(','))

    r_idx = line.find('r')

    r = int(line[r_idx+2:])

    return Nanobot(x, y, z, r)


def parse(lines):
    return [parse_line(line) for line in lines]


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def dist(self, point):
        return abs(self.x - point.x) + abs(self.y - point.y) + abs(self.z - point.z)

    def __repr__(self):
        return f'({self.x}, {self.y}, {self.z})'


class Nanobot(Point):
    def __init__(self, x, y, z, r):
        super().__init__(x, y, z)
        self.r = r

    def have_in_range(self, point):
        return self.dist(point) <= self.r

    def intersects(self, nanobot):
        dist = self.dist(nanobot)
        return dist <= self.r + nanobot.r

    def freedom_after_intersection(self, nanobot):
        dist = self.dist(nanobot)
        return (self.r + nanobot.r) - dist

    def __repr__(self):
        return f'({self.x}, {self.y}, {self.z}) r={self.r}'


def check_point(nanobots, point):
    return sum([n.have_in_range(point) for n in nanobots])


def get_min_max(lst, getter):
    min_item = min(lst, key=getter)
    max_item = max(lst, key=getter)

    return getter(min_item), getter(max_item)


def make_grid(grid_size, x_min, x_max, y_min, y_max, z_min, z_max):
    x_step = (x_max - x_min) // (grid_size + 1)
    y_step = (y_max - y_min) // (grid_size + 1)
    z_step = (z_max - z_min) // (grid_size + 1)

    return [
        Point(
            x_min + x_step * x_nr,
            y_min + y_step * y_nr,
            z_min + z_step * z_nr
        )
        for x_nr in range(1, grid_size+1)
        for y_nr in range(1, grid_size+1)
        for z_nr in range(1, grid_size+1)
    ]


def filter_useless(threshold, nanobots):
    usefull_nanobots = []

    for n1 in nanobots:
        cnt = 0
        for n2 in nanobots:
            cnt += n1.intersects(n2)
        if cnt >= threshold:
            usefull_nanobots.append(n1)

    return usefull_nanobots


def get_intersections(nanobots):
    intersections = []
    for n1 in nanobots:
        cnt = 0
        for n2 in nanobots:
            cnt += n1.intersects(n2)
        intersections.append(cnt)

    return intersections


def intersection(nanobots, left_getter, right_getter):
    left = - float('inf')
    right = float('inf')

    for n in nanobots:
        bounds = [left_getter(n), right_getter(n)]
        current_min = min(bounds)
        current_max = max(bounds)
        left = max(left, current_min)
        right = min(right, current_max)

    return left, right


def mark(value, middle):
    return 'G' if value > middle else 'L'


lines = get_lines()
nanobots_from_input = parse(lines)
CURRENT_BEST = 859  # using grid search commented below
nanobots = filter_useless(CURRENT_BEST, nanobots_from_input)

# x_min, x_max = get_min_max(nanobots, lambda n: n.x)
# y_min, y_max = get_min_max(nanobots, lambda n: n.y)
# z_min, z_max = get_min_max(nanobots, lambda n: n.z)

# for grid_size in range(1, 20):
#     print(grid_size)
#     points = make_grid(grid_size, left_x, right_x, left_y, right_y, left_z, right_z)
#     in_range = [check_point(nanobots, p) for p in points]
#     max_in_range = max(in_range)
#     max_idx = in_range.index(max_in_range)
#     max_point = points[max_idx]
#     print(max_in_range)
#     print(max_point)

zero_freedom = set()
zero_freedom_points = set()

for n1 in nanobots:
    for n2 in nanobots:
        freedom = n1.freedom_after_intersection(n2)
        if not freedom and (n2, n1) not in zero_freedom:
            zero_freedom.add((n1, n2))
            zero_freedom_points.add(n1)
            zero_freedom_points.add(n2)


left_x, right_x = intersection(
    zero_freedom, lambda n: n[0].x, lambda n: n[1].x)
left_y, right_y = intersection(
    zero_freedom, lambda n: n[0].y, lambda n: n[1].y)
left_z, right_z = intersection(
    zero_freedom, lambda n: n[0].z, lambda n: n[1].z)

markers = defaultdict(lambda: [])

for zfp in zero_freedom_points:
    x_marker = mark(zfp.x, (right_x + left_x) // 2)
    y_marker = mark(zfp.y, (right_y + left_y) // 2)
    z_marker = mark(zfp.z, (right_z + left_z) // 2)
    marker = x_marker + y_marker + z_marker
    markers[marker].append(zfp)

lgg = markers['LGG'][0]
glg = markers['GLG'][0]
ggl = markers['GGL'][0]

equations = np.array([
    [-1, 1, 1],
    [1, -1, 1],
    [1, 1, -1]
])

results = np.array([
    - lgg.r - lgg.x + lgg.y + lgg.z,
    - glg.r + glg.x - glg.y + glg.z,
    - ggl.r + ggl.x + ggl.y - ggl.z
])


solution = [int(res) for res in np.linalg.solve(equations, results)]

# print(check_point(nanobots_from_input, Point(*solution)))
print(Point(*solution).dist(Point(0, 0, 0)))

