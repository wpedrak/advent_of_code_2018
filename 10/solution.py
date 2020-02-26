from re import search


class Point:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def tick(self):
        self.x += self.vx
        self.y += self.vy

    def __str__(self):
        return f'({self.x}, {self.y}, {self.vx}, {self.vy})'

    def __repr__(self):
        return str(self)


class Sky:
    def __init__(self):
        self.points = []

    def add_point(self, point):
        self.points.append(point)

    def tick(self):
        for point in self.points:
            point.tick()

    def get_min_max(self):
        max_x = max(self.points, key=lambda p: p.x).x
        min_x = min(self.points, key=lambda p: p.x).x
        max_y = max(self.points, key=lambda p: p.y).y
        min_y = min(self.points, key=lambda p: p.y).y

        return min_x, max_x, min_y, max_y

    def draw(self):
        min_x, max_x, min_y, max_y = self.get_min_max()
        x_shift = - min_x
        y_shift = - min_y

        delta_x = max_x - min_x
        delta_y = max_y - min_y

        canvas = [[' '] * (delta_x+1) for _ in range(delta_y+1)]


        for point in self.points:

            canvas[point.y + y_shift][point.x + x_shift] = '#'

        drawing = '\n'.join([''.join(row) for row in canvas]) + '\n'

        print(drawing)

    def is_close(self):
        VERTICAL_DIST = 10
        HORIZONTAL_DIST = 100

        min_x, max_x, min_y, max_y = self.get_min_max()
        
        return max_y - min_y < VERTICAL_DIST and max_x - min_x < HORIZONTAL_DIST


def get_lines():
    file = open("input.txt", "r")
    lines = [line.rstrip('\n') for line in file]
    return lines


def parse_point(line):
    line = line.replace(' ', '')
    search_result = search(
        r'position=<([-]?[0-9]+),([-]?[0-9]+)>velocity=<([-]?[0-9]+),([-]?[0-9]+)>', line)

    point_params = [int(search_result.group(i)) for i in range(1, 5)]

    return Point(*point_params)


lines = get_lines()

sky = Sky()

for line in lines:
    point = parse_point(line)
    sky.add_point(point)


while True:
    if sky.is_close():
        sky.draw()

    sky.tick()
