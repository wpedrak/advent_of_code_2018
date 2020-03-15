import sys

WATER_SOURCE = (500, 0)
EMPTY = '.'
CLAY = '#'
WATER = 'o'

used_sources = set()


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
        for x in range(min_x-1, max_x + 2):
            count += board[y][x] == WATER

    return count


def is_in_board(field_type):
    def aux(board, point):
        x, y = point
        return board[y][x] == field_type

    return aux


is_clay = is_in_board(CLAY)
is_water = is_in_board(WATER)
is_empty = is_in_board(EMPTY)


def put_water(board, point):
    x, y = point
    previous_value = board[y][x]
    board[y][x] = WATER
    return previous_value != WATER


def go_down(board, source, max_y):
    x, y = source
    if y > max_y:
        return None

    if is_water(board, (x, y)) and is_empty(board, (x, y-1)):
        return None

    if is_used_source(source) and is_water(board, (x, y-1)):
        return None

    if is_clay(board, source) or is_water(board, (x, y)):
        return (x, y-1)

    put_water(board, source)

    return go_down(board, (x, y+1), max_y)


def is_left_source(board, point):
    x, y = point
    return board[y][x] in [EMPTY, WATER] and board[y+1][x] in [EMPTY, WATER] and board[y+1][x+1] in [CLAY] and board[y][x-1] in [EMPTY]


def should_stop_left_walk(board, point):
    return is_clay(board, point) or is_left_source(board, point)


def go_left(board, point, min_x):
    x, y = point
    changed_count = 0

    while not should_stop_left_walk(board, point):
        if point[0] < min_x-1:
            shift = 10
            draw_board(board, x-shift, x+shift, y-shift, y+shift)
            raise Exception(f'go_left is too left: ({x}, {y})')

        changed_count += put_water(board, point)
        point = (point[0]-1, y)

    return changed_count, point


def is_right_source(board, point):
    x, y = point
    return board[y][x] in [EMPTY, WATER] and board[y+1][x] in [EMPTY, WATER] and board[y+1][x-1] in [CLAY] and board[y][x+1] in [EMPTY]


def should_stop_right_walk(board, point):
    return is_clay(board, point) or is_right_source(board, point)


def go_right(board, point, max_x):
    x, y = point
    changed_count = 0

    while not should_stop_right_walk(board, point):
        if point[0] > max_x+1:
            shift = 10
            draw_board(board, x-shift, x+shift, y-shift, y+shift)
            raise Exception(f'go_right is too right: ({x}, {y})')

        changed_count += put_water(board, point)
        point = (point[0]+1, y)

    return changed_count, point


def is_source_below(board, point, min_x, max_x):
    x, y = point[0], point[1] + 1
    left_changes, left_point = go_left(board, (x-1, y), min_x)
    right_changes, right_point = go_right(board, (x+1, y), max_x)

    if left_changes + right_changes:
        shift = 10
        draw_board(board, x-shift, x+shift, y-shift, y+shift)
        raise Exception('it only check, it should not change anything')

    return is_left_source(board, left_point) or is_right_source(board, right_point)


def go_up(board, point, min_x, max_x, min_y):
    x, y = point

    put_water(board, point)

    if y < min_y-1:
        shift = 10
        draw_board(board, x-shift, x+shift, y-shift, y+shift)
        raise Exception(f'go_up is too high: ({x}, {y})')

    left_changes, left_point = go_left(board, (x-1, y), min_x)
    right_changes, right_point = go_right(board, (x+1, y), max_x)

    sources = []

    if is_left_source(board, left_point):
        sources.append(left_point)

    if is_right_source(board, right_point):
        sources.append(right_point)

    if sources:
        return sources

    return go_up(board, (x, y-1), min_x, max_x, min_y)


def is_used_source(source):
    return source in used_sources


def use_sources(sources):
    for source in sources:
        used_sources.add(source)


def fill_with_water(board, source, min_x, max_x, min_y, max_y):
    last_point = go_down(board, source, max_y)

    if not last_point:
        return

    x, y = last_point

    if is_water(board, (x, y+1)) and is_source_below(board, last_point, min_x, max_x):
        return

    potential_new_sources = go_up(board, last_point, min_x, max_x, min_y)
    new_sources = list(filter(
        lambda s: is_empty(board, s),
        potential_new_sources
    ))

    use_sources(new_sources)

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

    fill_with_water(board, source, min_x, max_x, min_y, max_y)

    # draw_board(board, min_x-2, max_x+2, min_y, max_y)
    return water_in_range(board, min_x, max_x, min_y, max_y)


lines = get_lines()
rectangles = parse(lines)
result = solve(rectangles, WATER_SOURCE)

print(result)