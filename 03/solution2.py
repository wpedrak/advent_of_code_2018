from re import search


def parse_claim(claim):
    search_result = search(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)', claim)

    return [int(search_result.group(i)) for i in range(1, 6)]


def mark_on_fabric(fabric, x, y, width, height):
    new_ones = 0
    for y_delta in range(height):
        for x_delta in range(width):
            fabric[y+y_delta][x+x_delta] += 1
            if fabric[y+y_delta][x+x_delta] == 1:
                new_ones += 1
                
    return new_ones


def get_lines():
    file = open("input.txt", "r")
    lines = [line.rstrip('\n') for line in file]
    return lines


def get_fabric():
    fabric_edge_size = 1000
    fabric = [[0] * fabric_edge_size for _ in range(fabric_edge_size)]
    return fabric


def get_partial_success(claims):
    fabric = get_fabric()
    success = set()

    for claim in claims:
        claim_id, from_left, from_top, width, height = parse_claim(claim)
        new_ones = mark_on_fabric(fabric, from_left, from_top, width, height)

        if new_ones == width * height:
            success.add(claim_id)

    return success


lines = get_lines()
reversed_lines = list(reversed(get_lines()))

forward_result = get_partial_success(lines)
backward_result = get_partial_success(reversed_lines)

result = forward_result & backward_result

print(result)
