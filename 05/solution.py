def get_polymer():
    file = open("input.txt", "r")
    lines = [line.rstrip('\n') for line in file]
    return lines[0]

def will_react(u1, u2):
    return u1 != u2 and u1.upper() == u2.upper()

def try_reduce(polymer):
    length = len(polymer)

    for idx in range(length - 1):
        unit1 = polymer[idx]
        unit2 = polymer[idx + 1]

        if will_react(unit1, unit2):
            return polymer[:idx] + polymer[idx + 2:]

    return polymer

polymer = get_polymer()

polymer_size = len(polymer)

polymer = try_reduce(polymer)

while polymer_size != len(polymer):
    print(polymer_size)
    polymer_size = len(polymer)
    polymer = try_reduce(polymer)


print(len(polymer))
