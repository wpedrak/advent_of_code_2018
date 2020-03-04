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


def get_lines(load_program=False):
    filename = 'input2' if load_program else 'input'
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

def get_program(lines):
    return [parse_instruction(line) for line in lines]

def match(operation, request):
    registers = request[0]
    opcode, in1, in2, out = request[1]
    result = request[2]

    return result == operation(registers, in1, in2, out)


def find_opcodes(requests, operations_arg):
    operations = operations_arg[:]
    found = set()
    print('{')
    while operations:
        for request in requests:
            fitting_operations = [
                match(operation, request) for operation in operations
            ]

            if sum(fitting_operations) != 1:
                continue

            opcode = request[1][0]

            func_idx = fitting_operations.index(True)
            func = operations[func_idx]
            function_name = func.__name__

            print(f'{opcode}: {function_name},')
            del operations[func_idx]

    print('}')

def solve(program, operations):
    registers = [0, 0, 0, 0]

    for instruction in program:
        opcode, in1, in2, out = instruction
        operation = operations[opcode]
        registers = operation(registers, in1, in2, out)

    return registers[0]


lines = get_lines()
requests = get_requests(lines)
# find_opcodes(requests, operations)

opcodes_to_operation = {
    0: eqir,
    1: seti,
    2: eqri,
    3: eqrr,
    4: addi,
    5: setr,
    6: gtrr,
    7: gtri,
    8: muli,
    9: bori,
    10: bani,
    11: borr,
    12: gtir,
    13: banr,
    14: addr,
    15: mulr,
}

program_lines = get_lines(load_program=True)
program = get_program(program_lines)
result = solve(program, opcodes_to_operation)

print(result)