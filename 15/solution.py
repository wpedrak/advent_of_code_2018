from collections import deque


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
        self.dead = False

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
        print(f'moving ({self.x}, {self.y})')

        if not self.battle_map.free_spot(self.opponent()):
            print('No free spots, skipping...')
            return

        target, distance = self.find_target()

        print(f'target is {target} and dist {distance}')

        if not target:
            return

        if distance == 0:
            return

        direction = self.find_direction(target)

        print(f'will go to {direction}')

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
                new_point
                for point in to_visit
                for new_point in self.battle_map.get_neighbours(point)
                if new_point not in visited
            ]

            dist += 1

        return None, 0

    def find_direction(self, target):
        self_point = (self.x, self.y)
        neighbours = self.battle_map.get_neighbours(self_point)

        if not neighbours:
            return self_point

        distances = [self.battle_map.distance(n, target) for n in neighbours]
        min_dist = min(distances)

        closest_points = [point for dist, point in zip(
            distances, neighbours) if dist == min_dist]

        return self.reading_order(closest_points)

    def perform_move(self, direction):
        x, y = direction
        board = self.battle_map.battle_map
        board[self.y][self.x] = '.'
        board[y][x] = self.fraction
        self.x = x
        self.y = y

    def reading_order(self, points):
        return min(points, key=lambda p: (p[1], p[0]))

    def attack(self):
        self_point = (self.x, self.y)
        enemy_points_nearby = self.battle_map.get_neighbours(
            self_point, allowed_chars=[self.opponent()])

        if not enemy_points_nearby:
            return

        enemies_hp = [self.battle_map.get_unit(
            p).hp for p in enemy_points_nearby]
        min_hp = min(enemies_hp)

        weakest_enemies_points = [enemy_point for hp, enemy_point in zip(
            enemies_hp, enemy_points_nearby) if hp == min_hp]

        selected_enemy_point = self.reading_order(weakest_enemies_points)

        selected_enemy = self.battle_map.get_unit(selected_enemy_point)

        selected_enemy.get_hit(self.attack_power)

    def get_hit(self, attack_power):
        self.hp -= attack_power

        if self.hp <= 0:
            self.die()

    def die(self):
        self.dead = True
        board = self.battle_map.battle_map
        board[self.y][self.x] = '.'

    def is_dead(self):
        return self.dead

    def is_alive(self):
        return not self.is_dead()

    def __repr__(self):
        return f'({self.x}, {self.y}, {self.fraction}, {self.hp})'


class Board:
    def __init__(self, battle_map):
        self.battle_map = battle_map
        self.finished_rounds = 0
        units = []

        for y, row in enumerate(battle_map):
            for x, item in enumerate(row):
                if item not in [Unit.ELF, Unit.GOBLIN]:
                    continue

                unit = Unit(x, y, item, self)
                units.append(unit)

        self.units = units

    def get_finished_rounds(self):
        return self.finished_rounds

    def hp_sum(self):
        return sum([u.hp for u in self.units if not u.is_dead()])

    def fight_finished(self):
        fractions_of_alive = [
            u.fraction for u in self.units if not u.is_dead()]
        return len(set(fractions_of_alive)) == 1

    def get_neighbours(self, point, allowed_chars=['.']):
        x, y = point
        potential_neighbours = [
            (x - 1, y),
            (x + 1, y),
            (x, y - 1),
            (x, y + 1)
        ]

        return [p for p in potential_neighbours if self.battle_map[p[1]][p[0]] in allowed_chars]

    def is_near(self, point, item):
        neighbours = self.get_neighbours(point, allowed_chars=['E', 'G'])

        return any([
            self.battle_map[n[1]][n[0]] == item
            for n in neighbours
        ])

    def distance(self, source, target):
        to_visit = deque([source, 'UP'])
        visited = set()
        dist = 0

        while len(to_visit) > 1:
            point = to_visit.popleft()

            if point == 'UP':
                dist += 1
                to_visit.append('UP')
                continue

            if point in visited:
                continue

            visited.add(point)

            if point == target:
                return dist

            to_visit += [p for p in self.get_neighbours(
                point) if p not in visited]

        return float('inf')

    def get_unit(self, point):
        matching_units = list(filter(
            lambda u: u.x == point[0] and u.y == point[1] and not u.is_dead(),
            self.units
        ))

        if len(matching_units) > 1:
            raise Exception(f'Ambigious unit on point {point}')

        if len(matching_units) == 0:
            raise Exception(f'No units on point {point}')

        return matching_units[0]

    def free_spot(self, fraction):
        all_from_fraction = list(filter(
            lambda u: u.fraction == fraction and u.is_alive(),
            self.units
        ))

        for unit in all_from_fraction:
            unit_point = (unit.x, unit.y)
            if self.get_neighbours(unit_point):
                return True

        return False

    def tick(self):
        units_in_order = list(sorted(self.units))

        for unit in units_in_order:
            if unit.is_dead():
                continue
            if self.fight_finished():
                return
            unit.move()
            unit.attack()

        self.finished_rounds += 1

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

    while not board.fight_finished():
        # for _ in range(2):
        print(board.get_finished_rounds())
        board.tick()
        board.display()
        print(board.units)

    round_number = board.get_finished_rounds()
    # print('ala')
    hp_sum = board.hp_sum()
    print(round_number, hp_sum)
    # print('kot')
    return round_number * hp_sum


test = False

if not test:
    result = solve()
    print(result)
else:
    TESTS_NUM = 6
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
