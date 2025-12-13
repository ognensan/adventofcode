#!/usr/bin/env python3
"""
Unit tests for rectangle area calculation.
"""

import unittest


def calculate_rectangle_area(p1, p2):
    """
    Calculate the area of a rectangle formed by two points as opposite corners.
    Uses inclusive counting: (|x2-x1|+1) * (|y2-y1|+1)
    """
    x1, y1 = p1
    x2, y2 = p2
    width = abs(x2 - x1) + 1
    height = abs(y2 - y1) + 1
    return width * height


def parse_coordinates(filename):
    """Parse coordinates from CSV file."""
    points = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            coords = line.split(',')
            if len(coords) == 2:
                x, y = int(coords[0]), int(coords[1])
                points.append((x, y))
    return points


def find_largest_rectangle(points):
    """Find the largest rectangle area from all pairs of points."""
    max_area = 0
    best_pair = None

    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            area = calculate_rectangle_area(points[i], points[j])
            if area > max_area:
                max_area = area
                best_pair = (points[i], points[j])

    return max_area, best_pair


class TestRectangleArea(unittest.TestCase):
    """Test cases for rectangle area calculation."""

    def test_largest_area(self):
        """Test that (2,5) and (11,1) gives area 50."""
        area = calculate_rectangle_area((2, 5), (11, 1))
        self.assertEqual(area, 50)

    def test_area_case_1(self):
        """Test that (7,3) and (2,3) gives area 6."""
        area = calculate_rectangle_area((7, 3), (2, 3))
        self.assertEqual(area, 6)

    def test_area_case_2(self):
        """Test that (7,1) and (11,7) gives area 35."""
        area = calculate_rectangle_area((7, 1), (11, 7))
        self.assertEqual(area, 35)

    def test_area_case_3(self):
        """Test that (2,5) and (9,7) gives area 24."""
        area = calculate_rectangle_area((2, 5), (9, 7))
        self.assertEqual(area, 24)

    def test_max_area_from_test_data(self):
        """Test that the maximum area from all point combinations is 50."""
        points = parse_coordinates('9_test.csv')
        max_area, best_pair = find_largest_rectangle(points)
        self.assertEqual(max_area, 50)
        # Verify it's the expected pair
        self.assertIn((2, 5), best_pair)
        self.assertIn((11, 1), best_pair)

    def test_order_independence(self):
        """Test that point order doesn't matter."""
        area1 = calculate_rectangle_area((2, 5), (11, 1))
        area2 = calculate_rectangle_area((11, 1), (2, 5))
        self.assertEqual(area1, area2)

    def test_single_cell(self):
        """Test a 1x1 rectangle (same point)."""
        area = calculate_rectangle_area((5, 5), (5, 5))
        self.assertEqual(area, 1)

    def test_horizontal_line(self):
        """Test a horizontal line (height=1)."""
        area = calculate_rectangle_area((1, 3), (5, 3))
        self.assertEqual(area, 5)

    def test_vertical_line(self):
        """Test a vertical line (width=1)."""
        area = calculate_rectangle_area((3, 1), (3, 5))
        self.assertEqual(area, 5)


if __name__ == '__main__':
    unittest.main()
