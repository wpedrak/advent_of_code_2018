THRESHOLD = 10551260
x0 = 0
x2 = 1
x3 = 1

while True:
    # print(x2, x0)
    if x2 * x3 == THRESHOLD:
        x0 += x3

    x2 += 1

    if x2 <= THRESHOLD:
        continue

    x3 += 1

    if x3 <= THRESHOLD:
        x2 = 1
        continue

print(x0) 