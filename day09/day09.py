

# Goal : to move file blocks one at a time from the end of the disk
# to the leftmost free space block
def represent(raw: str) -> str:
    s = ""
    id = 0
    for i , digit in enumerate(raw):
        if i % 2 == 0:
            s = s + "".join(str(id) * int(digit))
            id += 1
        else:
            s = s + "".join("." * int(digit))
    return s

def swap(s: str) -> list:
    s_list = list(s)
    max_pop = len([el for el in s_list if el == "."]) + 1000
    num_popped = 0
    early_stop = 0
    res = []
    for char in s_list:
        # early_stop +=1
        if char != ".":
            res.append(char)
            # print(f"{char=}, {''.join(s_list)[:20]=} , popped=None, {''.join(res)[:20]=}")
        else:
            while True:
                if num_popped <= max_pop:
                    popped = s_list.pop()
                    num_popped += 1
                    if popped != ".":
                        res.append(popped)
                        # print(f"{char=}, {''.join(s_list)[:20]=} , {popped=}, {''.join(res)[:20]=}")
                        break
                else:
                    break
        # if early_stop > 20:
        #     break
    return res

def checksum(res: list) -> int:
    return sum([i * int(el) for i, el in enumerate(res)])

RAW_MAP = """12345"""
#ID number based on the order of the files as they appear *before* they are rearranged
assert represent(RAW_MAP) == """0..111....22222"""
# assert swap(represent(RAW_MAP)) == ['0', '2', '2', '1', '1', '1', '2', '2', '2']

RAW_MAP_2 = """2333133121414131402"""
assert represent(RAW_MAP_2) == """00...111...2...333.44.5555.6666.777.888899"""
# assert swap(represent(RAW_MAP_2)) == ['0', '0', '9', '9', '8', '1', '1', '1', '8', '8', '8', '2', '7', '7', '7', '3', '3', '3', '6', '4', '4', '6', '5', '5', '5', '5', '6', '6']
# assert checksum(swap(represent(RAW_MAP_2))) == 1928



def main():
    with open("day09.txt") as f:
        raw_map = f.read().strip()
    string_representation = represent(raw_map)
    swapped = swap(string_representation)
    print(f'part 1 : {checksum(swapped)}') # Wrong, too low part 1 : 91088873473


if __name__ == "__main__":
    ...
    main()
