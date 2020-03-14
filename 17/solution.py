WATER_SOURCE = (500, 0)
EMPTY = '.'
CLAY = '#'
WATER = 'o'


class Rectangle():
    def __init__(self, top_left, bot_right):
        self.top_left = top_left
        self.bot_right = bot_right

    def __str__(self):
        return f'From {self.top_left} to {self.bot_right}'

    def __repr__(self):
        return str(self)


def get_lines():
    filename = 'input'
    file = open(f"{filename}.txt", "r")
    lines = [line.rstrip('\n') for line in file]
    return lines


def parse_vertical(line):
    x_part, y_part = line.split(', ')
    x = int(x_part[2:])
    y_range = y_part[2:]
    top_y, bot_y = [int(y) for y in y_range.split('..')]

    return Rectangle((x, top_y), (x, bot_y))


def parse_horizontal(line):
    y_part, x_part = line.split(', ')
    y = int(y_part[2:])
    x_range = x_part[2:]
    left_x, right_x = [int(x) for x in x_range.split('..')]

    return Rectangle((left_x, y), (right_x, y))


def parse_line(line):
    first_char = line[0]

    if first_char == 'x':
        return parse_vertical(line)

    if first_char == 'y':
        return parse_horizontal(line)

    raise Exception(f'unknown first char: {first_char}')


def parse(lines):
    return [parse_line(line) for line in lines]


def put_rectangle_on_board(board, rectangle):
    for y in range(rectangle.top_left[1], rectangle.bot_right[1] + 1):
        for x in range(rectangle.top_left[0], rectangle.bot_right[0] + 1):
            board[y][x] = CLAY


def draw_board(board, left, right, top, bot):
    img = '\n'.join([''.join(row[left:right+1]) for row in board[top:bot+1]])
    print(img)


def water_in_range(board, min_x, max_x, min_y, max_y):
    count = 0

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            count += board[y][x] == WATER

    return count


def is_clay(board, point):
    x, y = point

    return board[y][x] == CLAY


def put_water(board, point):
    x, y = point

    board[y][x] = WATER


def go_down(board, source, max_y):
    print('go_down', source)
    x, y = source
    if y > max_y:
        return None

    if is_water(board, (x, y+1)):
        return None

    if is_clay(board, source):
        return (x, y-1)

    put_water(board, source)
    return go_down(board, (x, y+1), max_y)


def is_source(board, point):
    x, y = point
    return board[y+1][x] == EMPTY


def is_water(board, point):
    x, y = point

    return board[y][x] == WATER


def go_left(board, point, min_x):
    x, y = point

    if x < min_x-1:
        shift = 2
        draw_board(board, x-shift, x+shift, y-shift, y+shift)
        raise Exception(f'go_left is too left: ({x}, {y})')

    if is_clay(board, point):
        return []

    put_water(board, point)

    if is_source(board, point):
        return [point]

    return go_left(board, (x-1, y), min_x)


def go_right(board, point, max_x):
    x, y = point

    if x > max_x+1:
        shift = 100
        to_left = 300
        draw_board(board, x-shift-to_left, x+shift-to_left, y-5, y+50)
        raise Exception(f'go_right is too right: ({x}, {y})')

    if is_clay(board, point):
        return []

    put_water(board, point)

    if is_source(board, point):
        return [point]

    return go_right(board, (x+1, y), max_x)


def go_up(board, point, min_x, max_x, min_y):
    x, y = point

    if y < y-1:
        raise Exception(f'go_up is too high: ({x}, {y})')

    left_source = go_left(board, (x, y), min_x)
    right_source = go_right(board, (x, y), max_x)
    sources = left_source + right_source

    if sources:
        return sources

    return go_up(board, (x, y-1), min_x, max_x, min_y)


def fill_with_water(board, source, min_x, max_x, min_y, max_y):
    last_point = go_down(board, source, max_y)

    if not last_point:
        # print('no last')
        return

    # print(last_point)

    new_sources = go_up(board, last_point, min_x, max_x, min_y)

    for new_source in new_sources:
        fill_with_water(board, new_source, min_x, max_x, min_y, max_y)


def solve(rectangles, source):
    min_x = min(rectangles, key=lambda r: r.top_left[0]).top_left[0]
    max_x = max(rectangles, key=lambda r: r.bot_right[0]).bot_right[0]
    min_y = min(rectangles, key=lambda r: r.top_left[1]).top_left[1]
    max_y = max(rectangles, key=lambda r: r.bot_right[1]).bot_right[1]

    board = [['.'] * (max_x + 13) for _ in range(max_y + 13)]

    for rectangle in rectangles:
        put_rectangle_on_board(board, rectangle)

    draw_board(board, min_x, max_x, min_y, max_y)
    print('')

    fill_with_water(board, source, min_x, max_x, min_y, max_y)

    # draw_board(board, min_x, max_x, min_y, max_y)
    draw_board(board, min_x, max_x, min_y, max_y)

    return water_in_range(board, min_x, max_x, min_y, max_y)


lines = get_lines()
rectangles = parse(lines)
# print(rectangles)
result = solve(rectangles, WATER_SOURCE)

print(result)
