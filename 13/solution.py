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

        if is_cart(rail):
            raise Exception(f'Crash on ({self.x}, {self.y})')

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

    def slash(self):
        direction = self.direction
        if direction == '<':
            self.direction = 'v'
        if direction == '>':
            self.direction = '^'
        if direction == '^':
            self.direction = '>'
        if direction == 'v':
            self.direction = '<'

    def backslash(self):
        direction = self.direction
        if direction == '<':
            self.direction = '^'
        if direction == '>':
            self.direction = 'v'
        if direction == '^':
            self.direction = '<'
        if direction == 'v':
            self.direction = '>'

    def intersection(self):
        self.turn_left()

        for _ in range(self.next_turn):
            self.turn_right()

        self.next_turn = (self.next_turn + 1) % 3

    def turn_left(self):
        direction = self.direction
        if direction == '<':
            self.direction = 'v'
        if direction == '>':
            self.direction = '^'
        if direction == '^':
            self.direction = '<'
        if direction == 'v':
            self.direction = '>'

    def turn_right(self):
        direction = self.direction
        if direction == '<':
            self.direction = '^'
        if direction == '>':
            self.direction = 'v'
        if direction == '^':
            self.direction = '>'
        if direction == 'v':
            self.direction = '<'

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

while tick_number < 16:
    print(tick_number)
    tick_number += 1

    for cart in carts:
        cart.tick(original_map)


    carts.sort()
    print(carts)
