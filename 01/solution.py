file = open("input.txt", "r")
lines = [line.rstrip('\n') for line in file]

result = sum([int(x) for x in lines])

print(result)
