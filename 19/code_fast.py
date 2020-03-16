THRESHOLD = 10551260
result = 0

for number in range(1, THRESHOLD + 1):
    if THRESHOLD % number == 0:
        result += number

print(result)
