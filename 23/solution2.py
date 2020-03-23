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



lines = get_lines()
nanobots = parse(lines)
CURRENT_BEST = 859

x_min, x_max = get_min_max(nanobots, lambda n: n.x)
y_min, y_max = get_min_max(nanobots, lambda n: n.y)
z_min, z_max = get_min_max(nanobots, lambda n: n.z)

# for grid_size in range(1, 100):
#     # grid_size = 3
#     print(grid_size)
#     points = make_grid(grid_size, x_min, x_max, y_min, y_max, z_min, z_max)
#     in_range = [check_point(nanobots, p) for p in points]
#     max_in_range = max(in_range)
#     max_idx = in_range.index(max_in_range)
#     max_point = points[max_idx]
#     print(max_in_range)
#     print(max_point)

nanobots2 = filter_useless(CURRENT_BEST, nanobots)
intersections = get_intersections(nanobots2)

print(min(intersections))
print(max(intersections))


# current best: 859
# upper bound: 972
# print(check_point(nanobots, Point(48365889, 45740560, 43704147)))
