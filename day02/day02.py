from itertools import tee
from typing import List, NamedTuple

class Report(NamedTuple):
    raw: List[int]
    diffs: List[int]
    is_safe: bool

def pairwise(lst):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(lst)
    next(b, None)
    return zip(a, b)

def calculate_diffs(report: list) -> list:
    p = pairwise(report)
    diffs = []
    for _ in range(len(report) -1):
        a, b = next(p)
        diffs.append(a - b)
    return diffs

def is_report_safe(report: list) -> bool:
    single_direction  = bool(
        all([diff >= 0 for diff in report])
        or
        all([diff <= 0 for diff in report])
    )
    less_than_4 = all([abs(diff) < 4 for diff in report])
    non_zero = all([diff != 0 for diff in report])

    return single_direction and less_than_4 and non_zero

def compute_safe_reports_with_problem_dampener(reports: list) -> int:
    res = []
    for report in reports:
        report_obj = Report(raw=report,
                            diffs=calculate_diffs(report),
                            is_safe=is_report_safe(calculate_diffs(report)))
        if report_obj.is_safe:
            # happy path
            res.append(report_obj)
        else:
            # need to check again if we drop one value from the report
            # 1. create all possible variations
            modified_reports = []
            for index in range(len(report)):
                new_report = report.copy()
                modified_reports.append([x for i, x in enumerate(new_report) if i != index])

            # 2. create all corresponding objects and compute is_sage
            modified_reports_obj = [
                Report(raw=modified_report,
                       diffs=calculate_diffs(modified_report),
                       is_safe=is_report_safe(calculate_diffs(modified_report)))
                for modified_report
                in modified_reports
                ]

            # 3. if there is any safe report in the modified reports, we will add it to the result (just one!)
            for modified_reports_obj in modified_reports_obj:
                if modified_reports_obj.is_safe:
                    res.append(modified_reports_obj)
                    break
    return len(res)


def main():
    with open("day02/day02.txt") as f:
        reports = [[int(val) for val in line.split()] for line in f.readlines()]
    diffs = [calculate_diffs(report) for report in reports]
    safes = [is_report_safe(diff) for diff in diffs]

    # part 1
    print(sum(safes))

    # part 2
    print(compute_safe_reports_with_problem_dampener(reports))

if __name__ == "__main__":
    main()
