#!/usr/bin/env python3
"""
Part 2: Sort all rectangles by area, then check validity from largest to smallest.
A rectangle with red corners (x1,y1) and (x2,y2) is valid if the other two corners
(x1,y2) and (x2,y1) have red cells beyond them (indicating they're inside the polygon).
"""


def calculate_rectangle_area(p1, p2):
    """Calculate area using inclusive counting."""
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


def point_in_polygon(x, y, polygon):
    """Check if point is inside polygon using ray casting."""
    n = len(polygon)
    inside = False

    p1x, p1y = polygon[0]
    for i in range(1, n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y

    return inside


def is_on_polygon_edge(x, y, polygon):
    """Check if point is on polygon edge."""
    n = len(polygon)
    for i in range(n):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % n]

        if x1 == x2 and x == x1:  # Vertical edge
            if min(y1, y2) <= y <= max(y1, y2):
                return True
        elif y1 == y2 and y == y1:  # Horizontal edge
            if min(x1, x2) <= x <= max(x1, x2):
                return True
    return False


def is_rectangle_valid(x1, y1, x2, y2, red_points_set, polygon):
    """
    Check if rectangle is valid.
    Corners (x1,y1) and (x2,y2) are red.
    Check other 2 corners AND sample points on edges (adaptive sampling).
    """
    x_min, x_max = min(x1, x2), max(x1, x2)
    y_min, y_max = min(y1, y2), max(y1, y2)

    # The two corners we need to check
    corner1 = (x_min, y_max)
    corner2 = (x_max, y_min)

    points_to_check = [corner1, corner2]

    # Adaptive sampling: check every ~1000 units or at least 50 points per edge
    width = x_max - x_min
    height = y_max - y_min

    x_samples = max(50, width // 1000)
    y_samples = max(50, height // 1000)

    # Bottom edge: y=y_min, x varies
    for i in range(1, x_samples):
        x = x_min + width * i // x_samples
        points_to_check.append((x, y_min))

    # Top edge: y=y_max, x varies
    for i in range(1, x_samples):
        x = x_min + width * i // x_samples
        points_to_check.append((x, y_max))

    # Left edge: x=x_min, y varies
    for i in range(1, y_samples):
        y = y_min + height * i // y_samples
        points_to_check.append((x_min, y))

    # Right edge: x=x_max, y varies
    for i in range(1, y_samples):
        y = y_min + height * i // y_samples
        points_to_check.append((x_max, y))

    # Check all points
    for cx, cy in points_to_check:
        if (cx, cy) not in red_points_set:
            if not (is_on_polygon_edge(cx, cy, polygon) or point_in_polygon(cx, cy, polygon)):
                return False

    return True


def find_largest_valid_rectangle(points):
    """Find largest valid rectangle by checking from largest to smallest."""
    red_points_set = set(points)

    # Generate all rectangles sorted by area (largest first)
    print("Generating all rectangles...")
    rectangles = []
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            area = calculate_rectangle_area(points[i], points[j])
            rectangles.append((area, points[i], points[j]))

    rectangles.sort(reverse=True)
    print(f"Generated {len(rectangles)} rectangles")

    # Check validity from largest to smallest
    print("\nChecking validity from largest to smallest...")
    for idx, (area, p1, p2) in enumerate(rectangles):
        print(f"  [{idx}/{len(rectangles)}] Checking area {area} - corners {p1} to {p2}")

        x1, y1 = p1
        x2, y2 = p2

        if is_rectangle_valid(x1, y1, x2, y2, red_points_set, points):
            print(f"  ✓ Found valid rectangle at index {idx}")
            return area, (p1, p2)
        else:
            print("    ✗ Invalid")

    return 0, None


if __name__ == "__main__":
    points = parse_coordinates('9.csv')
    print(f"Total red points: {len(points)}")

    # Find largest valid rectangle
    max_area, best_pair = find_largest_valid_rectangle(points)

    print(f"\n{'='*60}")
    print(f"Largest valid rectangle area: {max_area}")
    if best_pair:
        print(f"Opposite corners: {best_pair[0]} and {best_pair[1]}")
        x1, y1 = best_pair[0]
        x2, y2 = best_pair[1]
        print(f"Width: {abs(x2 - x1) + 1}")
        print(f"Height: {abs(y2 - y1) + 1}")
