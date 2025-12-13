import pytest
import numpy as np
from solution import parse_machine, solve_lights_gf2, solve


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


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
