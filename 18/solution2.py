from collections import Counter, defaultdict

GROUND = '.'
TREE = '|'
LUMBERYARD = '#'
FAKE = '+'
TIME = 1000000000


def get_lines():
    filename = 'input'
    file = open(f"{filename}.txt", "r")
    lines = [line.rstrip('\n') for line in file]
    return lines


def get_board():
    lines = get_lines()
    size = len(lines)
    board = [[FAKE] * (size + 2)]
    board += [[FAKE] + list(row) + [FAKE] for row in lines]
    board += [[FAKE] * (size + 2)]
    return board


def print_board(board):
    img = '\n'.join([''.join(row) for row in board])
    print(img)
    print('')


def get_empty_board(size):
    return [[FAKE] * size for _ in range(size)]


def scan_adjacent_acres(board, item_x, item_y):
    neighbours = [
        board[y][x]
        for x in range(item_x-1, item_x+2)
        for y in range(item_y-1, item_y+2)
        if (x, y) != (item_x, item_y)
    ]

    return defaultdict(lambda: 0, Counter(neighbours))


def ground_rule(scan):
    return TREE if scan[TREE] >= 3 else GROUND


def tree_rule(scan):
    return LUMBERYARD if scan[LUMBERYARD] >= 3 else TREE


def lumberyard_rule(scan):
    return LUMBERYARD if scan[TREE] and scan[LUMBERYARD] else GROUND


def apply_rule(board, x, y):
    item = board[y][x]
    scan = scan_adjacent_acres(board, x, y)

    if item == GROUND:
        return ground_rule(scan)
    if item == TREE:
        return tree_rule(scan)
    if item == LUMBERYARD:
        return lumberyard_rule(scan)

    raise Exception(f'Unexpected field value: {item} for ({x}, {y})')


def detect_loop(board, time):
    visited = set()
    visited_in_order = []
    results = []
    size = len(board)
    for time in range(time):
        after_epoch = get_empty_board(len(board))
        for y in range(1, size - 1):
            for x in range(1, size - 1):
                item = apply_rule(board, x, y)
                after_epoch[y][x] = item

        board = after_epoch
        tupled_board = tuple([tuple(row) for row in board])
        if tupled_board in visited:
            idx = visited_in_order.index(tupled_board)
            return idx, time - idx, results

        results.append(get_resource_value(board))
        visited.add(tupled_board)
        visited_in_order.append(tupled_board)

    raise Exception('No loop found')


def count_resource(board, resource):
    return Counter([item for row in board for item in row])[resource]


def get_resource_value(board):
    tree_count = count_resource(board, TREE)
    lumberyard_count = count_resource(board, LUMBERYARD)

    return tree_count * lumberyard_count


board = get_board()
prefix_size, loop_size, results = detect_loop(board, TIME)
time_in_loop = TIME - prefix_size - 1
item_in_loop = time_in_loop % loop_size
result = results[prefix_size + item_in_loop]

print(result)
