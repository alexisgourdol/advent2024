from typing import List, Tuple

Program = List[int]
Registers = Tuple[int, int, int]


def parse(raw: str) -> Tuple[Program, Registers]:
    registers, program = raw.strip().split("\n\n")
    registers = [
        int(r.strip().strip("Register A: ").strip("Register B: ").strip("Register C: "))
        for r in registers.split("\n")
    ]
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
        raise ValueError(f"{operand} is not between 0 and 6")


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
            jump = True  # will set the pointer to proper vlue in the while loop
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


def run(raw):
    r, p = parse(raw)
    pointer = 0
    outputs = []
    while True:
        # print(f"{pointer=}, {outputs}")
        r, p, j, opc, opr, out = process(r, p, pointer)
        if j:
            pointer = opr
        else:
            pointer += 2
        if out is not None:
            outputs.append(out)
        if pointer > len(p) - 1:
            break
    # print(r)
    return ",".join([str(o) for o in outputs])


def run_2(raw):
    increment = 0
    r, p = parse(raw)
    original_registers = r.copy()
    original_program = p.copy()
    print(original_registers)
    while True:
        increment = +1
        pointer = 0
        outputs = []
        print(f"{increment=}")
        while True:
            print(f"{pointer=}, {outputs}")
            r, p, j, opc, opr, out = process(r, p, pointer)
            if j:
                pointer = opr
            else:
                pointer += 2
            if out is not None:
                outputs.append(out)
            if outputs:
                for oi, pi in zip(outputs, original_program):
                    print(f"{oi=}, {pi=}")
                    # for every new output, check if is starts as the original program
                    if oi != pi:
                        pointer = len(p)
            if pointer > len(p) - 1:
                break
        if original_registers == outputs:
            break
    return original_registers[0] + increment


if __name__ == "__main__":
    RAW = """Register A: 729\nRegister B: 0\nRegister C: 0\n\nProgram: 0,1,5,4,3,0"""

    assert process([0, 0, 9], [2, 6], 0)[0][1] == 1
    assert (
        run("""Register A: 10\nRegister B: 0\nRegister C: 0\n\nProgram: 5,0,5,1,5,4""")
        == "0,1,2"
    )
    assert (
        run(
            """Register A: 2024\nRegister B: 0\nRegister C: 0\n\nProgram: 0,1,5,4,3,0"""
        )
        == "4,2,5,6,7,7,7,7,3,1,0"
    )
    run(
        """Register A: 2024\nRegister B: 0\nRegister C: 0\n\nProgram: 0,1,5,4,3,0"""
    )  # registers=[0, 7, 0] => leave 0 in register A : OK, checked via print statement
    assert process([0, 29, 0], [1, 7], 0)[0][1] == 26
    assert process([0, 2024, 43690], [4, 0], 0)[0][1] == 44354
    assert run(RAW) == "4,6,3,5,6,3,5,2,1,0"

    with open("day17.txt") as f:
        inp = f.read()

    outputs = run(inp)
    print(f"part 1 :", outputs)
    print(f"       :", "".join([o for o in outputs if o != ","]))

    print(
        "part 2 test",
        run_2(
            """Register A: 2024\nRegister B: 0\nRegister C: 0\n\nProgram: 0,3,5,4,3,0"""
        ),
    )  # 729
    # print(f"part 2 :", run_2(inp))  # 46337278 too low
