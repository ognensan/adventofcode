import unittest
import math
from solution import (
    read_coordinates,
    euclidean_distance,
    build_clusters,
    get_top_clusters_product,
    solve,
    connect_until_one_cluster
)


class TestEuclideanDistance(unittest.TestCase):
    """Test the euclidean distance calculation."""

    def test_distance_zero(self):
        """Test distance between identical points."""
        p1 = (0, 0, 0)
        p2 = (0, 0, 0)
        self.assertEqual(euclidean_distance(p1, p2), 0.0)

    def test_distance_unit(self):
        """Test distance of 1 along each axis."""
        self.assertAlmostEqual(euclidean_distance((0, 0, 0), (1, 0, 0)), 1.0)
        self.assertAlmostEqual(euclidean_distance((0, 0, 0), (0, 1, 0)), 1.0)
        self.assertAlmostEqual(euclidean_distance((0, 0, 0), (0, 0, 1)), 1.0)

    def test_distance_3d(self):
        """Test distance in 3D space."""
        # Distance from (0,0,0) to (1,1,1) is sqrt(3)
        self.assertAlmostEqual(
            euclidean_distance((0, 0, 0), (1, 1, 1)),
            math.sqrt(3)
        )

    def test_distance_symmetric(self):
        """Test that distance is symmetric."""
        p1 = (162, 817, 812)
        p2 = (425, 690, 689)
        self.assertEqual(
            euclidean_distance(p1, p2),
            euclidean_distance(p2, p1)
        )

    def test_distance_known_points(self):
        """Test distance between known points from the problem."""
        p1 = (162, 817, 812)
        p2 = (425, 690, 689)
        # These should be the closest points
        dist = euclidean_distance(p1, p2)
        self.assertGreater(dist, 0)
        # sqrt((263)^2 + (-127)^2 + (-123)^2)
        # = sqrt(69169 + 16129 + 15129) = sqrt(100427)
        expected = math.sqrt(263**2 + 127**2 + 123**2)
        self.assertAlmostEqual(dist, expected)


class TestReadCoordinates(unittest.TestCase):
    """Test reading coordinates from file."""

    def test_read_test_file(self):
        """Test reading the test file."""
        coords = read_coordinates("8_test.csv")
        self.assertEqual(len(coords), 20)
        self.assertEqual(coords[0], (162, 817, 812))
        self.assertEqual(coords[19], (425, 690, 689))

    def test_coordinate_types(self):
        """Test that coordinates are tuples of integers."""
        coords = read_coordinates("8_test.csv")
        for coord in coords:
            self.assertIsInstance(coord, tuple)
            self.assertEqual(len(coord), 3)
            self.assertIsInstance(coord[0], int)
            self.assertIsInstance(coord[1], int)
            self.assertIsInstance(coord[2], int)


class TestBuildClusters(unittest.TestCase):
    """Test the cluster building function."""

    def test_no_connections(self):
        """Test with no connections - each point is its own cluster."""
        coords = [(0, 0, 0), (1, 1, 1), (2, 2, 2)]
        clusters = build_clusters(coords, num_connections=0)
        self.assertEqual(len(clusters), 3)

    def test_one_connection(self):
        """Test with one connection."""
        coords = [(0, 0, 0), (1, 0, 0), (10, 10, 10)]
        clusters = build_clusters(coords, num_connections=1)
        self.assertEqual(len(clusters), 2)
        # Should connect the two closest points

    def test_all_connections(self):
        """Test connecting all points."""
        coords = [(0, 0, 0), (1, 1, 1), (2, 2, 2)]
        # With 3 points, we need 2 connections to connect all
        clusters = build_clusters(coords, num_connections=2)
        self.assertEqual(len(clusters), 1)
        self.assertEqual(len(clusters[0]), 3)

    def test_ten_connections_test_data(self):
        """Test with 10 connections on the test data."""
        coords = read_coordinates("8_test.csv")
        clusters = build_clusters(coords, num_connections=10)

        # After 10 connections, there should be 11 clusters
        # (20 points - 10 connections + number of separate components)
        self.assertEqual(len(clusters), 11)

        # Get cluster sizes
        sizes = sorted([len(c) for c in clusters], reverse=True)

        # The three longest arrays have lengths 5, 4, and 2
        self.assertEqual(sizes[0], 5)
        self.assertEqual(sizes[1], 4)
        self.assertEqual(sizes[2], 2)

    def test_cluster_point_indices(self):
        """Test that clusters contain valid point indices."""
        coords = read_coordinates("8_test.csv")
        clusters = build_clusters(coords, num_connections=10)

        all_indices = set()
        for cluster in clusters:
            for idx in cluster:
                self.assertGreaterEqual(idx, 0)
                self.assertLess(idx, len(coords))
                all_indices.add(idx)

        # All points should be in exactly one cluster
        self.assertEqual(len(all_indices), len(coords))


class TestGetTopClustersProduct(unittest.TestCase):
    """Test the product calculation function."""

    def test_product_simple(self):
        """Test product with simple cluster sizes."""
        clusters = [{0, 1, 2}, {3, 4}, {5}]
        product = get_top_clusters_product(clusters, top_n=3)
        self.assertEqual(product, 3 * 2 * 1)

    def test_product_top_3(self):
        """Test product of top 3 clusters."""
        clusters = [{0}, {1}, {2, 3}, {4, 5, 6, 7}, {8, 9, 10, 11, 12}]
        product = get_top_clusters_product(clusters, top_n=3)
        self.assertEqual(product, 5 * 4 * 2)

    def test_product_fewer_than_requested(self):
        """Test product when there are fewer clusters than requested."""
        clusters = [{0, 1}, {2, 3}]
        product = get_top_clusters_product(clusters, top_n=5)
        self.assertEqual(product, 2 * 2)

    def test_product_test_data(self):
        """Test product with the test data."""
        coords = read_coordinates("8_test.csv")
        clusters = build_clusters(coords, num_connections=10)
        product = get_top_clusters_product(clusters, top_n=3)
        self.assertEqual(product, 40)


class TestSolve(unittest.TestCase):
    """Test the complete solution."""

    def test_solve_test_data(self):
        """Test the complete solution with test data."""
        result = solve("8_test.csv", num_connections=10, top_n=3)
        self.assertEqual(result, 40)

    def test_solve_different_connections(self):
        """Test solution with different number of connections."""
        # With fewer connections, we should have more clusters
        result_5 = solve("8_test.csv", num_connections=5, top_n=3)
        result_15 = solve("8_test.csv", num_connections=15, top_n=3)

        # Both should return valid results
        self.assertGreater(result_5, 0)
        self.assertGreater(result_15, 0)


class TestClosestPairs(unittest.TestCase):
    """Test that we're identifying the correct closest pairs."""

    def test_closest_pair_is_correct(self):
        """Verify that 162,817,812 and 425,690,689 are the closest."""
        coords = read_coordinates("8_test.csv")

        # Find the closest points
        p1 = (162, 817, 812)
        p2 = (425, 690, 689)

        # Calculate distance between them
        closest_dist = euclidean_distance(p1, p2)

        # Verify this is the minimum distance
        min_dist = float('inf')
        for i in range(len(coords)):
            for j in range(i + 1, len(coords)):
                dist = euclidean_distance(coords[i], coords[j])
                if dist < min_dist:
                    min_dist = dist

        self.assertAlmostEqual(closest_dist, min_dist)

    def test_second_closest_pair(self):
        """Verify second closest pair involves one of first two points."""
        coords = read_coordinates("8_test.csv")

        # Calculate all distances
        distances = []
        for i in range(len(coords)):
            for j in range(i + 1, len(coords)):
                dist = euclidean_distance(coords[i], coords[j])
                distances.append((dist, i, j, coords[i], coords[j]))

        distances.sort()

        # First closest should be 162,817,812 and 425,690,689
        self.assertIn(distances[0][3], [(162, 817, 812), (425, 690, 689)])
        self.assertIn(distances[0][4], [(162, 817, 812), (425, 690, 689)])

        # Second closest should be 162,817,812 and 431,825,988
        second_pair = {distances[1][3], distances[1][4]}
        expected_points = {(162, 817, 812), (431, 825, 988)}
        self.assertEqual(second_pair, expected_points)


class TestConnectUntilOneCluster(unittest.TestCase):
    """Test connecting points until all are in one cluster."""

    def test_three_points(self):
        """Test with three simple points."""
        coords = [(0, 0, 0), (1, 0, 0), (10, 10, 10)]
        product, p1, p2, connections = connect_until_one_cluster(coords)

        # Should make 2 connections to connect 3 points
        self.assertEqual(connections, 2)

        # Product should be valid
        self.assertGreater(product, 0)

        # Last connected points should be from the coordinates
        self.assertIn(p1, coords)
        self.assertIn(p2, coords)

    def test_connections_count(self):
        """Test that n points require n-1 connections."""
        coords = [(i, i, i) for i in range(10)]
        product, p1, p2, connections = connect_until_one_cluster(coords)

        # n points need n-1 connections to form one cluster
        self.assertEqual(connections, len(coords) - 1)

    def test_test_data(self):
        """Test with the test data."""
        coords = read_coordinates("8_test.csv")
        product, p1, p2, connections = connect_until_one_cluster(coords)

        # 20 points should need 19 connections
        self.assertEqual(connections, 19)

        # Verify the result matches expected output
        self.assertEqual(p1, (216, 146, 977))
        self.assertEqual(p2, (117, 168, 530))
        self.assertEqual(product, 25272)

    def test_last_connection_is_longest(self):
        """Test that last connection is among the longest."""
        # Create points in a line with one outlier
        coords = [(i, 0, 0) for i in range(5)] + [(100, 100, 100)]
        product, p1, p2, connections = connect_until_one_cluster(coords)

        # Should connect 6 points with 5 connections
        self.assertEqual(connections, 5)

        # The outlier should be in the last connection
        outlier = (100, 100, 100)
        self.assertTrue(p1 == outlier or p2 == outlier)

    def test_product_calculation(self):
        """Test that product is correctly calculated."""
        coords = [(5, 10, 15), (7, 20, 25)]
        product, p1, p2, connections = connect_until_one_cluster(coords)

        # Only 2 points need 1 connection
        self.assertEqual(connections, 1)

        # Product should be 5 * 7 = 35
        self.assertEqual(product, 5 * 7)


if __name__ == "__main__":
    unittest.main()
