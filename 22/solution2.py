from collections import defaultdict, deque
import heapq

DEPTH = 4080
TARGET = (14, 785)
X_MULTIPLIER = 16807
Y_MULTIPLIER = 48271
MOD = 20183
ROCKY = 0
WET = 1
NARROW = 2

TORCH = 'TORCH'
CLIMBING_GEAR = 'CLIMBING_GEAR'
NEITHER = 'NEITHER'


def erosion_level(geologic_index):
    return (geologic_index + DEPTH) % MOD


def map_type(cave):
    return [[c % 3 for c in row] for row in cave]


def get_cave_map(x_size, y_size):
    cave = [['.'] * (x_size+1) for _ in range(y_size + 1)]

    for x in range(1, x_size+1):
        cave[0][x] = erosion_level(x * X_MULTIPLIER)

    for y in range(1, y_size+1):
        cave[y][0] = erosion_level(y * Y_MULTIPLIER)

    cave[0][0] = 0
    cave[TARGET[1]][TARGET[0]] = 0

    for y in range(1, y_size+1):
        for x in range(1, x_size+1):
            if (x, y) == TARGET:
                continue
            geological_index = cave[y-1][x] * cave[y][x-1]
            cave[y][x] = erosion_level(geological_index)

    return map_type(cave)


def heuristic(point):
    x, y, _ = point
    return abs(x - TARGET[0]) + abs(y - TARGET[1])


def allowed_tools(region_type):
    return {
        ROCKY: [CLIMBING_GEAR, TORCH],
        WET: [CLIMBING_GEAR, NEITHER],
        NARROW: [TORCH, NEITHER]
    }[region_type]


def second_tool(region_type, tool):
    allowed = set(allowed_tools(region_type))
    allowed.remove(tool)
    return list(allowed)[0]


def get_neighbours(cave, state):
    x, y, tool = state
    potential_geographic_neighbours = [
        (x+1, y, tool),
        (x-1, y, tool),
        (x, y+1, tool),
        (x, y-1, tool)
    ]

    geographic_neighbours = list(filter(
        lambda s:
        s[2] in allowed_tools(cave[s[1]][s[0]]) and s[0] >= 0 and s[1] >= 0,
        potential_geographic_neighbours
    ))

    return geographic_neighbours + [(x, y, second_tool(cave[y][x], tool))]


def distance(state1, state2):
    x1, y1, tool1 = state1
    x2, y2, tool2 = state2

    if tool1 != tool2:
        return 7

    return 1


def shortest_path(cave, start, target):
    start_state = (start[0], start[1], TORCH)
    target_state = (target[0], target[1], TORCH)

    g_score = defaultdict(lambda: float('inf'))
    g_score[start_state] = 0

    f_score = defaultdict(lambda: float('inf'))
    f_score[start_state] = heuristic(start_state)

    open_set = [(f_score[start], start_state)]

    visited = set()

    while open_set:
        dist, current = heapq.heappop(open_set)

        if current in visited:
            continue

        if current == target_state:
            return dist

        for neighbour in get_neighbours(cave, current):
            tentative_g_score = g_score[current] + distance(current, neighbour)
            if tentative_g_score < g_score[neighbour]:
                g_score[neighbour] = tentative_g_score
                f_score[neighbour] = g_score[neighbour] + heuristic(neighbour)
                heapq.heappush(open_set, (f_score[neighbour], neighbour))

    raise Exception('Target not reached')

print('Calculating cave map...', end='')
cave = get_cave_map(TARGET[0] * 14, TARGET[1] * 14)
print('Done!')
print('Calculating shortest path...', end='')
result = shortest_path(cave, (0, 0), TARGET)
print('Done!')

print(result)
