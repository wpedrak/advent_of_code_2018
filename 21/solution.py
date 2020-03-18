from collections import defaultdict


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


OPERATIONS = {
    'addr': addr,
    'addi': addi,
    'mulr': mulr,
    'muli': muli,
    'banr': banr,
    'bani': bani,
    'borr': borr,
    'bori': bori,
    'setr': setr,
    'seti': seti,
    'gtir': gtir,
    'gtri': gtri,
    'gtrr': gtrr,
    'eqir': eqir,
    'eqri': eqri,
    'eqrr': eqrr
}


def get_lines():
    filename = 'input'
    file = open(f"{filename}.txt", "r")
    lines = [line.rstrip('\n') for line in file]
    return lines


def get_ip_bind(line):
    return int(line[-1])


def parse_command(command):
    opcode, in1, in2, out = command.split()
    return (opcode, int(in1), int(in2), int(out))

def parse_program(lines):
    return [parse_command(line) for line in lines]


def debug(program, ip_bind):
    registers = [0, 0, 0, 0, 0, 0]
    ip = 0
    size = len(program)

    while ip < size:
        if ip == 28:
            return registers[4]
        opcode, in1, in2, out = program[ip]
        operation = OPERATIONS[opcode]
        registers[ip_bind] = ip
        registers = operation(registers, in1, in2, out)
        ip = registers[ip_bind]
        ip += 1

    raise Exception('Halt without looking at register 0')

lines = get_lines()
ip_bind = get_ip_bind(lines[0])
program = parse_program(lines[1:])

result = debug(program, ip_bind)
print(result)
