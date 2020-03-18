DEPTH = 4080
TARGET = (14, 785)
X_MULTIPLIER = 16807
Y_MULTIPLIER = 48271
MOD = 20183


def erosion_level(geologic_index):
    return (geologic_index + DEPTH) % MOD


def risk_level(cave):
    return sum([c % 3 for row in cave for c in row])


cave = [['.'] * (TARGET[0]+1) for _ in range(TARGET[1] + 1)]

for x in range(1, TARGET[0]+1):
    cave[0][x] = erosion_level(x * X_MULTIPLIER)

for y in range(1, TARGET[1]+1):
    cave[y][0] = erosion_level(y * Y_MULTIPLIER)

for y in range(1, TARGET[1]+1):
    for x in range(1, TARGET[0]+1):
        geological_index = cave[y-1][x] * cave[y][x-1]
        cave[y][x] = erosion_level(geological_index)

cave[0][0] = 0
cave[TARGET[1]][TARGET[0]] = 0


result = risk_level(cave)
print(result)
