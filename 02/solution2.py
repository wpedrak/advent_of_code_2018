from itertools import combinations


def differ_by_one(word1, word2):
    # same size
    length = len(word1)
    simmilarities = map(
        lambda x: x[0] == x[1],
        zip(word1, word2)
    )

    return sum(simmilarities) == length - 1


file = open("input.txt", "r")
lines = [line.rstrip('\n') for line in file]

for id1, id2 in combinations(lines, 2):
    if differ_by_one(id1, id2):
        print(id1)
        print(id2)
