import math
from typing import List, Tuple, Set
from collections import defaultdict


def read_coordinates(filepath: str) -> List[Tuple[int, int, int]]:
    """Read 3D coordinates from a CSV file.

    Args:
        filepath: Path to the CSV file containing coordinates

    Returns:
        List of tuples representing (x, y, z) coordinates
    """
    coordinates = []
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if line:  # Skip empty lines
                parts = line.split(',')
                if len(parts) == 3:
                    x, y, z = int(parts[0]), int(parts[1]), int(parts[2])
                    coordinates.append((x, y, z))
    return coordinates


def euclidean_distance(
    p1: Tuple[int, int, int],
    p2: Tuple[int, int, int]
) -> float:
    """Calculate euclidean distance between two 3D points.

    Args:
        p1: First point (x, y, z)
        p2: Second point (x, y, z)

    Returns:
        Euclidean distance between the two points
    """
    dx = (p1[0] - p2[0]) ** 2
    dy = (p1[1] - p2[1]) ** 2
    dz = (p1[2] - p2[2]) ** 2
    return math.sqrt(dx + dy + dz)


def build_clusters(
    coordinates: List[Tuple[int, int, int]],
    num_connections: int
) -> List[Set[int]]:
    """Build clusters by connecting the closest points.

    Args:
        coordinates: List of 3D coordinates
        num_connections: Number of shortest connections to make

    Returns:
        List of sets, where each set contains indices of points in a cluster
    """
    n = len(coordinates)

    # Calculate all pairwise distances
    distances = []
    for i in range(n):
        for j in range(i + 1, n):
            dist = euclidean_distance(coordinates[i], coordinates[j])
            distances.append((dist, i, j))

    # Sort by distance
    distances.sort()

    # Union-Find data structure to track clusters
    parent = list(range(n))

    def find(x):
        """Find the root of the cluster containing x."""
        if parent[x] != x:
            parent[x] = find(parent[x])  # Path compression
        return parent[x]

    def union(x, y):
        """Merge the clusters containing x and y."""
        root_x = find(x)
        root_y = find(y)
        if root_x != root_y:
            parent[root_x] = root_y
            return True
        return False

    # Make the specified number of connections
    connections_made = 0
    for dist, i, j in distances:
        if connections_made >= num_connections:
            break
        union(i, j)
        connections_made += 1

    # Build clusters from the union-find structure
    cluster_map = defaultdict(set)
    for i in range(n):
        root = find(i)
        cluster_map[root].add(i)

    return list(cluster_map.values())


def get_top_clusters_product(clusters: List[Set[int]], top_n: int = 3) -> int:
    """Get the product of the sizes of the top N largest clusters.

    Args:
        clusters: List of clusters (sets of point indices)
        top_n: Number of top clusters to consider

    Returns:
        Product of the sizes of the top N largest clusters
    """
    sizes = sorted([len(cluster) for cluster in clusters], reverse=True)
    product = 1
    for i in range(min(top_n, len(sizes))):
        product *= sizes[i]
    return product


def connect_until_one_cluster(
    coordinates: List[Tuple[int, int, int]]
) -> Tuple[int, Tuple[int, int, int], Tuple[int, int, int], int]:
    """Connect points until all are in one cluster.

    Args:
        coordinates: List of 3D coordinates

    Returns:
        Tuple of (product_of_x_coords, point1, point2) where point1 and point2
        are the last two points connected
    """
    n = len(coordinates)

    # Calculate all pairwise distances
    distances = []
    for i in range(n):
        for j in range(i + 1, n):
            dist = euclidean_distance(coordinates[i], coordinates[j])
            distances.append((dist, i, j))

    # Sort by distance
    distances.sort()

    # Union-Find data structure to track clusters
    parent = list(range(n))

    def find(x):
        """Find the root of the cluster containing x."""
        if parent[x] != x:
            parent[x] = find(parent[x])  # Path compression
        return parent[x]

    def union(x, y):
        """Merge the clusters containing x and y."""
        root_x = find(x)
        root_y = find(y)
        if root_x != root_y:
            parent[root_x] = root_y
            return True
        return False

    def count_clusters():
        """Count the number of distinct clusters."""
        roots = set()
        for i in range(n):
            roots.add(find(i))
        return len(roots)

    # Keep connecting until we have one cluster
    last_i, last_j = None, None
    connections_made = 0

    for dist, i, j in distances:
        if union(i, j):
            connections_made += 1
            last_i, last_j = i, j

            # Check if we're down to one cluster
            if count_clusters() == 1:
                break

    # Get the last connected points
    point1 = coordinates[last_i]
    point2 = coordinates[last_j]

    # Calculate product of X coordinates
    product = point1[0] * point2[0]

    return product, point1, point2, connections_made


def solve(filepath: str, num_connections: int, top_n: int = 3) -> int:
    """Solve the clustering problem.

    Args:
        filepath: Path to the CSV file containing coordinates
        num_connections: Number of shortest connections to make
        top_n: Number of top clusters to consider for product

    Returns:
        Product of the sizes of the top N largest clusters
    """
    coordinates = read_coordinates(filepath)
    clusters = build_clusters(coordinates, num_connections)
    return get_top_clusters_product(clusters, top_n)


if __name__ == "__main__":
    # Test with the example file
    result = solve("8_test.csv", num_connections=10, top_n=3)
    print(f"Product of top 3 cluster sizes (10 connections): {result}")
    test_coords = read_coordinates('8_test.csv')
    test_clusters = build_clusters(test_coords, 10)
    print(f"Number of clusters: {len(test_clusters)}")

    # Show cluster details
    coords = read_coordinates("8_test.csv")
    clusters = build_clusters(coords, 10)
    sizes = sorted([len(c) for c in clusters], reverse=True)
    print(f"Cluster sizes: {sizes}")
    print(f"Top 3 sizes: {sizes[:3]}")
