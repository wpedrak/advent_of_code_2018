class Unit:
    ELF = 'E'
    GOBLIN = 'G'

    def __init__(self, x, y, fraction, battle_map):
        self.x = x
        self.y = y
        self.fraction = fraction
        self.battle_map = battle_map

        self.hp = 200
        self.attack_power = 3
        self.is_dead = False

    def __lt__(self, unit):
        # reading order
        return (self.y, self.x) < (unit.y, unit.x)

    def opponent(self):
        opp = {
            Unit.ELF: Unit.GOBLIN,
            Unit.GOBLIN: Unit.ELF
        }
        return opp[self.fraction]

    def move(self):
        target, distance = self.find_target()
        if not target:
            return

        if distance == 0:
            return

        direction = self.find_direction(target)

        self.perform_move(direction)

    def find_target(self):
        visited = set()
        to_visit = [(self.x, self.y)]
        dist = 0

        while to_visit:
            targets = list(filter(
                lambda p: self.battle_map.is_near(p, self.opponent()),
                to_visit
            ))

            if targets:
                return self.reading_order(targets), dist

            visited |= set(to_visit)
            to_visit = [
                self.battle_map.get_neighbours(p)
                for p in to_visit
                if p not in visited
            ]
            dist += 1

    def reading_order(self, points):
        return min(points, key=lambda p: (p[1], p[0]))

    def attack(self):
        pass

    def __repr__(self):
        return f'({self.x}, {self.y}, {self.fraction})'


class Board:
    def __init__(self, battle_map):
        self.battle_map = battle_map
        self.round_number = 0
        units = []

        for y, row in enumerate(battle_map):
            for x, item in enumerate(row):
                if item not in [Unit.ELF, Unit.GOBLIN]:
                    continue

                unit = Unit(x, y, item, battle_map)
                units.append(unit)

        self.units = units

    def get_round_number(self):
        return self.round_number

    def hp_sum(self):
        return sum([u.hp for u in self.units])

    def fight_finished(self):
        fractions_of_alive = [u.fraction for u in self.units if not u.is_dead]
        return len(set(fractions_of_alive)) == 1

    def get_neighbours(self, point):
        x, y = point
        potential_neighbours = [
            (x - 1, y),
            (x + 1, y),
            (x, y - 1),
            (x, y + 1)
        ]

        return [p for p in potential_neighbours if self.battle_map[y][x] == '.']

    def is_near(self, point, item):
        neighbours = self.get_neighbours(point)
        return any([
            self.battle_map[n[1]][n[0]] == item
            for n in neighbours
        ])

    def tick(self):
        units_in_order = list(sorted(self.units))

        for unit in units_in_order:
            unit.move()
            unit.attack()

    def __str__(self):
        return '\n'.join([
            ''.join(row) for row in self.battle_map
        ])

    def display(self):
        print(str(self))
        print('')


def get_lines(test_number=0):
    filename = f'test{test_number}' if test_number else 'input'
    file = open(f"{filename}.txt", "r")
    lines = [line.rstrip('\n') for line in file]
    return lines


def solve(test_number=0):
    lines = get_lines(test_number=test_number)
    original_map = [list(line) for line in lines]
    board = Board(original_map)

    board.display()

    # while not board.fight_finished():
    for _ in range(1):
        board.tick()
        board.display()

    round_number = board.get_round_number()
    hp_sum = board.hp_sum()

    return round_number * hp_sum


if True:
    # TESTS_NUM = 6
    TESTS_NUM = 1
    test_results = [solve(test_number=i) for i in range(1, TESTS_NUM + 1)]
    expected_values = [
        27730,
        36334,
        39514,
        27755,
        28944,
        18740
    ]

    assertions = list(map(
        lambda x: (x[0] == x[1], x[0], x[1]),
        zip(test_results, expected_values)
    ))

    print(assertions)
