import pytest
from solution import parse_graph, count_paths, solve


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


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
