# Day 8: Point Clustering by Distance

## Problem Description

Given a set of 3D coordinates, find clusters by connecting the closest pairs of points. The algorithm:

1. Calculate euclidean distances between all pairs of points
2. Sort pairs by distance (closest first)
3. Make N connections by iterating through sorted pairs:
   - If both points are already in the same cluster, skip
   - If one point is in a cluster, add the other to that cluster
   - If both points are in different clusters, merge them
   - If neither is in a cluster, create a new cluster
4. After N connections, calculate the product of the top 3 largest cluster sizes

## Example with Test Data

With the test data (20 points) and 10 connections:
- **Closest pair**: (162,817,812) and (425,690,689)
- **Second closest**: (162,817,812) and (431,825,988) - extends first cluster
- **Third closest**: (906,360,560) and (805,96,715) - forms new cluster
- **Fourth closest**: (431,825,988) and (425,690,689) - already in same cluster, skip

After 10 connections:
- **11 clusters** are formed
- **Top 3 sizes**: 5, 4, 2
- **Product**: 5 × 4 × 2 = 40

## Solution Structure

### Functions

- `read_coordinates(filepath)`: Parse CSV file into list of 3D coordinate tuples
- `euclidean_distance(p1, p2)`: Calculate 3D euclidean distance
- `build_clusters(coordinates, num_connections)`: Build clusters using Union-Find
- `get_top_clusters_product(clusters, top_n)`: Calculate product of top N cluster sizes
- `solve(filepath, num_connections, top_n)`: Complete solution pipeline

### Algorithm: Union-Find

The solution uses a Union-Find (Disjoint Set Union) data structure for efficient cluster management:

```python
# Each point starts in its own cluster
parent = list(range(n))

# Find operation with path compression
def find(x):
    if parent[x] != x:
        parent[x] = find(parent[x])
    return parent[x]

# Union operation merges clusters
def union(x, y):
    root_x = find(x)
    root_y = find(y)
    if root_x != root_y:
        parent[root_x] = root_y
        return True
    return False
```

**Time Complexity**: O(n² log n) for sorting distances, O(α(n)) per union/find operation where α is inverse Ackermann function (practically constant)

## Running the Solution

### Test Data (8_test.csv)

```bash
# Run the main solution on test data
python solution.py

# Run all unit tests
python test_solution.py -v
```

### Full Dataset (8.csv)

```bash
# Run on full dataset with 1000 connections
python run_full.py
```

**Expected output:**
```
Running solution on full dataset (8.csv) with 1000 connections...

Total points in dataset: 1000

Making 1000 connections...
Number of clusters formed: 294

Top 10 cluster sizes: [54, 51, 45, 44, 29, 24, 23, 19, 18, 17]

Top 3 cluster sizes: 54, 51, 45
Product of top 3 cluster sizes: 123930
```

**Answer**: 54 × 51 × 45 = **123,930**

To change the number of connections, edit the `num_connections` variable in `run_full.py`.

## Part 2: Connect Until One Cluster

In Part 2, we extend the problem to connect all points until they form a single cluster. The goal is to find the last two points that were connected and multiply their X coordinates.

### Algorithm

Continue making connections in order of distance (closest first) until all points are in one cluster. To connect N points into one cluster, we need exactly N-1 connections.

### Running Part 2

```bash
# Run Part 2 on both test and full datasets
python part2.py
```

### Results

**Test Data (8_test.csv):**
- Total points: 20
- Connections made: 19
- Last connected points: (216, 146, 977) and (117, 168, 530)
- Product: 216 × 117 = **25,272**

**Full Dataset (8.csv):**
- Total points: 1,000
- Connections made: 999
- Last connected points: (2496, 83742, 96522) and (10953, 95468, 87128)
- **Answer**: 2496 × 10953 = **27,338,688**

### Key Insight

The last connection represents the two clusters that were furthest apart. These are typically outlier points or points from well-separated regions of the space.

## Test Coverage

The test suite includes:
- **Euclidean distance tests**: Zero distance, unit distances, 3D distances, symmetry
- **File reading tests**: Parsing CSV, coordinate types
- **Clustering tests**: Various connection counts, cluster validation
- **Product calculation tests**: Different cluster sizes, edge cases
- **Integration tests**: Complete solution with test data
- **Verification tests**: Confirms closest pairs match expected values
- **Part 2 tests**: Connect until one cluster, connection counts, last connection validation

All 25 tests pass successfully.
