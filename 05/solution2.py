def get_polymer():
    file = open("input.txt", "r")
    lines = [line.rstrip('\n') for line in file]
    return lines[0]


def will_react(u1, u2):
    return u1 != u2 and u1.upper() == u2.upper()


def check_polymer_size(polymer):
    left_stack = list(polymer)
    right_stack = []

    while left_stack:
        left_unit = left_stack.pop()

        if not right_stack:
            right_stack.append(left_unit)
            continue

        right_unit = right_stack.pop()

        if not will_react(left_unit, right_unit):
            right_stack.append(right_unit)
            right_stack.append(left_unit)

    return len(right_stack)


polymer = get_polymer()

all_unit = set([x.upper() for x in polymer])

results = []

for unit_to_remove in all_unit:
    better_polymer = filter(
        lambda x: x.upper() != unit_to_remove,
        polymer
    )

    results.append(check_polymer_size(better_polymer))

print(min(results))
