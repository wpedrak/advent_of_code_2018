def get_lines():
    filename = 'input'
    file = open(f"{filename}.txt", "r")
    lines = [line.rstrip('\n') for line in file]
    return lines

class Nanobot:
    def __init__(self, x, y, z, r):
        self.x = x
        self.y = y
        self.z = z
        self.r = r

    def dist(self, nanobot):
        return abs(self.x - nanobot.x) + abs(self.y - nanobot.y) + abs(self.z - nanobot.z)

    def have_in_range(self, nanobot):
        return self.dist(nanobot) <= self.r


def parse_line(line):
    left_brace_idx = line.find('<')
    right_brace_idx = line.find('>')

    coordinates = line[left_brace_idx + 1:right_brace_idx]
    x, y, z = map(int, coordinates.split(','))

    r_idx = line.find('r')

    r = int(line[r_idx+2:])

    return Nanobot(x, y, z, r)

def parse(lines):
    return [parse_line(line) for line in lines]

def solve(nanobots):
    max_range_nanobot = max(nanobots, key=lambda x: x.r)
    return sum([max_range_nanobot.have_in_range(n) for n in nanobots])


lines = get_lines()
nanobots = parse(lines)
result = solve(nanobots)

print(result)
