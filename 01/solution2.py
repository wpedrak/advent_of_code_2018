from itertools import cycle

file = open("input.txt", "r")
lines = [line.rstrip('\n') for line in file]

# lines = [+3, +3, +4, -2, -4]

changes = cycle([int(x) for x in lines])

current_frequency = 0
visited = set([0])

for change in changes:
    current_frequency += change
    if current_frequency in visited:
        print(current_frequency)
        break
    visited.add(current_frequency)
