from collections import Counter

def main():
    with open("day01/day01.txt") as f:
        lines = [x.strip().split() for x in f.readlines()]
    left_list, right_list = [], []
    for line in lines:
        left_list.append(int(line[0]))
        right_list.append(int(line[1]))

    left_list = sorted(left_list)
    right_list = sorted(right_list)

    # part 1
    diffs = []
    for l, r in zip(left_list, right_list):
        diffs.append(abs(l - r))
    print(sum(diffs))

    # part 2
    c = Counter(right_list)
    similarity_scores = [c[n] * n for n in left_list]
    print(sum(similarity_scores))

if __name__ == "__main__":
    main()
