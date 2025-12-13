import re
from typing import List, Tuple, Optional
import pulp


def parse_machine_part2(line: str) -> Tuple[List[int], List[List[int]]]:
    """Parse a machine configuration line for part 2.

    Args:
        line: A line from the CSV file

    Returns:
        Tuple of (target_joltages, buttons) where:
        - target_joltages is a list of target counter values
        - buttons is a list of button configurations, each a list of counter indices
    """
    line = line.strip()
    if not line:
        return [], []

    # Extract the joltage requirements {3,5,4,7}
    joltage_match = re.search(r'\{([0-9,]+)\}', line)
    if not joltage_match:
        return [], []

    joltage_str = joltage_match.group(1)
    target_joltages = [int(x) for x in joltage_str.split(',')]

    # Extract button configurations (0,1,2) (3,4) etc.
    button_pattern = r'\(([0-9,]+)\)'
    button_matches = re.findall(button_pattern, line)

    buttons = []
    for button_str in button_matches:
        indices = [int(x) for x in button_str.split(',')]
        buttons.append(indices)

    return target_joltages, buttons


def solve_joltage_ilp(target_joltages: List[int], buttons: List[List[int]]) -> Optional[int]:
    """Solve the joltage counter problem using Integer Linear Programming.

    This creates an ILP problem where:
    - Each button can be pressed a non-negative integer number of times
    - Each button press increments certain counters by 1
    - We need to reach the target joltage values
    - Minimize the total number of button presses

    Args:
        target_joltages: List of target counter values
        buttons: List of button configurations

    Returns:
        Minimum number of button presses, or None if no solution exists
    """
    if not target_joltages or not buttons:
        return 0

    # Check if all targets are zero
    if all(t == 0 for t in target_joltages):
        return 0

    num_counters = len(target_joltages)
    num_buttons = len(buttons)

    # Create the ILP problem
    prob = pulp.LpProblem("JoltageConfiguration", pulp.LpMinimize)

    # Decision variables: number of times each button is pressed
    button_presses = [
        pulp.LpVariable(f"button_{i}", lowBound=0, cat='Integer')
        for i in range(num_buttons)
    ]

    # Objective: minimize total button presses
    prob += pulp.lpSum(button_presses)

    # Constraints: each counter must reach its target value
    for counter_idx in range(num_counters):
        # Sum of contributions from all buttons that affect this counter
        contributions = []
        for button_idx, button in enumerate(buttons):
            if counter_idx in button:
                contributions.append(button_presses[button_idx])

        if contributions:
            prob += pulp.lpSum(contributions) == target_joltages[counter_idx]
        elif target_joltages[counter_idx] != 0:
            # No button affects this counter, but target is non-zero
            return None

    # Solve the problem
    # Use PULP_CBC_CMD solver with suppressed output
    prob.solve(pulp.PULP_CBC_CMD(msg=0))

    # Check if solution was found
    if prob.status != pulp.LpStatusOptimal:
        return None

    # Return the total number of button presses
    total_presses = sum(int(var.varValue) for var in button_presses)
    return total_presses


def solve_part2(filepath: str) -> int:
    """Solve the joltage configuration problem for all machines.

    Args:
        filepath: Path to the CSV file containing machine configurations

    Returns:
        Total minimum button presses required for all machines
    """
    total_presses = 0

    with open(filepath, 'r') as f:
        for line in f:
            target_joltages, buttons = parse_machine_part2(line)
            if target_joltages and buttons:
                min_presses = solve_joltage_ilp(target_joltages, buttons)
                if min_presses is not None:
                    total_presses += min_presses
                    print(f"Machine: {target_joltages} -> {min_presses} presses")
                else:
                    print(f"Machine: {target_joltages} -> No solution!")

    return total_presses


if __name__ == "__main__":
    # Test with the example file
    result = solve_part2("10_test.csv")
    print(f"\nTotal minimum button presses (Part 2): {result}")

    # Run on full dataset
    result_full = solve_part2("10.csv")
    print(f"\nTotal minimum button presses for 10.csv (Part 2): {result_full}")
