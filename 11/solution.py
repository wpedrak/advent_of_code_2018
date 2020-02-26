GRID_SERIAL_NUMBER = 9221
BOARD_SIZE = 300


def power_level(x, y):
    rack_id = x + 10
    start_level = rack_id * y
    increased_power = start_level + GRID_SERIAL_NUMBER
    to_hunreds = increased_power * rack_id
    hundreds_digit = (to_hunreds % 1000) // 100
    return hundreds_digit - 5

def square_power_level(top_left_x, top_left_y):
    power = 0
    for x in range(top_left_x, top_left_x + 3):
        for y in range(top_left_y, top_left_y + 3):
            power += power_level(x, y)

    return power


candidates = [[x, y] for x in range(1, BOARD_SIZE - 3 + 1) for y in range(1, BOARD_SIZE - 3 + 1)]
results = list(map(
    lambda l: square_power_level(*l),
    candidates
))

max_power = max(results)
arg_max_idx = results.index(max_power)
print(max_power)
print(candidates[arg_max_idx])