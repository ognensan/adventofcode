import pytest
import numpy as np
from solution import parse_machine, solve_lights_gf2, solve
from solution_part2 import parse_machine_part2, solve_joltage_ilp, solve_part2


class TestParseMachine:
    """Test the machine configuration parser."""

    def test_parse_first_machine(self):
        """Test parsing the first machine from the example."""
        line = "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}"
        target_state, buttons = parse_machine(line)

        assert target_state == [0, 1, 1, 0]
        assert buttons == [[3], [1, 3], [2], [2, 3], [0, 2], [0, 1]]

    def test_parse_second_machine(self):
        """Test parsing the second machine from the example."""
        line = "[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}"
        target_state, buttons = parse_machine(line)

        assert target_state == [0, 0, 0, 1, 0]
        assert buttons == [[0, 2, 3, 4], [2, 3], [0, 4], [0, 1, 2], [1, 2, 3, 4]]

    def test_parse_third_machine(self):
        """Test parsing the third machine from the example."""
        line = "[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"
        target_state, buttons = parse_machine(line)

        assert target_state == [0, 1, 1, 1, 0, 1]
        assert buttons == [[0, 1, 2, 3, 4], [0, 3, 4], [0, 1, 2, 4, 5], [1, 2]]

    def test_parse_empty_line(self):
        """Test parsing an empty line."""
        line = ""
        target_state, buttons = parse_machine(line)

        assert target_state == []
        assert buttons == []

    def test_parse_all_off(self):
        """Test parsing a configuration with all lights off."""
        line = "[...] (0) (1) (2) {1}"
        target_state, buttons = parse_machine(line)

        assert target_state == [0, 0, 0]
        assert buttons == [[0], [1], [2]]

    def test_parse_all_on(self):
        """Test parsing a configuration with all lights on."""
        line = "[###] (0,1) (1,2) (0,2) {1}"
        target_state, buttons = parse_machine(line)

        assert target_state == [1, 1, 1]
        assert buttons == [[0, 1], [1, 2], [0, 2]]


class TestSolveLightsGF2:
    """Test the GF(2) solver."""

    def test_first_machine(self):
        """Test the first machine from the example.

        [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
        Expected: 2 presses
        """
        target_state = [0, 1, 1, 0]
        buttons = [[3], [1, 3], [2], [2, 3], [0, 2], [0, 1]]

        result = solve_lights_gf2(target_state, buttons)
        assert result == 2

    def test_second_machine(self):
        """Test the second machine from the example.

        [...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
        Expected: 3 presses
        """
        target_state = [0, 0, 0, 1, 0]
        buttons = [[0, 2, 3, 4], [2, 3], [0, 4], [0, 1, 2], [1, 2, 3, 4]]

        result = solve_lights_gf2(target_state, buttons)
        assert result == 3

    def test_third_machine(self):
        """Test the third machine from the example.

        [.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
        Expected: 2 presses
        """
        target_state = [0, 1, 1, 1, 0, 1]
        buttons = [[0, 1, 2, 3, 4], [0, 3, 4], [0, 1, 2, 4, 5], [1, 2]]

        result = solve_lights_gf2(target_state, buttons)
        assert result == 2

    def test_simple_case_one_button(self):
        """Test a simple case with one button."""
        # Target: turn on light 0
        # Button: toggles light 0
        target_state = [1]
        buttons = [[0]]

        result = solve_lights_gf2(target_state, buttons)
        assert result == 1

    def test_simple_case_no_presses(self):
        """Test a case where all lights should stay off."""
        target_state = [0, 0, 0]
        buttons = [[0], [1], [2]]

        result = solve_lights_gf2(target_state, buttons)
        assert result == 0

    def test_impossible_case(self):
        """Test a case with no solution."""
        # Target: turn on light 0
        # Buttons: only toggle light 1
        target_state = [1, 0]
        buttons = [[1]]

        result = solve_lights_gf2(target_state, buttons)
        assert result is None

    def test_two_lights_xor(self):
        """Test XOR-like behavior with two lights."""
        # Target: [1, 0]
        # Button 0: toggles both lights
        # Button 1: toggles light 0
        # Solution: press button 1 once
        target_state = [1, 0]
        buttons = [[0, 1], [0]]

        result = solve_lights_gf2(target_state, buttons)
        assert result == 1

    def test_redundant_buttons(self):
        """Test case with redundant buttons."""
        # Target: [1]
        # Button 0: toggles light 0
        # Button 1: toggles light 0 (redundant)
        # Multiple solutions: press either button once
        target_state = [1]
        buttons = [[0], [0]]

        result = solve_lights_gf2(target_state, buttons)
        assert result == 1


class TestSolve:
    """Test the full solution."""

    def test_example_file(self):
        """Test the example file from the problem description."""
        result = solve("10_test.csv")
        assert result == 7  # 2 + 3 + 2 = 7


class TestManualVerification:
    """Manually verify solutions by simulating button presses."""

    def test_verify_first_machine_solution(self):
        """Verify that pressing buttons (0,2) and (0,1) achieves [.##.]."""
        # Initial state: [0, 0, 0, 0]
        # Press (0,2): toggle lights 0 and 2 -> [1, 0, 1, 0]
        # Press (0,1): toggle lights 0 and 1 -> [0, 1, 1, 0]
        state = [0, 0, 0, 0]

        # Press button (0,2)
        for light in [0, 2]:
            state[light] = 1 - state[light]
        assert state == [1, 0, 1, 0]

        # Press button (0,1)
        for light in [0, 1]:
            state[light] = 1 - state[light]
        assert state == [0, 1, 1, 0]  # Target achieved!

    def test_verify_second_machine_solution(self):
        """Verify that pressing (0,4), (0,1,2), (1,2,3,4) achieves [...#.]."""
        # Initial state: [0, 0, 0, 0, 0]
        # Target: [0, 0, 0, 1, 0]
        state = [0, 0, 0, 0, 0]

        # Press button (0,4)
        for light in [0, 4]:
            state[light] = 1 - state[light]
        assert state == [1, 0, 0, 0, 1]

        # Press button (0,1,2)
        for light in [0, 1, 2]:
            state[light] = 1 - state[light]
        assert state == [0, 1, 1, 0, 1]

        # Press button (1,2,3,4)
        for light in [1, 2, 3, 4]:
            state[light] = 1 - state[light]
        assert state == [0, 0, 0, 1, 0]  # Target achieved!

    def test_verify_third_machine_solution(self):
        """Verify that pressing (0,3,4) and (0,1,2,4,5) achieves [.###.#]."""
        # Initial state: [0, 0, 0, 0, 0, 0]
        # Target: [0, 1, 1, 1, 0, 1]
        state = [0, 0, 0, 0, 0, 0]

        # Press button (0,3,4)
        for light in [0, 3, 4]:
            state[light] = 1 - state[light]
        assert state == [1, 0, 0, 1, 1, 0]

        # Press button (0,1,2,4,5)
        for light in [0, 1, 2, 4, 5]:
            state[light] = 1 - state[light]
        assert state == [0, 1, 1, 1, 0, 1]  # Target achieved!


class TestParseMachinePart2:
    """Test the machine configuration parser for part 2."""

    def test_parse_first_machine_joltages(self):
        """Test parsing joltages from the first machine."""
        line = "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}"
        target_joltages, buttons = parse_machine_part2(line)

        assert target_joltages == [3, 5, 4, 7]
        assert buttons == [[3], [1, 3], [2], [2, 3], [0, 2], [0, 1]]

    def test_parse_second_machine_joltages(self):
        """Test parsing joltages from the second machine."""
        line = "[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}"
        target_joltages, buttons = parse_machine_part2(line)

        assert target_joltages == [7, 5, 12, 7, 2]
        assert buttons == [[0, 2, 3, 4], [2, 3], [0, 4], [0, 1, 2], [1, 2, 3, 4]]

    def test_parse_third_machine_joltages(self):
        """Test parsing joltages from the third machine."""
        line = "[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"
        target_joltages, buttons = parse_machine_part2(line)

        assert target_joltages == [10, 11, 11, 5, 10, 5]
        assert buttons == [[0, 1, 2, 3, 4], [0, 3, 4], [0, 1, 2, 4, 5], [1, 2]]

    def test_parse_empty_line_part2(self):
        """Test parsing an empty line for part 2."""
        line = ""
        target_joltages, buttons = parse_machine_part2(line)

        assert target_joltages == []
        assert buttons == []

    def test_parse_single_value_joltage(self):
        """Test parsing a single joltage value."""
        line = "[.] (0) {5}"
        target_joltages, buttons = parse_machine_part2(line)

        assert target_joltages == [5]
        assert buttons == [[0]]


class TestSolveJoltageILP:
    """Test the ILP solver for joltage configuration."""

    def test_first_machine_part2(self):
        """Test the first machine from part 2.

        Target: {3, 5, 4, 7}
        Buttons: [3], [1,3], [2], [2,3], [0,2], [0,1]
        Expected: 10 presses
        """
        target_joltages = [3, 5, 4, 7]
        buttons = [[3], [1, 3], [2], [2, 3], [0, 2], [0, 1]]

        result = solve_joltage_ilp(target_joltages, buttons)
        assert result == 10

    def test_second_machine_part2(self):
        """Test the second machine from part 2.

        Target: {7, 5, 12, 7, 2}
        Buttons: [0,2,3,4], [2,3], [0,4], [0,1,2], [1,2,3,4]
        Expected: 12 presses
        """
        target_joltages = [7, 5, 12, 7, 2]
        buttons = [[0, 2, 3, 4], [2, 3], [0, 4], [0, 1, 2], [1, 2, 3, 4]]

        result = solve_joltage_ilp(target_joltages, buttons)
        assert result == 12

    def test_third_machine_part2(self):
        """Test the third machine from part 2.

        Target: {10, 11, 11, 5, 10, 5}
        Buttons: [0,1,2,3,4], [0,3,4], [0,1,2,4,5], [1,2]
        Expected: 11 presses
        """
        target_joltages = [10, 11, 11, 5, 10, 5]
        buttons = [[0, 1, 2, 3, 4], [0, 3, 4], [0, 1, 2, 4, 5], [1, 2]]

        result = solve_joltage_ilp(target_joltages, buttons)
        assert result == 11

    def test_simple_case_one_counter(self):
        """Test a simple case with one counter and one button."""
        # Target: counter 0 = 5
        # Button: increments counter 0
        # Solution: press button 5 times
        target_joltages = [5]
        buttons = [[0]]

        result = solve_joltage_ilp(target_joltages, buttons)
        assert result == 5

    def test_simple_case_all_zeros(self):
        """Test a case where all counters should stay at zero."""
        target_joltages = [0, 0, 0]
        buttons = [[0], [1], [2]]

        result = solve_joltage_ilp(target_joltages, buttons)
        assert result == 0

    def test_impossible_case_part2(self):
        """Test a case with no solution."""
        # Target: counter 0 = 5
        # Buttons: only affect counter 1
        target_joltages = [5, 0]
        buttons = [[1]]

        result = solve_joltage_ilp(target_joltages, buttons)
        assert result is None

    def test_two_counters_same_button(self):
        """Test case with one button affecting multiple counters."""
        # Target: [3, 3]
        # Button 0: increments both counters
        # Solution: press button 3 times
        target_joltages = [3, 3]
        buttons = [[0, 1]]

        result = solve_joltage_ilp(target_joltages, buttons)
        assert result == 3

    def test_two_counters_different_targets(self):
        """Test case with different target values."""
        # Target: [2, 5]
        # Button 0: increments counter 0
        # Button 1: increments counter 1
        # Solution: press button 0 twice, button 1 five times = 7 total
        target_joltages = [2, 5]
        buttons = [[0], [1]]

        result = solve_joltage_ilp(target_joltages, buttons)
        assert result == 7

    def test_overlapping_buttons(self):
        """Test case with overlapping button effects."""
        # Target: [3, 2]
        # Button 0: increments both counters
        # Button 1: increments counter 0
        # One solution: press button 0 twice, button 1 once = 3 total
        target_joltages = [3, 2]
        buttons = [[0, 1], [0]]

        result = solve_joltage_ilp(target_joltages, buttons)
        assert result == 3

    def test_redundant_buttons_ilp(self):
        """Test case with redundant buttons."""
        # Target: [5]
        # Button 0: increments counter 0
        # Button 1: increments counter 0 (redundant)
        # Solution: press any combination totaling 5
        target_joltages = [5]
        buttons = [[0], [0]]

        result = solve_joltage_ilp(target_joltages, buttons)
        assert result == 5


class TestSolvePart2:
    """Test the full solution for part 2."""

    def test_example_file_part2(self):
        """Test the example file from part 2."""
        result = solve_part2("10_test.csv")
        assert result == 33  # 10 + 12 + 11 = 33


class TestManualVerificationPart2:
    """Manually verify part 2 solutions by simulating button presses."""

    def test_verify_first_machine_solution_part2(self):
        """Verify solution for first machine in part 2.

        Target: {3, 5, 4, 7}
        Solution: (3) once, (1,3) 3x, (2,3) 3x, (0,2) once, (0,1) 2x = 10 presses
        """
        counters = [0, 0, 0, 0]
        target = [3, 5, 4, 7]

        # Press button (3) once
        counters[3] += 1
        assert counters == [0, 0, 0, 1]

        # Press button (1,3) three times
        for _ in range(3):
            counters[1] += 1
            counters[3] += 1
        assert counters == [0, 3, 0, 4]

        # Press button (2,3) three times
        for _ in range(3):
            counters[2] += 1
            counters[3] += 1
        assert counters == [0, 3, 3, 7]

        # Press button (0,2) once
        counters[0] += 1
        counters[2] += 1
        assert counters == [1, 3, 4, 7]

        # Press button (0,1) twice
        for _ in range(2):
            counters[0] += 1
            counters[1] += 1
        assert counters == [3, 5, 4, 7]
        assert counters == target  # Target achieved!

    def test_verify_second_machine_solution_part2(self):
        """Verify solution for second machine in part 2.

        Target: {7, 5, 12, 7, 2}
        Solution: (0,2,3,4) 2x, (2,3) 5x, (0,1,2) 5x = 12 presses
        """
        counters = [0, 0, 0, 0, 0]
        target = [7, 5, 12, 7, 2]

        # Press button (0,2,3,4) twice
        for _ in range(2):
            counters[0] += 1
            counters[2] += 1
            counters[3] += 1
            counters[4] += 1
        assert counters == [2, 0, 2, 2, 2]

        # Press button (2,3) five times
        for _ in range(5):
            counters[2] += 1
            counters[3] += 1
        assert counters == [2, 0, 7, 7, 2]

        # Press button (0,1,2) five times
        for _ in range(5):
            counters[0] += 1
            counters[1] += 1
            counters[2] += 1
        assert counters == [7, 5, 12, 7, 2]
        assert counters == target  # Target achieved!

    def test_verify_third_machine_solution_part2(self):
        """Verify solution for third machine in part 2.

        Target: {10, 11, 11, 5, 10, 5}
        Solution: (0,1,2,3,4) 5x, (0,1,2,4,5) 5x, (1,2) once = 11 presses
        """
        counters = [0, 0, 0, 0, 0, 0]
        target = [10, 11, 11, 5, 10, 5]

        # Press button (0,1,2,3,4) five times
        for _ in range(5):
            counters[0] += 1
            counters[1] += 1
            counters[2] += 1
            counters[3] += 1
            counters[4] += 1
        assert counters == [5, 5, 5, 5, 5, 0]

        # Press button (0,1,2,4,5) five times
        for _ in range(5):
            counters[0] += 1
            counters[1] += 1
            counters[2] += 1
            counters[4] += 1
            counters[5] += 1
        assert counters == [10, 10, 10, 5, 10, 5]

        # Press button (1,2) once
        counters[1] += 1
        counters[2] += 1
        assert counters == [10, 11, 11, 5, 10, 5]
        assert counters == target  # Target achieved!


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
