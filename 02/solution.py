from collections import Counter

def check_count(count):
    def aux(word):
        counter = Counter(word)
        return count in counter.values()
    return aux

is_double = check_count(2)
is_triple = check_count(3)

file = open("input.txt", "r")
lines = [line.rstrip('\n') for line in file]

doubles = 0
triples = 0

for box_id in lines:
    doubles += is_double(box_id)
    triples += is_triple(box_id)

result = doubles * triples

print(result)