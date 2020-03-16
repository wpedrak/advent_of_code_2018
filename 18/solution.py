from collections import Counter, defaultdict

GROUND = '.'
TREE = '|'
LUMBERYARD = '#'
FAKE = '+'
TIME = 10


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


def after_time(board, time, v=False):
    if v:
        print_board(board)

    size = len(board)
    for _ in range(time):
        after_epoch = get_empty_board(len(board))
        for y in range(1, size - 1):
            for x in range(1, size - 1):
                item = apply_rule(board, x, y)
                after_epoch[y][x] = item

        board = after_epoch
        if v:
            print_board(board)

    return board

def count_resource(board, resource):
    return Counter([item for row in board for item in row])[resource]

def get_resource_value(board):
    tree_count = count_resource(board, TREE)
    lumberyard_count = count_resource(board, LUMBERYARD)

    return tree_count * lumberyard_count


board = get_board()
board_after_time = after_time(board, TIME)
result = get_resource_value(board_after_time)

print(result)
