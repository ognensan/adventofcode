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


def count_paths(graph, start, end, visited=None):
    """
    Count all different paths from start to end using DFS.

    Args:
        graph: Adjacency list representation of the graph
        start: Starting node
        end: Ending node
        visited: Set of visited nodes in the current path

    Returns:
        Number of different paths from start to end
    """
    if visited is None:
        visited = set()

    # Base case: reached the destination
    if start == end:
        return 1

    # Mark current node as visited
    visited.add(start)

    # Count paths through all neighbors
    path_count = 0
    if start in graph:
        for neighbor in graph[start]:
            if neighbor not in visited:
                path_count += count_paths(graph, neighbor, end, visited)

    # Backtrack: remove current node from visited set
    visited.remove(start)

    return path_count


def solve(filename, start='you', end='out'):
    """
    Solve the path counting problem.

    Args:
        filename: Path to the input CSV file
        start: Starting element (default: 'you')
        end: Ending element (default: 'out')

    Returns:
        Number of different paths from start to end
    """
    graph = parse_graph(filename)
    return count_paths(graph, start, end)


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: python solution.py <input_file> [start] [end]")
        sys.exit(1)

    filename = sys.argv[1]
    start = sys.argv[2] if len(sys.argv) > 2 else 'you'
    end = sys.argv[3] if len(sys.argv) > 3 else 'out'

    result = solve(filename, start, end)
    print(f"Number of different paths from '{start}' to '{end}': {result}")
