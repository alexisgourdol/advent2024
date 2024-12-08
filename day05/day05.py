from typing import List, Tuple
from itertools import combinations, permutations
from tqdm import tqdm


def main():
    with open("day05/day05.txt") as f:
        raw_ordering_rules, raw_updates = f.read().split("\n\n")
    ordering_rules, updates = parse(raw_ordering_rules, raw_updates)
    are_updates_valid = check_updates_validity(updates, ordering_rules)
    print("part1 : ", compute_middle_numbers_sum(are_updates_valid, updates))
    print(
        "part2 : ",
        compute_middle_numbers_sum(
            *fix_wrong_updates(are_updates_valid, updates, ordering_rules), updates
        ),
    )


def parse(raw_ordering_rules: str, raw_updates: str) -> Tuple[List[Tuple], List[Tuple]]:
    ordering_rules = raw_ordering_rules.strip().split("\n")
    ordering_rules = [(tuple(map(int, rule.split("|")))) for rule in ordering_rules]
    updates = raw_updates.strip().split("\n")
    updates = [list(map(int, update.split(","))) for update in updates]

    return ordering_rules, updates


def check_updates_validity(
    updates: List[List[int]], ordering_rules: List[Tuple]
) -> List[bool]:
    are_updates_valid = []
    for update in updates:
        all_combinations = list(combinations(update, 2))
        # print(f"{set(all_combinations)=}")
        # print(f"{set(ordering_rules)=}")
        # print(f"{set(all_combinations).difference(set(ordering_rules))=}")
        # print(f"{set(all_combinations).difference(set(ordering_rules)) == set() =}")
        if set(all_combinations).difference(set(ordering_rules)) == set():
            are_updates_valid.append(True)
        else:
            are_updates_valid.append(False)
    return are_updates_valid


def compute_middle_numbers_sum(are_updates_valid: List[bool], updates):
    """Each updates, filter only the ones that are valid (True) and pick their middle numbers. Sum these numbers"""
    sum_middle_numbers = 0
    for i, update in enumerate(updates):
        if are_updates_valid[i]:
            mid_num = len(update) // 2
            sum_middle_numbers += update[mid_num]
    return sum_middle_numbers


def fix_wrong_updates(are_updates_valid: List[bool], updates, ordering_rules):
    fixed_updates = []
    # Filter only wrong updates
    for i, update in enumerate(updates):

        # get all permutations of the updates as List[List[int]]
        if not are_updates_valid[i]:
            all_permutations = permutations(update)
            # check validity for each permutation
            for p in tqdm(all_permutations):
                print(f"{i=}, {update=}, {p=}")
                is_p_valid = check_updates_validity([list(p)], ordering_rules)
                # print(f"{p=}, {is_p_valid=}")
                if is_p_valid[0]:
                    fixed_updates.append(list(p))
                    break
    return [True for _ in fixed_updates], fixed_updates


if __name__ == "__main__":
    #     RAW = """47|53
    # 97|13
    # 97|61
    # 97|47
    # 75|29
    # 61|13
    # 75|53
    # 29|13
    # 97|29
    # 53|29
    # 61|53
    # 97|53
    # 61|29
    # 47|13
    # 75|47
    # 97|75
    # 47|61
    # 75|61
    # 47|29
    # 75|13
    # 53|13

    # 75,47,61,53,29
    # 97,61,53,29,13
    # 75,29,13
    # 75,97,47,61,53
    # 61,13,29
    # 97,13,75,29,47"""

    #     raw_ordering_rules, raw_updates = RAW.split("\n\n")
    #     t_ordering_rules, t_updates = parse(raw_ordering_rules, raw_updates)
    #     t_are_updates_valid = check_updates_validity(t_updates, t_ordering_rules)
    #     assert compute_middle_numbers_sum(t_are_updates_valid, t_updates) == 143
    #     assert fix_wrong_updates(t_are_updates_valid, t_updates, t_ordering_rules) == (
    #         [True, True, True],
    #         [[97, 75, 47, 61, 53], [61, 29, 13], [97, 75, 47, 29, 13]],
    #     )
    #     assert (
    #         compute_middle_numbers_sum(
    #             *fix_wrong_updates(t_are_updates_valid, t_updates, t_ordering_rules)
    #         )
    #         == 123
    #     )

    main()
