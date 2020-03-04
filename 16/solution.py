def addr(registers, in1, in2, out):
    res = registers[:]
    res[out] = res[in1] + res[in2]
    return res


def addi(registers, in1, in2, out):
    res = registers[:]
    res[out] = res[in1] + in2
    return res


def mulr(registers, in1, in2, out):
    res = registers[:]
    res[out] = res[in1] * res[in2]
    return res


def muli(registers, in1, in2, out):
    res = registers[:]
    res[out] = res[in1] * in2
    return res


def banr(registers, in1, in2, out):
    res = registers[:]
    res[out] = res[in1] & res[in2]
    return res


def bani(registers, in1, in2, out):
    res = registers[:]
    res[out] = res[in1] & in2
    return res


def borr(registers, in1, in2, out):
    res = registers[:]
    res[out] = res[in1] | res[in2]
    return res


def bori(registers, in1, in2, out):
    res = registers[:]
    res[out] = res[in1] | in2
    return res


def setr(registers, in1, in2, out):
    res = registers[:]
    res[out] = res[in1]
    return res


def seti(registers, in1, in2, out):
    res = registers[:]
    res[out] = in1
    return res


def gtir(registers, in1, in2, out):
    res = registers[:]
    res[out] = 1 if in1 > res[in2] else 0
    return res


def gtri(registers, in1, in2, out):
    res = registers[:]
    res[out] = 1 if res[in1] > in2 else 0
    return res


def gtrr(registers, in1, in2, out):
    res = registers[:]
    res[out] = 1 if res[in1] > res[in2] else 0
    return res


def eqir(registers, in1, in2, out):
    res = registers[:]
    res[out] = 1 if in1 == res[in2] else 0
    return res


def eqri(registers, in1, in2, out):
    res = registers[:]
    res[out] = 1 if res[in1] == in2 else 0
    return res


def eqrr(registers, in1, in2, out):
    res = registers[:]
    res[out] = 1 if res[in1] == res[in2] else 0
    return res


operations = [
    addr, addi,
    mulr, muli,
    banr, bani,
    borr, bori,
    setr, seti,
    gtir, gtri, gtrr,
    eqir, eqri, eqrr
]


def get_lines():
    filename = 'input'
    file = open(f"{filename}.txt", "r")
    lines = [line.rstrip('\n') for line in file]
    return lines


def parse_instruction(line):
    return [int(x) for x in line.split()]


def parse_registers(line):
    begin_idx = line.find('[')
    end_idx = line.find(']')
    return [int(x) for x in line[begin_idx + 1: end_idx].split(',')]


def get_requests(lines):
    requests = []
    for idx in range(0, len(lines), 4):
        begin = parse_registers(lines[idx])
        instruction = parse_instruction(lines[idx+1])
        end = parse_registers(lines[idx+2])
        requests.append(
            (begin, instruction, end)
        )

    return requests


def match(operation, request):
    registers = request[0]
    opcode, in1, in2, out = request[1]
    result = request[2]

    return result == operation(registers, in1, in2, out)


def solve(requests, operations):
    count = 0
    for request in requests:
        fitting_operations_count = sum(
            [match(operation, request) for operation in operations]
        )

        if fitting_operations_count >= 3:
            count += 1

    return count


lines = get_lines()
requests = get_requests(lines)
result = solve(requests, operations)

print(result)
