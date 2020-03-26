def get_lines(filename):
    file = open(f"{filename}.txt", "r")
    lines = [line.rstrip('\n') for line in file]
    return lines


def parse_groups(lines):
    return [parse_group(line) for line in lines]


def parse_group(line):
    standard, extras = separate(line)
    extra_powers = get_powers(extras)
    group = parse_standard_group(standard)

    for weakness in extra_powers['weak']:
        group.add_weakness(weakness)

    for immunity in extra_powers['immune']:
        group.add_immunity(immunity)

    return group


def separate(line):
    left_brace_idx = line.find('(')
    right_brace_idx = line.find(')')

    if left_brace_idx == -1:
        return line, ''

    return line[:left_brace_idx] + line[right_brace_idx+2:], line[left_brace_idx+1:right_brace_idx]


def get_powers(extras):
    powers = {
        'weak': [],
        'immune': []
    }
    # print(extras)
    if not extras:
        return powers

    for extra in extras.split(';'):
        extra_type, powers_enum = extra.split(' to ')
        powers[extra_type.strip()] = powers_enum.split(', ')

    return powers


def parse_standard_group(line):
    UNIT_NUMBER_POS = 0
    UNIT_HP_POS = 4
    ATTACK_POWER_POS = 12
    ATTACK_TYPE_POS = 13
    INITIATIVE_POS = 17

    words = line.split()
    units_number = int(words[UNIT_NUMBER_POS])
    unit_hp = int(words[UNIT_HP_POS])
    attack_power = int(words[ATTACK_POWER_POS])
    attack_type = words[ATTACK_TYPE_POS]
    initiative = int(words[INITIATIVE_POS])

    return Group(units_number, unit_hp, attack_power, attack_type, initiative)


class Group:
    def __init__(self, units_number, unit_hp, attack_power, attack_type, initiative):
        self.units_number = units_number
        self.unit_hp = unit_hp
        self.attack_power = attack_power
        self.attack_type = attack_type
        self.initiative = initiative
        self.weaknesses = []
        self.immunities = []

    def add_weakness(self, weakness):
        self.weaknesses.append(weakness)

    def add_immunity(self, immunity):
        self.immunities.append(immunity)

    def effective_power(self):
        return self.units_number * self.attack_power

    def damage_to(self, group):
        if self.attack_type in group.weaknesses:
            return self.effective_power() * 2

        if self.attack_type in group.immunities:
            return 0

        return self.effective_power()

    def get_hit(self, group):
        dmg = group.damage_to(self)

        units_died = min(dmg // self.unit_hp, self.units_number)

        self.units_number -= units_died
        assert self.units_number >= 0

    def __repr__(self):
        return f'(#units={self.units_number}, hp={self.unit_hp}, ap={self.attack_power}, at={self.attack_type}, init={self.initiative}, weak={self.weaknesses}, immune={self.immunities})'
        # return f'(#units={self.units_number}, init={self.initiative})'

    def __lt__(self, value):
        return (self.effective_power(), self.initiative) < (value.effective_power(), value.initiative)


class War:
    IMMUNE_SYSTEM = 'IMMUNE_SYSTEM'
    INFECTION = 'INFECTION'

    def __init__(self, immune_system, infection, boost):
        self.immune_system = immune_system
        self.infection = infection

        for group in self.immune_system:
            group.fraction = War.IMMUNE_SYSTEM
            group.attack_power += boost

        for group in self.infection:
            group.fraction = War.INFECTION

    def simulate(self):
        while not self.is_finished():
            self.fight()
            self.print_state()

    def print_state(self):
        print('Immune System:')
        for group in self.immune_system:
            print(group)

        print('Infection:')
        for group in self.infection:
            print(group)

    def is_finished(self):
        return not self.immune_system or not self.infection

    def get_winning_army(self):
        if not self.immune_system:
            return self.infection

        if not self.infection:
            return self.immune_system

        raise Exception('No winning army!')

    def get_winning_army_units(self):
        winning_army = self.get_winning_army()

        return sum(map(
            lambda g: g.units_number,
            winning_army
        ))

    def immune_system_won(self):
        return not self.infection

    def fight(self):
        groups = list(sorted(
            self.immune_system + self.infection,
            reverse=True
        ))

        not_selected_groups = self.immune_system + self.infection

        combat_pairs = []

        for group in groups:
            target = self.choose_target(group, not_selected_groups)
            combat_pairs.append((group, target))

        sorted_combat_pairs = sorted(
            combat_pairs,
            key=lambda p: p[0].initiative,
            reverse=True
        )

        for attacker, defender in sorted_combat_pairs:
            if not defender:
                continue
            defender.get_hit(attacker)

        self.clean_dead_groups()

    def clean_dead_groups(self):
        self.immune_system = list(filter(
            lambda g: g.units_number > 0,
            self.immune_system
        ))

        self.infection = list(filter(
            lambda g: g.units_number > 0,
            self.infection
        ))

    def choose_target(self, group, not_selected_groups):
        opposite_fraction = self.get_opposite_fraction(group.fraction)
        potential_targets = list(filter(
            lambda g: g.fraction == opposite_fraction and group.damage_to(g),
            not_selected_groups
        ))

        if not potential_targets:
            return None

        potential_damage = map(
            lambda g: (group.damage_to(g), g.effective_power(), g.initiative),
            potential_targets
        )

        _, _, initiative = max(potential_damage)
        max_idx = [g.initiative for g in not_selected_groups].index(initiative)
        target = not_selected_groups[max_idx]
        del not_selected_groups[max_idx]

        return target

    def get_opposite_fraction(self, fraction):
        if fraction == War.IMMUNE_SYSTEM:
            return War.INFECTION
        if fraction == War.INFECTION:
            return War.IMMUNE_SYSTEM

        raise Exception(f'Nonexisting fraction: {fraction}')


def solve(lines):
    boost = 48
    immune_system, infection = [parse_groups(l) for l in lines]
    war = War(immune_system, infection, boost)
    war.simulate()
    
    if not war.immune_system_won():
        return -1

    return war.get_winning_army_units()


input_files = ['imune', 'infection']
lines = [get_lines(filename) for filename in input_files]
result = solve(lines)

print(result)
