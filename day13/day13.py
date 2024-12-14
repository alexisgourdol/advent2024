from ortools.linear_solver import pywraplp


def parse_input(raw: str) -> list:

    blocks = raw.strip().split('\n\n')
    lines = [block.split('\n') for block in blocks]
    parsed = []
    for line in lines:
        equations = []
        target = None
        for segment in line :
            if segment.startswith('Button'):
                button, rest = segment.strip('Button ').split(':')
                rest = [int(val.strip(" X+").strip("Y+")) for val in rest.split(', ')]
                x_val, y_val = rest[0], rest[1]
                equations.append((x_val, y_val))
            elif segment.startswith('Prize'):
                rest = segment.strip('Prize: ').split(',')
                rest = [int(val.strip().strip("X=").strip().strip(" Y=")) for val in rest]
                x_target, y_target = rest[0], rest[1]
                target = x_target, y_target
            else:
                print(f'Error: {line=}')
            if target:
                parsed.append((equations, target))
    return parsed

def cost_to_win(equations: list, target: tuple, verbose=False, target_adj=False) -> None:
    upper_bound = 100
    coeff_a, coeff_b = equations    #[(94, 34), (22, 67)]
    coeff_xa, coeff_ya = coeff_a
    coeff_xb, coeff_yb = coeff_b
    target_x, target_y = target     #(8400, 5400))

    solver = pywraplp.Solver('Minimize cost', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

    if target_adj:
        upper_bound = solver.infinity()
        #print(f"{target_x =} , {target_y =} |||| {upper_bound =} {coeff_a =} {coeff_b =}")
        target_x += 10_000_000_000_000
        target_y += 10_000_000_000_000

    # 1. Create the variables we want to optimize
    a_button_press = solver.IntVar(0, upper_bound, 'a_button_press')
    b_button_press = solver.IntVar(0, upper_bound, 'b_button_press')

    # 2. Add constraints for each resource
    solver.Add(a_button_press * coeff_xa + b_button_press * coeff_xb == target_x)
    solver.Add(a_button_press * coeff_ya  + b_button_press * coeff_yb == target_y)

    # 3. Minimize the objective function
    solver.Minimize(3 * a_button_press + 1 * b_button_press)

    # Solve problem
    status = solver.Solve()
    # If an optimal solution has been found, print results

    if status == pywraplp.Solver.OPTIMAL:
        optimal_value = solver.Objective().Value()
        if verbose:
            print('================= Solution =================')
            print(f'Solved in {solver.wall_time():.2f} milliseconds in {solver.iterations()} iterations')
            print()
            print(f'Optimal value = {optimal_value}')
            print('Result:')
            print(f' - Number of times the A button is pressed = {a_button_press.solution_value()}')
            print(f' - Number of times the B button is pressed = = {b_button_press.solution_value()}')
        return optimal_value
    else:
        if verbose:
            print('The solver could not find an optimal solution.')
    return

def compute_total(inp: list, verbose=False, target_adj=False) -> int:
    total = 0
    for system in inp:
        equations, target = system
        res = cost_to_win(equations, target, verbose=verbose, target_adj=target_adj)
        total += res if res else 0
    return int(total)


if __name__ == "__main__":
    RAW = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""

    inp = parse_input(RAW)
    assert inp == [([(94, 34), (22, 67)], (8400, 5400)), ([(26, 66), (67, 21)], (12748, 12176)), ([(17, 86), (84, 37)], (7870, 6450)), ([(69, 23), (27, 71)], (18641, 10279))]
    assert compute_total(inp) == 480
    compute_total(inp, target_adj=True, verbose=True)


    verbose=True

    with open('day13.txt') as f:
        raw = f.read()
    inp = parse_input(raw)

    print(compute_total(inp)) # 39996

    print("part 2 : 58770475218851 too low")
    print(compute_total(inp, target_adj=True, verbose=True)) # 58770475218851 too low






