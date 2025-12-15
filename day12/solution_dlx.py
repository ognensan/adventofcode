from typing import List, Tuple, Dict
from multiprocessing import Pool, cpu_count
import sys


def parse_input(filename: str) -> Tuple[Dict[int, List[str]], List[Tuple[int, int, List[int]]]]:
    """Parse input file - always 6 elements then area definitions."""
    with open(filename, 'r') as f:
        lines = [line.rstrip('\n') for line in f.readlines()]

    elements = {}
    areas = []
    i = 0

    # Read exactly 6 elements (0-5)
    for element_idx in range(6):
        while i < len(lines) and not lines[i].startswith(f"{element_idx}:"):
            i += 1
        if i >= len(lines):
            break
        i += 1
        shape = []
        for _ in range(3):
            if i < len(lines):
                shape.append(lines[i])
                i += 1
        elements[element_idx] = shape

    # Read area definitions
    while i < len(lines):
        line = lines[i]
        if line and 'x' in line and ':' in line:
            parts = line.split(':')
            dimensions = parts[0].strip()
            counts = parts[1].strip()
            dims = dimensions.split('x')
            cols = int(dims[0])
            rows = int(dims[1])
            element_counts = [int(x) for x in counts.split()]
            areas.append((rows, cols, element_counts))
        i += 1

    return elements, areas


def rotate_shape(shape: List[str]) -> List[str]:
    """Rotate a shape 90 degrees clockwise."""
    if not shape:
        return shape
    rows = len(shape)
    cols = len(shape[0])
    rotated = []
    for col in range(cols):
        new_row = ''
        for row in range(rows - 1, -1, -1):
            new_row += shape[row][col]
        rotated.append(new_row)
    return rotated


def get_all_rotations(shape: List[str]) -> List[List[str]]:
    """Get all 4 rotations of a shape."""
    rotations = [shape]
    current = shape
    for _ in range(3):
        current = rotate_shape(current)
        rotations.append(current)
    return rotations


def shape_to_coords(shape: List[str]) -> List[Tuple[int, int]]:
    """Convert a shape to a list of relative coordinates."""
    coords = []
    for r, row in enumerate(shape):
        for c, cell in enumerate(row):
            if cell == '#':
                coords.append((r, c))
    return coords


def normalize_rotation(shape_coords: List[Tuple[int, int]]) -> Tuple[Tuple[int, int], ...]:
    """Normalize shape coordinates to start at (0, 0) and return as sorted tuple."""
    if not shape_coords:
        return tuple()
    min_r = min(r for r, c in shape_coords)
    min_c = min(c for r, c in shape_coords)
    normalized = tuple(sorted((r - min_r, c - min_c) for r, c in shape_coords))
    return normalized


def get_unique_rotations(shape: List[str]) -> List[List[Tuple[int, int]]]:
    """Get unique rotations of a shape (remove duplicates)."""
    all_rotations = get_all_rotations(shape)
    seen = set()
    unique = []
    for rotation in all_rotations:
        coords = shape_to_coords(rotation)
        normalized = normalize_rotation(coords)
        if normalized not in seen:
            seen.add(normalized)
            unique.append(coords)
    return unique


# Dancing Links implementation
class DancingNode:
    """Node in the Dancing Links structure."""
    def __init__(self):
        self.left = self
        self.right = self
        self.up = self
        self.down = self
        self.column = None
        self.row_id = None


class ColumnNode(DancingNode):
    """Column header node."""
    def __init__(self, name):
        super().__init__()
        self.size = 0
        self.name = name
        self.column = self


class DancingLinks:
    """Dancing Links data structure for Algorithm X."""

    def __init__(self, num_primary_cols: int, num_secondary_cols: int = 0):
        self.header = ColumnNode("header")
        self.columns = []
        self.solution = []
        self.num_primary = num_primary_cols

        # Create primary columns (must be covered) - linked to header
        prev = self.header
        for i in range(num_primary_cols):
            col = ColumnNode(f"P{i}")
            col.left = prev
            col.right = prev.right
            prev.right.left = col
            prev.right = col
            self.columns.append(col)
            prev = col

        # Create secondary columns (optional coverage) - NOT linked to header
        self.secondary_start = None
        if num_secondary_cols > 0:
            self.secondary_start = ColumnNode(f"S0")
            self.columns.append(self.secondary_start)
            prev = self.secondary_start

            for i in range(1, num_secondary_cols):
                col = ColumnNode(f"S{i}")
                col.left = prev
                col.right = self.secondary_start
                prev.right = col
                self.secondary_start.left = col
                self.columns.append(col)
                prev = col

    def add_row(self, row_id: int, cols: List[int]):
        """Add a row to the matrix."""
        if not cols:
            return

        first_node = None
        prev_node = None

        for col_idx in cols:
            if col_idx >= len(self.columns):
                continue

            col = self.columns[col_idx]
            node = DancingNode()
            node.column = col
            node.row_id = row_id

            # Link vertically
            node.up = col.up
            node.down = col
            col.up.down = node
            col.up = node
            col.size += 1

            # Link horizontally
            if first_node is None:
                first_node = node
                prev_node = node
            else:
                node.left = prev_node
                node.right = first_node
                prev_node.right = node
                first_node.left = node
                prev_node = node

    def cover(self, col: ColumnNode):
        """Cover a column (remove from header list)."""
        col.right.left = col.left
        col.left.right = col.right

        # Cover all rows that have a 1 in this column
        row = col.down
        while row != col:
            right = row.right
            while right != row:
                right.down.up = right.up
                right.up.down = right.down
                right.column.size -= 1
                right = right.right
            row = row.down

    def uncover(self, col: ColumnNode):
        """Uncover a column (restore to header list)."""
        row = col.up
        while row != col:
            left = row.left
            while left != row:
                left.column.size += 1
                left.down.up = left
                left.up.down = left
                left = left.left
            row = row.up

        col.right.left = col
        col.left.right = col

    def search(self, k: int = 0) -> bool:
        """Algorithm X search with secondary columns."""
        # Check if all primary columns are covered
        if self.header.right == self.header:
            return True

        # Choose column with minimum size (S heuristic) from primary columns only
        col = None
        min_size = float('inf')
        c = self.header.right

        while c != self.header:
            if c.size < min_size:
                min_size = c.size
                col = c
            c = c.right

        if col is None or min_size == 0:
            return False

        self.cover(col)

        row = col.down
        while row != col:
            self.solution.append(row.row_id)

            # Cover all other columns in this row (both primary and secondary)
            right = row.right
            while right != row:
                # Only cover if it's a column that's still in the matrix
                if right.column.name.startswith('P') or right.column.name.startswith('S'):
                    self.cover(right.column)
                right = right.right

            # Recurse
            if self.search(k + 1):
                return True

            # Backtrack
            self.solution.pop()

            # Uncover in reverse order
            left = row.left
            while left != row:
                if left.column.name.startswith('P') or left.column.name.startswith('S'):
                    self.uncover(left.column)
                left = left.left

            row = row.down

        self.uncover(col)
        return False


def solve_area_dlx(rows: int, cols: int, elements_to_place: List[Tuple[int, List[List[str]]]]) -> bool:
    """Solve area using Dancing Links."""
    # Early exit: check total cells needed vs available
    grid_cells = rows * cols
    total_cells_needed = 0

    for element_id, rotations in elements_to_place:
        # Count cells in first rotation (all rotations have same number of cells)
        coords = shape_to_coords(rotations[0])
        total_cells_needed += len(coords)

        # Early exit if already over capacity
        if total_cells_needed > grid_cells:
            return False

    # Calculate unique rotations
    element_rotations_list = []
    for element_id, rotations in elements_to_place:
        unique_rots = get_unique_rotations(rotations[0])
        element_rotations_list.append((element_id, unique_rots))

    # Setup DLX
    num_elements = len(elements_to_place)
    num_cells = rows * cols

    dlx = DancingLinks(num_primary_cols=num_elements, num_secondary_cols=num_cells)

    # Generate all possible placements
    row_id = 0
    for elem_idx, (element_id, unique_rots) in enumerate(element_rotations_list):
        elem_placements = 0
        for rot_coords in unique_rots:
            for start_row in range(rows):
                for start_col in range(cols):
                    # Check if placement is valid
                    cells = []
                    valid = True

                    for dr, dc in rot_coords:
                        r = start_row + dr
                        c = start_col + dc

                        if r < 0 or r >= rows or c < 0 or c >= cols:
                            valid = False
                            break

                        cells.append(r * cols + c)

                    if valid:
                        # Create constraint row
                        constraint_cols = [elem_idx] + [num_elements + cell for cell in cells]
                        dlx.add_row(row_id, constraint_cols)
                        row_id += 1
                        elem_placements += 1

        # If element has no valid placements, impossible to solve
        if elem_placements == 0:
            return False

    # Solve
    return dlx.search()


def process_single_area(args):
    """Process a single area (for parallel execution)."""
    area_idx, area_data, element_rotations, total_areas = args
    rows, cols, element_counts = area_data

    # Build list of elements to place
    elements_to_place = []
    for element_id, count in enumerate(element_counts):
        for _ in range(count):
            if element_id in element_rotations:
                elements_to_place.append((element_id, element_rotations[element_id]))

    # Calculate stats for reporting
    total_cells_needed = sum(len(shape_to_coords(rotations[0])) for _, rotations in elements_to_place)
    grid_cells = rows * cols

    # Estimate DLX matrix size
    est_unique_rots = []
    for element_id, rotations in elements_to_place:
        unique_rots = get_unique_rotations(rotations[0])
        est_unique_rots.append(len(unique_rots))

    max_rows_estimate = sum(ur * rows * cols for ur in est_unique_rots)

    result_msg = f"Processing area {area_idx + 1}/{total_areas}: {rows}x{cols} grid ({grid_cells} cells), {len(elements_to_place)} elements ({total_cells_needed} cells), ~{max_rows_estimate:,} placements... "

    # Try to solve this area
    if total_cells_needed > grid_cells:
        return (False, result_msg + "✗ Too many cells")
    elif solve_area_dlx(rows, cols, elements_to_place):
        return (True, result_msg + "✓ Fits")
    else:
        return (False, result_msg + "✗ Doesn't fit")


def count_fitting_areas(filename: str, num_workers: int = None) -> int:
    """Count how many areas can fit all their required elements."""
    elements, areas = parse_input(filename)

    # Precompute all rotations for each element
    element_rotations = {}
    for element_id, shape in elements.items():
        element_rotations[element_id] = get_all_rotations(shape)

    total_areas = len(areas)
    print(f"Total areas to process: {total_areas}")

    if num_workers is None:
        num_workers = min(cpu_count(), 8)  # Cap at 8 to avoid too much memory usage

    print(f"Using {num_workers} parallel workers")

    # Prepare arguments for parallel processing
    args_list = [(idx, area, element_rotations, total_areas) for idx, area in enumerate(areas)]

    fitting_count = 0

    # Process areas in parallel
    with Pool(processes=num_workers) as pool:
        for result, message in pool.imap_unordered(process_single_area, args_list):
            print(message, flush=True)
            if result:
                fitting_count += 1

    return fitting_count


if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else "12.csv"
    result = count_fitting_areas(filename)
    print(f"\nNumber of areas that can fit all elements: {result}")
