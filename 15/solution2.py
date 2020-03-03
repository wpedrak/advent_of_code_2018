from collections import deque


class Unit:
    ELF = 'E'
    GOBLIN = 'G'
    DEFAULT_ATTACK = 3

    def __init__(self, x, y, fraction, battle_map, attack_power):
        self.x = x
        self.y = y
        self.fraction = fraction
        self.battle_map = battle_map
        self.attack_power = attack_power

        self.hp = 200
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
        if not self.battle_map.is_free_spot(self.opponent()):
            return

        target, distance = self.find_target()

        if not target:
            return

        if distance == 0:
            return

        direction = self.find_direction(target)

        self.perform_move(direction)

    def find_target(self):
        self_point = (self.x, self.y)
        if self.battle_map.is_near(self_point, self.opponent()):
            return (self.x, self.y), 0

        targets = set(self.battle_map.get_free_spots(self.opponent()))
        reached_targets = []
        visited = set()
        to_visit = deque([(self.x, self.y), 'UP'])
        dist = 0

        while len(to_visit) > 1:
            point = to_visit.popleft()

            if point in visited:
                continue

            if point == 'UP':
                if reached_targets:
                    reached_target = self.reading_order(reached_targets)
                    return reached_target, dist

                dist += 1
                to_visit.append('UP')
                continue

            visited.add(point)

            if point in targets:
                reached_targets.append(point)

            to_visit += [
                p for p in self.battle_map.get_neighbours(point) if p not in visited
            ]

        if reached_targets:
            reached_target = self.reading_order(reached_targets)
            return reached_target, dist

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
        if self.fraction == Unit.ELF:
            raise Exception('Elf died!')

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
    def __init__(self, battle_map, elves_attack):
        self.battle_map = battle_map
        self.finished_rounds = 0
        units = []

        for y, row in enumerate(battle_map):
            for x, item in enumerate(row):
                if item not in [Unit.ELF, Unit.GOBLIN]:
                    continue

                attack = elves_attack if item == Unit.ELF else Unit.DEFAULT_ATTACK

                unit = Unit(x, y, item, self, attack)
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

    def get_free_spots(self, fraction):
        all_from_fraction = list(filter(
            lambda u: u.fraction == fraction and u.is_alive(),
            self.units
        ))

        free_spots = []

        for unit in all_from_fraction:
            unit_point = (unit.x, unit.y)
            free_spots += self.get_neighbours(unit_point)

        return free_spots

    def is_free_spot(self, fraction):
        return len(self.get_free_spots(fraction)) > 0

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


def solve(elves_attack, test_number=0):
    print(f'solving for attack {elves_attack}')
    lines = get_lines(test_number=test_number)
    original_map = [list(line) for line in lines]
    board = Board(original_map, elves_attack)

    try:
        while not board.fight_finished():
            board.tick()
    except Exception:
        return -1

    round_number = board.get_finished_rounds()
    hp_sum = board.hp_sum()
    return round_number * hp_sum


test = False

if not test:
    elves_attack = 4
    while elves_attack < 200 + 1:
        result = solve(elves_attack)
        if result > 0:
            break
        elves_attack += 1

    print(result)
else:
    attack_boost = [
        15,
        4,
        4,
        15,
        12,
        34
    ]
    test_results = [solve(attack_boost[i-1], test_number=i)
                    for i in range(1, 6 + 1)]
    expected_values = [
        4988,
        29064,
        31284,
        3478,
        6474,
        1140
    ]

    assertions = list(map(
        lambda x: (x[0] == x[1], x[0], x[1]),
        zip(test_results, expected_values)
    ))

    print(assertions)
