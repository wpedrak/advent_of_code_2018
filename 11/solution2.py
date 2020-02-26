GRID_SERIAL_NUMBER = 9221
BOARD_SIZE = 300


def power_level(x, y):
    rack_id = x + 10
    start_level = rack_id * y
    increased_power = start_level + GRID_SERIAL_NUMBER
    to_hunreds = increased_power * rack_id
    hundreds_digit = (to_hunreds % 1000) // 100
    return hundreds_digit - 5


def square_power_level(x, y, size, prefix_sum):
    return prefix_sum[y+size-1][x+size-1] + prefix_sum[y-1][x-1] - prefix_sum[y-1][x+size-1] - prefix_sum[y+size-1][x-1]


def solve_for_size(size, prefix_sum):
    print(f'checking_size {size}')

    candidates = [[x, y] for x in range(
        1, BOARD_SIZE - size + 2) for y in range(1, BOARD_SIZE - size + 2)]
    results = list(map(
        lambda l: square_power_level(l[0], l[1], size, prefix_sum),
        candidates
    ))

    max_power = max(results)
    arg_max_idx = results.index(max_power)
    arg_max = candidates[arg_max_idx]

    return max_power, size, arg_max


def square_prefix_sum(to_process):
    lst_2d = [row[:] for row in to_process]

    for y in range(1, len(lst_2d)):
        for x in range(1, len(lst_2d[0])):
            lst_2d[y][x] += lst_2d[y-1][x] + lst_2d[y][x-1] - lst_2d[y-1][x-1]

    return lst_2d


cell_power_level = [[0] + [power_level(x, y) for x in range(1, BOARD_SIZE + 1)]
                    for y in range(1, BOARD_SIZE + 1)]
cell_power_level = [[0] * (BOARD_SIZE + 1)] + cell_power_level

prefix_sum = square_prefix_sum(cell_power_level)

results_for_sizes = [solve_for_size(size, prefix_sum)
                     for size in range(1, BOARD_SIZE + 1)]

result = max(results_for_sizes)
print(result)
