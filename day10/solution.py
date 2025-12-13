import re
from typing import List, Tuple, Optional
import numpy as np


def parse_machine(line: str) -> Tuple[List[int], List[List[int]]]:
    """Parse a machine configuration line.

    Args:
        line: A line from the CSV file

    Returns:
        Tuple of (target_state, buttons) where:
        - target_state is a list of 0s and 1s (. = 0, # = 1)
        - buttons is a list of button configurations, each a list of light indices
    """
    line = line.strip()
    if not line:
        return [], []

    # Extract the target state [.##.]
    target_match = re.search(r'\[([.#]+)\]', line)
    if not target_match:
        return [], []

    target_str = target_match.group(1)
    target_state = [1 if c == '#' else 0 for c in target_str]

    # Extract button configurations (0,1,2) (3,4) etc.
    button_pattern = r'\(([0-9,]+)\)'
    button_matches = re.findall(button_pattern, line)

    buttons = []
    for button_str in button_matches:
        indices = [int(x) for x in button_str.split(',')]
        buttons.append(indices)

    return target_state, buttons


def solve_lights_gf2(target_state: List[int], buttons: List[List[int]]) -> Optional[int]:
    """Solve the lights problem over GF(2) to find minimum button presses.

    This creates a system of linear equations over GF(2) (binary field) where:
    - Each row represents a light
    - Each column represents a button
    - Entry (i,j) is 1 if button j toggles light i

    We need to find the solution x (which buttons to press) such that:
    A * x = b (mod 2)
    where A is the button matrix, x is button presses, and b is target state.

    Args:
        target_state: List of target light states (0 or 1)
        buttons: List of button configurations

    Returns:
        Minimum number of button presses, or None if no solution exists
    """
    if not target_state or not buttons:
        return 0

    num_lights = len(target_state)
    num_buttons = len(buttons)

    # Create the button matrix (lights x buttons)
    matrix = np.zeros((num_lights, num_buttons), dtype=int)

    for button_idx, button in enumerate(buttons):
        for light_idx in button:
            if light_idx < num_lights:
                matrix[light_idx, button_idx] = 1

    # Create augmented matrix [A | b]
    augmented = np.column_stack((matrix, target_state))

    # Gaussian elimination over GF(2)
    augmented = augmented.copy()
    rows, cols = augmented.shape

    pivot_row = 0
    pivot_cols = []  # Track which columns have pivots

    for col in range(num_buttons):
        # Find pivot
        found_pivot = False
        for row in range(pivot_row, num_lights):
            if augmented[row, col] == 1:
                # Swap rows
                augmented[[pivot_row, row]] = augmented[[row, pivot_row]]
                found_pivot = True
                break

        if not found_pivot:
            continue

        pivot_cols.append(col)

        # Eliminate other rows
        for row in range(num_lights):
            if row != pivot_row and augmented[row, col] == 1:
                augmented[row] = (augmented[row] + augmented[pivot_row]) % 2

        pivot_row += 1

    # Check for inconsistency (row with all zeros except last column)
    for row in range(num_lights):
        if np.all(augmented[row, :num_buttons] == 0) and augmented[row, num_buttons] == 1:
            return None  # No solution

    # Find all free variables (columns without pivots)
    free_vars = [i for i in range(num_buttons) if i not in pivot_cols]

    # If no free variables, we have a unique solution
    if not free_vars:
        # Extract the solution from augmented matrix
        solution = np.zeros(num_buttons, dtype=int)
        for i, col in enumerate(pivot_cols):
            if i < len(pivot_cols):
                solution[col] = augmented[i, num_buttons]
        return int(np.sum(solution))

    # Try all combinations of free variables to find minimum
    min_presses = float('inf')

    for mask in range(1 << len(free_vars)):
        solution = np.zeros(num_buttons, dtype=int)

        # Set free variables based on mask
        for i, var in enumerate(free_vars):
            solution[var] = (mask >> i) & 1

        # Back-substitute to find pivot variables
        for i in range(len(pivot_cols) - 1, -1, -1):
            col = pivot_cols[i]
            # solution[col] = augmented[i, num_buttons] - sum of (augmented[i, j] * solution[j] for j != col)
            val = augmented[i, num_buttons]
            for j in range(num_buttons):
                if j != col:
                    val = (val - augmented[i, j] * solution[j]) % 2
            solution[col] = val % 2

        # Verify solution
        result = np.dot(matrix, solution) % 2
        if np.array_equal(result, target_state):
            presses = int(np.sum(solution))
            min_presses = min(min_presses, presses)

    return min_presses if min_presses != float('inf') else None


def solve(filepath: str) -> int:
    """Solve the machine configuration problem.

    Args:
        filepath: Path to the CSV file containing machine configurations

    Returns:
        Total minimum button presses required for all machines
    """
    total_presses = 0

    with open(filepath, 'r') as f:
        for line in f:
            target_state, buttons = parse_machine(line)
            if target_state and buttons:
                min_presses = solve_lights_gf2(target_state, buttons)
                if min_presses is not None:
                    total_presses += min_presses
                    print(f"Machine: {target_state} -> {min_presses} presses")
                else:
                    print(f"Machine: {target_state} -> No solution!")

    return total_presses


if __name__ == "__main__":
    # Test with the example file
    result = solve("10.csv")
    print(f"\nTotal minimum button presses: {result}")
