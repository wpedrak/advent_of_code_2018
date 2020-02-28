RECIPES_TO_MAKE = 380621

scores = [3, 7]
elf_one_idx = 0
elf_two_idx = 1


def to_digits(n):
    if n < 10:
        return [n]
    return [1, n % 10]


while len(scores) < RECIPES_TO_MAKE + 10:
    new_recipe = scores[elf_one_idx] + scores[elf_two_idx]
    new_scores = to_digits(new_recipe)
    scores += new_scores
    elf_one_idx = (elf_one_idx + scores[elf_one_idx] + 1) % len(scores)
    elf_two_idx = (elf_two_idx + scores[elf_two_idx] + 1) % len(scores)
    # print(scores)

result = ''.join([str(x)
                  for x in scores[RECIPES_TO_MAKE:RECIPES_TO_MAKE + 10]])

print(result)
