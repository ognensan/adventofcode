def parse_graph(filename):
    """Parse the CSV file and build an adjacency list graph."""
    graph = {}

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Split by colon
            if ':' not in line:
                continue

            parts = line.split(':', 1)
            source = parts[0].strip()

            # Get the destinations
            if len(parts) > 1 and parts[1].strip():
                destinations = parts[1].strip().split()
                graph[source] = destinations
            else:
                graph[source] = []

    return graph


def count_paths(graph, start, end, visited=None, depth=0, max_depth=100,
                memo=None):
    """
    Count all different paths from start to end using DFS with memoization.

    Args:
        graph: Adjacency list representation of the graph
        start: Starting node
        end: Ending node
        visited: Set of visited nodes in the current path
        depth: Current recursion depth
        max_depth: Maximum allowed depth
        memo: Memoization cache for (start, end, frozenset(visited))

    Returns:
        Number of different paths from start to end
    """
    if visited is None:
        visited = set()
    if memo is None:
        memo = {}

    # Check for excessive depth
    if depth > max_depth:
        if depth == max_depth + 1:
            print(f"  WARNING: Max depth {max_depth} exceeded at node {start}")
        return 0

    # Base case: reached the destination
    if start == end:
        return 1

    # Check memoization cache
    cache_key = (start, end, frozenset(visited))
    if cache_key in memo:
        return memo[cache_key]

    # Mark current node as visited
    visited.add(start)

    # Count paths through all neighbors
    path_count = 0
    if start in graph:
        for neighbor in graph[start]:
            if neighbor not in visited:
                path_count += count_paths(
                    graph, neighbor, end, visited, depth + 1, max_depth,
                    memo)

    # Backtrack: remove current node from visited set
    visited.remove(start)

    # Cache the result
    memo[cache_key] = path_count
    return path_count


def count_paths_with_required_nodes(graph, start, end, required_nodes):
    """
    Count all different paths from start to end that pass through all
    required nodes.

    Uses optimized DFS with state tracking instead of enumerating all
    permutations. State = (current_node, frozenset of visited required
    nodes)

    Time complexity: O(V * 2^R * E) where V=vertices, R=required nodes,
    E=edges. Much better than O(R! * V * E) for the permutation approach.

    Args:
        graph: Adjacency list representation of the graph
        start: Starting node
        end: Ending node
        required_nodes: Set of nodes that must be visited

    Returns:
        Number of different paths from start to end that pass through
        all required nodes
    """
    required_set = frozenset(required_nodes)
    memo = {}

    def dfs(current, visited_nodes, visited_required):
        """
        DFS with state tracking.

        Args:
            current: Current node
            visited_nodes: Set of all visited nodes in current path
                          (prevents cycles)
            visited_required: Frozenset of visited required nodes

        Returns:
            Number of paths from current to end that visit all remaining
            required nodes
        """
        # Base case: reached destination
        if current == end:
            # Only count if all required nodes have been visited
            return 1 if visited_required == required_set else 0

        # Memoization key: (current node, which required nodes we've
        # visited). Note: We can't include all visited_nodes because that
        # would be too specific. But we track visited_nodes to prevent
        # cycles in the current path
        cache_key = (current, visited_required)
        if cache_key in memo:
            return memo[cache_key]

        # Mark current as visited
        visited_nodes.add(current)

        # Update visited required nodes if current is a required node
        new_visited_required = visited_required
        if current in required_set:
            new_visited_required = visited_required | {current}

        # Explore all neighbors
        path_count = 0
        if current in graph:
            for neighbor in graph[current]:
                if neighbor not in visited_nodes:
                    path_count += dfs(
                        neighbor, visited_nodes, new_visited_required)

        # Backtrack
        visited_nodes.remove(current)

        # Cache and return
        memo[cache_key] = path_count
        return path_count

    result = dfs(start, set(), frozenset())
    print(f"\nTotal paths from '{start}' to '{end}' passing through "
          f"{required_nodes}: {result}")
    return result


def solve(filename, start='svr', end='out', required_nodes=None):
    """
    Solve the path counting problem with required nodes.

    Args:
        filename: Path to the input CSV file
        start: Starting element (default: 'svr')
        end: Ending element (default: 'out')
        required_nodes: Set of nodes that must be visited
                       (default: {'fft', 'dac'})

    Returns:
        Number of different paths from start to end that pass through
        all required nodes
    """
    if required_nodes is None:
        required_nodes = {'fft', 'dac'}

    graph = parse_graph(filename)
    return count_paths_with_required_nodes(graph, start, end, required_nodes)


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: python solution_part2.py <input_file> [start] [end] "
              "[required_node1] [required_node2] ...")
        sys.exit(1)

    filename = sys.argv[1]
    start = sys.argv[2] if len(sys.argv) > 2 else 'svr'
    end = sys.argv[3] if len(sys.argv) > 3 else 'out'

    # Get required nodes from command line or use defaults
    if len(sys.argv) > 4:
        required_nodes = set(sys.argv[4:])
    else:
        required_nodes = {'fft', 'dac'}

    result = solve(filename, start, end, required_nodes)
    print(f"Number of different paths from '{start}' to '{end}' passing "
          f"through {required_nodes}: {result}")
