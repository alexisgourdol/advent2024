import re
from typing import List

RAW_1 = """do()xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"""
RAW_2 = """do()xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"""

def main():
    with open("day03/day03.txt", "r") as f:
        inp = f.read()

    def process_1(expressions: List[str]):
        values = [e.strip("mul").strip("(").strip(")").split(",") for e in expressions]
        values = [[int(v) for v in value] for value in values]
        results = [value[0] * value[1] for value in values]
        return(sum(results))

    #part 1
    pattern_1 = r"mul\(\d{1,3},\d{1,3}\)"
    expressions = re.findall(pattern_1, inp)
    print(process_1(expressions))


    # part 2
    def process_2(inp):
        # Regex to capture blocks starting with `do()` and ending with `don't()` or the end of the string
        do_block_pattern = r"do\(\)(.*?)(?=don't\(\)|$)"
        # Find all `do()` blocks
        do_blocks = re.findall(do_block_pattern, inp, re.DOTALL)

        mul_pattern = r"mul\(\d{1,3},\d{1,3}\)"
        results = [re.findall(mul_pattern, block) for block in do_blocks]
        # flatten the results list since re.findall returns lists
        results = [item for sublist in results for item in sublist]
        return process_1(results)

    print(process_2("do()" + inp))
    process_1

if __name__ == "__main__":
    main()

