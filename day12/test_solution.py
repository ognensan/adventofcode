import pytest
from solution_dlx import (
    parse_input,
    rotate_shape,
    get_all_rotations,
    shape_to_coords,
    normalize_rotation,
    get_unique_rotations,
    solve_area_dlx,
    count_fitting_areas
)


def test_parse_input():
    """Test parsing the input file."""
    elements, areas = parse_input("12_test.csv")

    # Check that we have 6 elements
    assert len(elements) == 6

    # Check element 0
    assert 0 in elements
    assert elements[0] == ["###", "##.", "##."]

    # Check element 4
    assert 4 in elements
    assert elements[4] == ["###", "#..", "###"]

    # Check that we have 3 areas
    assert len(areas) == 3

    # Check first area: 4x4 with 2 elements of type 4
    assert areas[0] == (4, 4, [0, 0, 0, 0, 2, 0])

    # Check second area: 12x5
    assert areas[1] == (5, 12, [1, 0, 1, 0, 2, 2])

    # Check third area: 12x5
    assert areas[2] == (5, 12, [1, 0, 1, 0, 3, 2])


def test_rotate_shape():
    """Test rotating a shape 90 degrees clockwise."""
    shape = ["##", "#."]

    # Rotate once (90° clockwise)
    rotated = rotate_shape(shape)
    assert rotated == ["##", ".#"]

    # Rotate again (180°)
    rotated2 = rotate_shape(rotated)
    assert rotated2 == [".#", "##"]

    # Rotate again (270°)
    rotated3 = rotate_shape(rotated2)
    assert rotated3 == ["#.", "##"]

    # Rotate one more time (360° - back to original)
    rotated4 = rotate_shape(rotated3)
    assert rotated4 == shape


def test_get_all_rotations():
    """Test getting all 4 rotations of a shape."""
    shape = ["##", "#."]
    rotations = get_all_rotations(shape)

    assert len(rotations) == 4
    assert rotations[0] == ["##", "#."]
    assert rotations[1] == ["##", ".#"]
    assert rotations[2] == [".#", "##"]
    assert rotations[3] == ["#.", "##"]


def test_shape_to_coords():
    """Test converting a shape to coordinates."""
    shape = ["###", "##.", "##."]
    coords = shape_to_coords(shape)

    expected = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (2, 0), (2, 1)]
    assert sorted(coords) == sorted(expected)


def test_solve_area_simple():
    """Test solving a simple area with one element."""
    # Create a 3x3 area and try to place a 2x2 square
    element_rotations = [[["##", "##"]]]
    elements_to_place = [(0, element_rotations[0])]

    result = solve_area_dlx(3, 3, elements_to_place)
    assert result is True


def test_solve_area_no_fit():
    """Test an area where elements don't fit."""
    # Try to place a 3x3 element in a 2x2 area
    element_rotations = [[["###", "###", "###"]]]
    elements_to_place = [(0, element_rotations[0])]

    result = solve_area_dlx(2, 2, elements_to_place)
    assert result is False


def test_count_fitting_areas():
    """Test the main function with the test file."""
    result = count_fitting_areas("12_test.csv")

    # According to the problem, the first two areas can fit all elements,
    # but the third one cannot
    assert result == 2


def test_element_shapes():
    """Test that element shapes are parsed correctly."""
    elements, _ = parse_input("12_test.csv")

    # Element 0: L-shape
    assert elements[0] == ["###", "##.", "##."]

    # Element 1: Different L-shape
    assert elements[1] == ["###", "##.", ".##"]

    # Element 2: Another variant
    assert elements[2] == [".##", "###", "##."]

    # Element 3: T-shape
    assert elements[3] == ["##.", "###", "##."]

    # Element 4: Plus-like shape
    assert elements[4] == ["###", "#..", "###"]

    # Element 5: Cross shape
    assert elements[5] == ["###", ".#.", "###"]


def test_normalize_rotation():
    """Test normalizing shape coordinates."""
    coords = [(1, 1), (1, 2), (2, 1)]
    normalized = normalize_rotation(coords)
    # Should start at (0, 0)
    assert normalized == ((0, 0), (0, 1), (1, 0))


def test_get_unique_rotations():
    """Test getting unique rotations (removes duplicates)."""
    # A square has only 1 unique rotation
    square = ["##", "##"]
    unique = get_unique_rotations(square)
    assert len(unique) == 1

    # An L-shape should have up to 4 unique rotations
    l_shape = ["##", "#."]
    unique = get_unique_rotations(l_shape)
    assert len(unique) == 4


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
