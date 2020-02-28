def get_lines():
    file = open("input.txt", "r")
    lines = [line.rstrip('\n') for line in file]
    return lines


def remove_carts(part_of_map):
    return part_of_map.replace('>', '-'). replace('<', '-').replace('^', '|').replace('v', '|')


def is_cart(c):
    return c in '<>^v'


class Cart:
    LEFT = 0
    FORWARD = 1
    RIGHT = 2

    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.next_turn = Cart.LEFT

    def __lt__(self, cart):
        return (self.y, self.x) < (cart.y, cart.x)

    def tick(self, rails):
        dx, dy = self.move()
        self.x += dx
        self.y += dy

        rail = rails[self.y][self.x]

        self.adjust_direction(rail)

    def adjust_direction(self, rail):
        if rail == '+':
            self.intersection()
            return

        if rail == '/':
            self.slash()
            return

        if rail == '\\':
            self.backslash()
            return

        if rail in '|-':
            return

        raise Exception(f'Unlegal rail:"{rail}"')

    def case_on_direction(self, cases):
        direction = self.direction
        if direction == '<':
            self.direction = cases[0]
        if direction == '>':
            self.direction = cases[1]
        if direction == '^':
            self.direction = cases[2]
        if direction == 'v':
            self.direction = cases[3]

    def slash(self):
        self.case_on_direction('v^><')

    def backslash(self):
        self.case_on_direction('^v<>')

    def intersection(self):
        self.turn_left()

        for _ in range(self.next_turn):
            self.turn_right()

        self.next_turn = (self.next_turn + 1) % 3

    def turn_left(self):
        self.case_on_direction('v^<>')

    def turn_right(self):
        self.case_on_direction('^v><')

    def move(self):
        direction = self.direction
        if direction == '<':
            return -1, 0
        if direction == '>':
            return 1, 0
        if direction == '^':
            return 0, -1
        if direction == 'v':
            return 0, 1

        raise Exception(f'Wrong direction: "{direction}"')

    def __str__(self):
        return f'({self.x}, {self.y}, {self.direction})'

    def __repr__(self):
        return str(self)


def find_accidents(carts):
    carts_coordinates = set((c.x, c.y) for c in carts)

    accidents = []

    for cart in carts:
        coordinates = (cart.x, cart.y)

        if coordinates not in carts_coordinates:
            accidents.append(coordinates)
            continue

        carts_coordinates.remove(coordinates)
    
    return accidents

lines = get_lines()
original_map = [remove_carts(line) for line in lines]

carts = []

for y, row in enumerate(lines):
    for x, elem in enumerate(row):
        if is_cart(elem):
            cart = Cart(x, y, elem)
            carts.append(cart)

carts.sort()

tick_number = 0

while True:
    print(tick_number)
    tick_number += 1

    for cart in carts:
        cart.tick(original_map)

        accidents = find_accidents(carts)
        if accidents:
            print(accidents)
            raise Exception('Carts crashed!')
    carts.sort()
