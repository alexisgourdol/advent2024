"""8 instructions

1 instructions
- is identified by a 3-bit number opcode
    - 0 : "adv"
    - 1 : "bxl"
    - 2 : "bst"
    - 3 : "jzn"
    - 4 : "bxc"
    - 5 : "out"
    - 6 : "bdv"
    - 7 : "cdv"
- and the operand next to the opcode next to the opcode, as input
    - Combo operands 0 through 3 represent literal values 0 through 3.
    - Combo operand 4 represents the value of register A.
    - Combo operand 5 represents the value of register B.
    - Combo operand 6 represents the value of register C.
    - Combo operand 7 is reserved and will not appear in valid programs.


instruction pointer he position in the program (starts at 0)
- if no jump : increments by 2


Representation of 3 bit numbers

0: 000
1: 001
2: 010
3: 011
4: 100
5: 101
6: 110
7: 111
"""

from typing import List, Tuple

Program = List[int]
Registers = Tuple[int, int, int]

def parse(raw: str) -> Tuple[Program, Registers]:
    registers, program = raw.strip().split("\n\n")
    registers= [int(r.strip().strip("Register A: ").strip("Register B: ").strip("Register C: ")) for r in registers.split("\n")]
    program = [int(el) for el in program.strip("Program: ").split(",")]
    # print(f"{registers=}, {program=}")
    return registers, program

def get_combo_operand(operand, registers):
    if operand in [0, 1, 2, 3]:
        return operand
    elif operand == 4:
        return registers[0]
    elif operand == 5:
        return registers[1]
    elif operand == 6:
        return registers[2]
    elif operand == 7:
        raise ValueError("operand 7 should not appear in valid programs")
    else:
        raise ValueError("{operand} is not between 0 and 6")

def process(registers, program, pointer):
    jump = False
    output = None
    opcode = program[pointer]
    operand = program[pointer + 1]

    if opcode == 0:
        registers[0] = registers[0] // (2 ** get_combo_operand(operand, registers))
    if opcode == 1:
        registers[1] = registers[1] ^ operand
    if opcode == 2:
        registers[1] = get_combo_operand(operand, registers) % 8
    if opcode == 3:
        if registers[0] == 0:
            pass
        else:
            jump = True # will set the pointer to proper vlue in the while loop
    if opcode == 4:
        registers[1] = registers[1] ^ registers[2]
    if opcode == 5:
        output = get_combo_operand(operand, registers) % 8
    if opcode == 6:
        registers[1] = registers[0] // (2 ** get_combo_operand(operand, registers))
    if opcode == 7:
        registers[2] = registers[0] // (2 ** get_combo_operand(operand, registers))

    # print(f"{opcode=}, {operand=}, {jump=}, {output=}")
    return registers, program, jump, opcode, operand, output




if __name__ == "__main__":
    RAW = """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0"""

    with open("day17.txt") as f:
        inp = f.read()

    selected_input = inp # <- change here for RAW or inp

    r, p = parse(inp)
    pointer = 0
    outputs = []
    while True:
        #print(f"{pointer=}, {outputs}")
        r, p, j, opc, opr, out = process(r, p, pointer)
        if j:
            pointer = opr
        else :
            pointer += 2
        if out is not None:
            outputs.append(out)
        if pointer > len(p) - 1:
            break
    print(",".join([str(o) for o in outputs]))
    if selected_input == inp:
        print(f"part 1 : ", "".join([str(o) for o in outputs]))
    if selected_input == RAW:
        print(f"test : ", "".join([str(o) for o in outputs]))

