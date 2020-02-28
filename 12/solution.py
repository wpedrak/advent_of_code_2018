class TwoWayArray:
    SIZE = 200

    def __init__(self, creator):
        self.creator = creator
        self.negative = [creator() for _ in range(TwoWayArray.SIZE)]
        self.nonNegative = [creator() for _ in range(TwoWayArray.SIZE)]

    def __getitem__(self, idx):
        if idx < 0:
            return self.negative[abs(idx)]

        return self.nonNegative[idx]

    def __setitem__(self, idx, value):
        if idx < 0:
            self.negative[abs(idx)] = value
            return

        self.nonNegative[idx] = value


class Rule:
    def __init__(self, pattern, target):
        self.pattern = pattern
        self.target = target

    def fits(self, indexable, index):
        pattern = ''.join([indexable[index + offset]
                           for offset in range(-2, 2 + 1)])
        return self.pattern == pattern

    def get_target(self):
        return self.target


def get_lines():
    file = open("input.txt", "r")
    lines = [line.rstrip('\n') for line in file]
    return lines


def parse_rule(line):
    splited = line.split()
    pattern = splited[0]
    target = splited[2]

    return Rule(pattern, target)


def match(rules, indexable, index):
    for rule in rules:
        if rule.fits(indexable, index):
            return rule.target

    # print('missmatch')
    return '.'


init_state = '##.#...#.#.#....###.#.#....##.#...##.##.###..#.##.###..####.#..##..#.##..#.......####.#.#..#....##.#'
NUMBER_OF_GENERATIONS = 20

rules = [parse_rule(line) for line in get_lines()]

this_generation = TwoWayArray(lambda: '.')
next_generation = TwoWayArray(lambda: '.')

for idx, state in enumerate(init_state):
    this_generation[idx] = state

for generation in range(NUMBER_OF_GENERATIONS):
    for position in range(-TwoWayArray.SIZE + 1 + 2, TwoWayArray.SIZE - 2):
        target = match(rules, this_generation, position)
        next_generation[position] = target

    this_generation = next_generation
    next_generation = TwoWayArray(lambda: '.')

result = 0

for position in range(-TwoWayArray.SIZE + 1, TwoWayArray.SIZE):
    if this_generation[position] == '#':
        result += position

print(result)
