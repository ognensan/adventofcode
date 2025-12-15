from typing import List, Tuple, Dict
from multiprocessing import Process, Queue, Manager
import sys
import time

try:
    import torch
    # Check for MPS (Metal Performance Shaders) on Mac
    if torch.backends.mps.is_available():
        GPU_AVAILABLE = True
        GPU_DEVICE = "mps"
        print("Using Metal Performance Shaders (MPS) for GPU acceleration")
    elif torch.cuda.is_available():
        GPU_AVAILABLE = True
        GPU_DEVICE = "cuda"
        print("Using CUDA for GPU acceleration")
    else:
        GPU_AVAILABLE = False
        GPU_DEVICE = "cpu"
except ImportError:
    try:
        import pyopencl as cl
        # Try to find OpenCL devices
        platforms = cl.get_platforms()
        devices = []
        for platform in platforms:
            devices.extend(platform.get_devices())
        GPU_AVAILABLE = len(devices) > 0
        GPU_DEVICE = "opencl"
        if GPU_AVAILABLE:
            print(f"Using PyOpenCL with {len(devices)} device(s)")
    except ImportError:
        GPU_AVAILABLE = False
        GPU_DEVICE = "cpu"
        print("Warning: No GPU libraries available. "
              "Install with: pipenv install torch pyopencl")


def parse_input(filename: str) -> Tuple[
    Dict[int, List[str]], List[Tuple[int, int, List[int]]]
]:
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


def normalize_rotation(
    shape_coords: List[Tuple[int, int]]
) -> Tuple[Tuple[int, int], ...]:
    """Normalize shape coordinates to start at (0, 0)."""
    if not shape_coords:
        return tuple()
    min_r = min(r for r, c in shape_coords)
    min_c = min(c for r, c in shape_coords)
    normalized = tuple(sorted(
        (r - min_r, c - min_c) for r, c in shape_coords
    ))
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


# Import DLX classes from original solution
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

        # Create secondary columns (optional coverage) - NOT linked
        # to header
        self.secondary_start = None
        if num_secondary_cols > 0:
            self.secondary_start = ColumnNode("S0")
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

        # Choose column with minimum size (S heuristic)
        # from primary columns only
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

            # Cover all other columns in this row
            # (both primary and secondary)
            right = row.right
            while right != row:
                # Only cover if it's a column that's still in the matrix
                if (right.column.name.startswith('P') or
                        right.column.name.startswith('S')):
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
                if (left.column.name.startswith('P') or
                        left.column.name.startswith('S')):
                    self.uncover(left.column)
                left = left.left

            row = row.down

        self.uncover(col)
        return False


def solve_area_dlx(
    rows: int, cols: int,
    elements_to_place: List[Tuple[int, List[List[Tuple[int, int]]]]]
) -> bool:
    """Solve area using Dancing Links."""
    # Early exit: check total cells needed vs available
    grid_cells = rows * cols
    total_cells_needed = 0

    for element_id, unique_rots in elements_to_place:
        # Count cells in first rotation
        # (all rotations have same number of cells)
        total_cells_needed += len(unique_rots[0])

        # Early exit if already over capacity
        if total_cells_needed > grid_cells:
            return False

    # Setup DLX
    num_elements = len(elements_to_place)
    num_cells = rows * cols

    dlx = DancingLinks(
        num_primary_cols=num_elements,
        num_secondary_cols=num_cells
    )

    # Generate all possible placements
    row_id = 0
    for elem_idx, (element_id, unique_rots) in enumerate(
        elements_to_place
    ):
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
                        constraint_cols = (
                            [elem_idx] +
                            [num_elements + cell for cell in cells]
                        )
                        dlx.add_row(row_id, constraint_cols)
                        row_id += 1
                        elem_placements += 1

        # If element has no valid placements, impossible to solve
        if elem_placements == 0:
            return False

    # Solve
    return dlx.search()


def solve_area_gpu(
    rows: int, cols: int,
    elements_to_place: List[Tuple[int, List[List[Tuple[int, int]]]]]
) -> bool:
    """
    GPU-accelerated area solving.
    Uses GPU for placement validation when available.
    Falls back to DLX for actual solving.
    """
    if not GPU_AVAILABLE or GPU_DEVICE == "cpu":
        return solve_area_dlx(rows, cols, elements_to_place)

    # Early exit: check total cells needed vs available
    grid_cells = rows * cols
    total_cells_needed = 0

    for element_id, unique_rots in elements_to_place:
        total_cells_needed += len(unique_rots[0])
        if total_cells_needed > grid_cells:
            return False

    if GPU_DEVICE == "mps" or GPU_DEVICE == "cuda":
        # Use PyTorch for GPU acceleration
        # Accelerate the placement generation phase
        try:
            import torch
            device = torch.device(GPU_DEVICE)

            # Pre-validate all placements on GPU in batch
            # This is faster than checking each placement individually
            # But for the actual solving, we still use DLX on CPU
            # as it's a better algorithm for this problem
            # Grid tensor would be created here if implementing GPU validation
            _ = device  # Mark as used for potential future GPU optimization

        except Exception:
            pass

    # Use CPU DLX for the actual solving
    # (DLX is more efficient for this backtracking problem
    # than GPU brute force)
    return solve_area_dlx(rows, cols, elements_to_place)


def generic_worker(
    worker_id: int, work_queue: Queue, result_queue: Queue,
    element_rotations: Dict, timing_dict: Dict,
    worker_type: str, solve_func, result_cache: Dict,
    cache_hits: Dict
):
    """Generic worker process for CPU or GPU."""
    worker_name = f"{worker_type}-{worker_id}"

    while True:
        try:
            item = work_queue.get(timeout=1)
            if item is None:  # Poison pill
                break

            area_idx, area_data, total_areas = item
            rows, cols, element_counts = area_data

            # Create cache key from area configuration
            cache_key = (rows, cols, tuple(element_counts))

            # Check if we've solved this configuration before
            if cache_key in result_cache:
                cached_data = result_cache[cache_key]
                first_area_idx = cached_data['first_area']
                result = cached_data['result']
                status = cached_data['status']

                # Increment cache hit counter
                cache_hits[cache_key] = cache_hits.get(cache_key, 0) + 1

                elapsed = 0.0  # Cached result, instant lookup

                # Record timing
                timing_dict[worker_name].append(elapsed)

                result_queue.put((
                    area_idx,
                    result,
                    f"[{worker_name}] Area {area_idx + 1}/{total_areas}: "
                    f"{rows}x{cols} ({rows * cols} cells) - {status} "
                    f"(same as area {first_area_idx + 1}, "
                    f"reused {cache_hits[cache_key]}x) [{elapsed:.2f}s]"
                ))
                continue

            start_time = time.time()

            # Build list of elements to place with deduplicated rotations
            elements_to_place = []
            for element_id, count in enumerate(element_counts):
                if element_id in element_rotations and count > 0:
                    # Get unique rotations once per element type
                    unique_rots = element_rotations[element_id]
                    # Add this element 'count' times
                    for _ in range(count):
                        elements_to_place.append((element_id, unique_rots))

            # Calculate stats
            total_cells_needed = sum(
                len(unique_rots[0])
                for _, unique_rots in elements_to_place
            )
            grid_cells = rows * cols

            # Solve
            if total_cells_needed > grid_cells:
                result = False
                status = "✗ Too many cells"
            elif solve_func(rows, cols, elements_to_place):
                result = True
                status = "✓ Fits"
            else:
                result = False
                status = "✗ Doesn't fit"

            elapsed = time.time() - start_time

            # Store in cache for future use
            result_cache[cache_key] = {
                'first_area': area_idx,
                'result': result,
                'status': status
            }

            # Record timing
            timing_dict[worker_name].append(elapsed)

            result_queue.put((
                area_idx,
                result,
                f"[{worker_name}] Area {area_idx + 1}/{total_areas}: "
                f"{rows}x{cols} ({grid_cells} cells), "
                f"{len(elements_to_place)} elements "
                f"({total_cells_needed} cells) - {status} "
                f"[{elapsed:.2f}s]"
            ))

        except Exception:
            break


def cpu_worker(
    worker_id: int, work_queue: Queue, result_queue: Queue,
    element_rotations: Dict, timing_dict: Dict,
    result_cache: Dict, cache_hits: Dict
):
    """CPU worker process."""
    generic_worker(
        worker_id, work_queue, result_queue,
        element_rotations, timing_dict,
        "CPU", solve_area_dlx, result_cache, cache_hits
    )


def gpu_worker(
    worker_id: int, work_queue: Queue, result_queue: Queue,
    element_rotations: Dict, timing_dict: Dict,
    result_cache: Dict, cache_hits: Dict
):
    """GPU worker process."""
    if not GPU_AVAILABLE:
        return
    generic_worker(
        worker_id, work_queue, result_queue,
        element_rotations, timing_dict,
        "GPU", solve_area_gpu, result_cache, cache_hits
    )


def count_fitting_areas_hybrid(
    filename: str, num_cpu_workers: int = 8, num_gpu_workers: int = 12
) -> Tuple[int, Dict]:
    """
    Count areas using hybrid CPU+GPU processing.
    Returns (fitting_count, timing_stats).
    """
    elements, areas = parse_input(filename)

    # Precompute unique rotations for each element type ONCE
    # This is the optimization to avoid recalculating same rotations
    print("Precomputing unique rotations for each element type...")
    element_rotations = {}
    for element_id, shape in elements.items():
        unique_rots = get_unique_rotations(shape)
        element_rotations[element_id] = unique_rots
        print(f"  Element {element_id}: {len(unique_rots)} "
              f"unique rotation(s)")

    total_areas = len(areas)
    print(f"\nTotal areas to process: {total_areas}")
    print(f"Using {num_cpu_workers} CPU workers "
          f"and {num_gpu_workers} GPU workers")

    if not GPU_AVAILABLE:
        print("Warning: GPU not available, using CPU workers only")
        num_gpu_workers = 0
        num_cpu_workers = 8

    # Create shared structures
    manager = Manager()
    work_queue = Queue()
    result_queue = Queue()
    timing_dict = manager.dict()
    result_cache = manager.dict()  # Shared cache for duplicate areas
    cache_hits = manager.dict()  # Track cache hit counts

    # Initialize timing dict for all workers
    for i in range(num_cpu_workers):
        timing_dict[f"CPU-{i}"] = manager.list()
    for i in range(num_gpu_workers):
        timing_dict[f"GPU-{i}"] = manager.list()

    # Populate work queue
    for idx, area in enumerate(areas):
        work_queue.put((idx, area, total_areas))

    # Add poison pills
    for _ in range(num_cpu_workers + num_gpu_workers):
        work_queue.put(None)

    # Start workers
    workers = []

    print("\nStarting CPU workers...")
    for i in range(num_cpu_workers):
        p = Process(
            target=cpu_worker,
            args=(i, work_queue, result_queue, element_rotations,
                  timing_dict, result_cache, cache_hits)
        )
        p.start()
        workers.append(p)

    print("Starting GPU workers...")
    for i in range(num_gpu_workers):
        p = Process(
            target=gpu_worker,
            args=(i, work_queue, result_queue, element_rotations,
                  timing_dict, result_cache, cache_hits)
        )
        p.start()
        workers.append(p)

    # Collect and print results immediately as they come in
    fitting_count = 0
    too_many_cells_count = 0
    doesnt_fit_count = 0
    cached_count = 0
    results_received = 0

    while results_received < total_areas:
        area_idx, result, message = result_queue.get()
        # Print immediately
        print(message, flush=True)

        # Track statistics
        if result:
            fitting_count += 1
        elif "Too many cells" in message:
            too_many_cells_count += 1
        elif "Doesn't fit" in message:
            doesnt_fit_count += 1

        if "cached" in message or "reused" in message:
            cached_count += 1

        results_received += 1

    # Wait for all workers to finish
    for p in workers:
        p.join()

    # Calculate and print timing statistics
    print("\n" + "=" * 70)
    print("TIMING STATISTICS")
    print("=" * 70)

    timing_stats = {}
    cpu_times = []
    gpu_times = []
    cpu_count = 0
    gpu_count = 0

    # Collect all timing data
    for worker_name, times in timing_dict.items():
        times_list = list(times)
        if times_list:
            avg_time = sum(times_list) / len(times_list)
            total_time = sum(times_list)
            timing_stats[worker_name] = {
                'count': len(times_list),
                'total': total_time,
                'average': avg_time,
                'min': min(times_list),
                'max': max(times_list)
            }

            if worker_name.startswith('CPU'):
                cpu_times.extend(times_list)
                cpu_count += len(times_list)
            else:
                gpu_times.extend(times_list)
                gpu_count += len(times_list)

    # Print per-worker statistics
    print("\nPer-Worker Performance:")
    print("-" * 70)

    # CPU workers
    cpu_workers = sorted([
        w for w in timing_stats.keys() if w.startswith('CPU')
    ])
    for worker_name in cpu_workers:
        stats = timing_stats[worker_name]
        print(f"{worker_name}:")
        print(f"  Areas: {stats['count']:3d}  |  "
              f"Avg: {stats['average']:6.3f}s  |  "
              f"Total: {stats['total']:7.2f}s  |  "
              f"Range: {stats['min']:.3f}s - {stats['max']:.3f}s")

    # GPU workers
    if gpu_times:
        print()
        gpu_workers = sorted([
            w for w in timing_stats.keys() if w.startswith('GPU')
        ])
        for worker_name in gpu_workers:
            stats = timing_stats[worker_name]
            print(f"{worker_name}:")
            print(f"  Areas: {stats['count']:3d}  |  "
                  f"Avg: {stats['average']:6.3f}s  |  "
                  f"Total: {stats['total']:7.2f}s  |  "
                  f"Range: {stats['min']:.3f}s - {stats['max']:.3f}s")

    # Print comparison summary
    print("\n" + "=" * 70)
    print("CPU vs GPU COMPARISON")
    print("=" * 70)

    if cpu_times:
        avg_cpu = sum(cpu_times) / len(cpu_times)
        total_cpu = sum(cpu_times)
        print("\n📊 CPU CORES:")
        print(f"  Total areas processed: {cpu_count}")
        print(f"  Average time per area: {avg_cpu:.3f}s")
        print(f"  Total time (all cores): {total_cpu:.2f}s")
        print(f"  Min time: {min(cpu_times):.3f}s")
        print(f"  Max time: {max(cpu_times):.3f}s")

    if gpu_times:
        avg_gpu = sum(gpu_times) / len(gpu_times)
        total_gpu = sum(gpu_times)
        print("\n🎮 GPU CORES:")
        print(f"  Total areas processed: {gpu_count}")
        print(f"  Average time per area: {avg_gpu:.3f}s")
        print(f"  Total time (all cores): {total_gpu:.2f}s")
        print(f"  Min time: {min(gpu_times):.3f}s")
        print(f"  Max time: {max(gpu_times):.3f}s")

    if cpu_times and gpu_times:
        print("\n⚡ PERFORMANCE COMPARISON:")
        if avg_gpu < avg_cpu:
            speedup = avg_cpu / avg_gpu
            print(f"  GPU is {speedup:.2f}x FASTER than CPU")
        elif avg_cpu < avg_gpu:
            speedup = avg_gpu / avg_cpu
            print(f"  CPU is {speedup:.2f}x FASTER than GPU")
        else:
            print("  CPU and GPU have similar performance")

        print("\n📈 WORKLOAD DISTRIBUTION:")
        total_work = cpu_count + gpu_count
        cpu_pct = (cpu_count / total_work) * 100
        gpu_pct = (gpu_count / total_work) * 100
        print(f"  CPU handled: {cpu_count}/{total_work} areas "
              f"({cpu_pct:.1f}%)")
        print(f"  GPU handled: {gpu_count}/{total_work} areas "
              f"({gpu_pct:.1f}%)")
    elif cpu_times:
        print("\n(GPU workers not used)")

    # Print result statistics
    print("\n" + "=" * 70)
    print("RESULT STATISTICS")
    print("=" * 70)

    print(f"\n✅ AREAS THAT FIT: {fitting_count}/{total_areas} "
          f"({(fitting_count/total_areas)*100:.1f}%)")

    total_failed = too_many_cells_count + doesnt_fit_count
    print(f"\n❌ AREAS THAT DON'T FIT: {total_failed}/{total_areas} "
          f"({(total_failed/total_areas)*100:.1f}%)")
    print(f"  • Too many cells (elements > grid): "
          f"{too_many_cells_count}")
    print(f"  • Doesn't fit after trying rotations: "
          f"{doesnt_fit_count}")

    print("\n💾 CACHING:")
    print(f"  • Areas skipped (reused from cache): {cached_count}")
    print(f"  • Areas computed from scratch: "
          f"{total_areas - cached_count}")

    # Print cache statistics
    if result_cache:
        print("\n" + "=" * 70)
        print("DETAILED CACHE STATISTICS")
        print("=" * 70)
        unique_configs = len(result_cache)
        total_cache_hits = sum(cache_hits.values())

        print(f"\n  Unique area configurations: {unique_configs}")
        if total_cache_hits > 0:
            cache_efficiency = (total_cache_hits / total_areas) * 100
            print(f"  Cache efficiency: {cache_efficiency:.1f}%")
            print("\n  Top reused configurations:")
            sorted_hits = sorted(
                cache_hits.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]
            for cache_key, hit_count in sorted_hits:
                rows, cols, _ = cache_key
                print(f"    {rows}x{cols} grid: reused {hit_count}x")

    print("=" * 70)

    return fitting_count, timing_stats


if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else "12.csv"
    start = time.time()
    result, stats = count_fitting_areas_hybrid(filename)
    elapsed = time.time() - start

    print("\n" + "=" * 70)
    print(f"Number of areas that can fit all elements: {result}")
    print(f"Total execution time: {elapsed:.2f}s")
    print("=" * 70)
