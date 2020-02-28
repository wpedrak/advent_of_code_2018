class TwoWayArray:
    SIZE = 2000

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

    def to_list(self):
        negative_part = list(reversed(self.negative[1:]))

        return negative_part + self.nonNegative[:]


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

    return '.'


def pos_sum(two_way_array):
    result = 0

    for position in range(-TwoWayArray.SIZE + 1, TwoWayArray.SIZE):
        if two_way_array[position] == '#':
            result += position

    return result


init_state = '##.#...#.#.#....###.#.#....##.#...##.##.###..#.##.###..####.#..##..#.##..#.......####.#.#..#....##.#'
NUMBER_OF_GENERATIONS = 50000000000

rules = [parse_rule(line) for line in get_lines()]

this_generation = TwoWayArray(lambda: '.')
next_generation = TwoWayArray(lambda: '.')

for idx, state in enumerate(init_state):
    this_generation[idx] = state

previous_score = pos_sum(this_generation)

for generation in range(NUMBER_OF_GENERATIONS):
    for position in range(-TwoWayArray.SIZE + 1 + 2, TwoWayArray.SIZE - 2):
        target = match(rules, this_generation, position)
        next_generation[position] = target

    this_generation = next_generation
    next_generation = TwoWayArray(lambda: '.')

    score = pos_sum(this_generation)

    if score - previous_score == 50: # 50 pattern observed previously
        print(generation, score, previous_score)
        # printed: 89 5195 5145 and then print on every generation
        # so assume result: (NUMBER_OF_GENERATIONS - 90) * 50 + 5195 = 2500000000695

    previous_score = score
