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


def parse_program(lines):
    program = []
    for line in lines:
        opcode, in1, in2, out = line.split()
        program.append((opcode, int(in1), int(in2), int(out)))

    return program


def override(program, overrides):
    class Prog:
        def __init__(self, program, overrides):
            self.program = program
            self.overrides = overrides
            self.used = defaultdict(lambda: 0)

        def __getitem__(self, idx):
            if idx not in self.overrides or self.used[idx]:
                return program[idx]

            self.used[idx] += 1

            return self.overrides[idx]

    return Prog(program, overrides)


def solve(program, ip_bind):
    registers = [1, 0, 0, 0, 0, 0]
    ip = 0

    size = len(program)
    program = override(program, {
        2: ('seti', 10551260, 6, 2)
    })

    while ip < size:
        opcode, in1, in2, out = program[ip]
        operation = OPERATIONS[opcode]
        registers[ip_bind] = ip
        print(f'ip={ip}', end=' ')
        print(registers, end=' ')
        print(opcode, in1, in2, out, end=' ')
        registers = operation(registers, in1, in2, out)
        ip = registers[ip_bind]
        print(registers, end='\n')
        ip += 1

    return registers[0]


lines = get_lines()
ip_bind = get_ip_bind(lines[0])
program = parse_program(lines[1:])

result = solve(program, ip_bind)
print(result)
