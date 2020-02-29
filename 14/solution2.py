PATTERN_TO_FIND = [int(x) for x in '380621']
RECIPES_TO_MAKE = 100000000


scores = [3, 7]
elf_one_idx = 0
elf_two_idx = 1


def to_digits(n):
    if n < 10:
        return [n]
    return [1, n % 10]


while len(scores) < RECIPES_TO_MAKE:
    new_recipe = scores[elf_one_idx] + scores[elf_two_idx]
    new_scores = to_digits(new_recipe)
    scores += new_scores
    elf_one_idx = (elf_one_idx + scores[elf_one_idx] + 1) % len(scores)
    elf_two_idx = (elf_two_idx + scores[elf_two_idx] + 1) % len(scores)

pattern_length = len(PATTERN_TO_FIND)

for pattern_begin in range(RECIPES_TO_MAKE - pattern_length):
    if PATTERN_TO_FIND == scores[pattern_begin : pattern_begin + pattern_length]:
        print(pattern_begin)
        break
