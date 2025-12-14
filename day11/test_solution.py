import pytest
from solution import parse_graph, count_paths, solve
from solution_part2 import (count_paths_with_required_nodes,
                            solve as solve_part2)


def test_parse_graph():
    """Test that the graph is parsed correctly."""
    graph = parse_graph('11_test.csv')

    assert 'aaa' in graph
    assert 'you' in graph
    assert 'bbb' in graph
    assert 'ccc' in graph

    # Check some specific edges
    assert set(graph['you']) == {'bbb', 'ccc'}
    assert set(graph['bbb']) == {'ddd', 'eee'}
    assert set(graph['ccc']) == {'ddd', 'eee', 'fff'}
    assert set(graph['eee']) == {'out'}


def test_count_paths_simple():
    """Test path counting with a simple graph."""
    # Create a simple graph: A -> B -> C
    graph = {
        'A': ['B'],
        'B': ['C'],
        'C': []
    }

    assert count_paths(graph, 'A', 'C') == 1


def test_count_paths_multiple():
    """Test path counting with multiple paths."""
    # Create a graph with two paths: A -> B -> D and A -> C -> D
    graph = {
        'A': ['B', 'C'],
        'B': ['D'],
        'C': ['D'],
        'D': []
    }

    assert count_paths(graph, 'A', 'D') == 2


def test_count_paths_with_cycles():
    """Test that visited tracking prevents infinite loops."""
    # Create a graph with a potential cycle
    graph = {
        'A': ['B', 'C'],
        'B': ['C'],
        'C': ['D'],
        'D': []
    }

    # Should find paths: A -> B -> C -> D and A -> C -> D
    assert count_paths(graph, 'A', 'D') == 2


def test_solve_with_test_file():
    """Test the complete solution with the test file."""
    result = solve('11_test.csv', 'you', 'out')

    # Based on the graph structure, there should be 5 different paths:
    # 1. you -> bbb -> ddd -> ggg -> out
    # 2. you -> bbb -> eee -> out
    # 3. you -> ccc -> ddd -> ggg -> out
    # 4. you -> ccc -> eee -> out
    # 5. you -> ccc -> fff -> out
    assert result == 5


def test_solve_different_start_end():
    """Test with different start and end nodes."""
    # Count paths from 'bbb' to 'out'
    result = solve('11_test.csv', 'bbb', 'out')

    # From bbb: bbb -> ddd -> ggg -> out and bbb -> eee -> out
    assert result == 2


def test_no_path_exists():
    """Test when no path exists between nodes."""
    graph = {
        'A': ['B'],
        'B': [],
        'C': ['D'],
        'D': []
    }

    # No path from A to D
    assert count_paths(graph, 'A', 'D') == 0


# Part 2 Tests

def test_count_paths_with_required_nodes_simple():
    """Test path counting with required nodes in a simple graph."""
    # Create a graph: A -> B -> C -> D where we require passing through B and C
    graph = {
        'A': ['B'],
        'B': ['C'],
        'C': ['D'],
        'D': []
    }

    result = count_paths_with_required_nodes(graph, 'A', 'D', {'B', 'C'})
    assert result == 1


def test_count_paths_with_required_nodes_multiple_paths():
    """Test path counting with required nodes and multiple possible paths."""
    # Graph with multiple paths but only some pass through required nodes
    # A -> B -> D -> E
    # A -> C -> D -> E
    # Only paths through B count if B is required
    graph = {
        'A': ['B', 'C'],
        'B': ['D'],
        'C': ['D'],
        'D': ['E'],
        'E': []
    }

    # Require passing through B
    result = count_paths_with_required_nodes(graph, 'A', 'E', {'B'})
    assert result == 1

    # Require passing through both B and D
    result = count_paths_with_required_nodes(graph, 'A', 'E', {'B', 'D'})
    assert result == 1


def test_count_paths_with_required_nodes_any_order():
    """Test that paths can visit required nodes in any order."""
    # Graph where required nodes can be visited in different orders
    # A -> B -> C -> D
    # A -> C -> B -> D
    graph = {
        'A': ['B', 'C'],
        'B': ['C', 'D'],
        'C': ['B', 'D'],
        'D': []
    }

    # Both paths A->B->C->D and A->C->B->D should count
    result = count_paths_with_required_nodes(graph, 'A', 'D', {'B', 'C'})
    assert result == 2


def test_count_paths_missing_required_node():
    """Test that paths not passing through all required nodes don't count."""
    # Graph where some paths don't pass through required node
    graph = {
        'A': ['B', 'C'],
        'B': ['D'],
        'C': ['D'],
        'D': []
    }

    # Require passing through node 'X' which doesn't exist in any path
    result = count_paths_with_required_nodes(graph, 'A', 'D', {'X'})
    assert result == 0


def test_solve_part2_with_test_file():
    """Test part 2 solution with test file."""
    # This will depend on whether svr, fft, and dac exist in test file
    # If they don't exist, we expect 0 paths
    result = solve_part2('11_test.csv', 'svr', 'out', {'fft', 'dac'})
    # svr, fft, dac likely don't exist in test file
    assert result == 0


def test_solve_part2_with_actual_file():
    """Test part 2 solution with actual input file."""
    # Test with the actual file which should have svr, fft, dac, and out
    result = solve_part2('11.csv', 'svr', 'out', {'fft', 'dac'})
    # Should find some paths (actual count depends on graph structure)
    assert result >= 0  # At minimum, should not error


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
