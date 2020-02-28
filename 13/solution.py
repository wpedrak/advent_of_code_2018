def get_lines():
    file = open("input.txt", "r")
    lines = [line.rstrip('\n') for line in file]
    return lines

def remove_carts(part_of_map):
    return part_of_map.replace('>', '-'). replace('<', '-').replace('^', '|').replace('v', '|')

lines = get_lines()
original_map = [remove_carts(line) for line in lines]

print('\n'.join(original_map))
