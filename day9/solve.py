#!/usr/bin/env python3
"""
Find the largest rectangle area from 9.csv using inclusive counting.
"""


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


if __name__ == "__main__":
    points = parse_coordinates('9.csv')
    print(f"Total red points: {len(points)}")

    max_area, best_pair = find_largest_rectangle(points)

    print(f"\nLargest rectangle area: {max_area}")
    if best_pair:
        print(f"Opposite corners: {best_pair[0]} and {best_pair[1]}")
        x1, y1 = best_pair[0]
        x2, y2 = best_pair[1]
        print(f"Width: {abs(x2 - x1) + 1}")
        print(f"Height: {abs(y2 - y1) + 1}")
