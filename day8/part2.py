from solution import read_coordinates, connect_until_one_cluster


def solve_part2(filepath: str):
    """Solve part 2: Connect all points into one cluster.

    Args:
        filepath: Path to the CSV file containing coordinates
    """
    print(f"Solving Part 2 for {filepath}...")
    print()

    coords = read_coordinates(filepath)
    print(f"Total points: {len(coords)}")
    print()

    print("Connecting points until all are in one cluster...")
    result = connect_until_one_cluster(coords)
    product, point1, point2, connections_made = result

    print(f"Connections made: {connections_made}")
    print()
    print("Last two points connected:")
    print(f"  Point 1: {point1}")
    print(f"  Point 2: {point2}")
    print()
    print(f"Product of X coordinates: {point1[0]} × {point2[0]} = {product}")
    print()

    return product


if __name__ == "__main__":
    print("=" * 60)
    print("PART 2: Connect Until One Cluster")
    print("=" * 60)
    print()

    # Test with test data
    print("Testing with test data:")
    test_result = solve_part2("8_test.csv")
    print("=" * 60)
    print()

    # Run on full dataset
    print("Running on full dataset:")
    full_result = solve_part2("8.csv")
    print("=" * 60)
    print()

    print(f"ANSWER: {full_result}")
