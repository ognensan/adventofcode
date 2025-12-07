#!/usr/bin/env python3

# Read the file
with open('7.csv', 'r') as f:
    lines = f.readlines()

# Parse the grid
grid = []
for line in lines:
    if '→' in line:
        line = line.split('→', 1)[1]
    grid.append(line.rstrip('\n'))

# Remove empty lines
grid = [row for row in grid if row.strip()]

print(f"Grid size: {len(grid)} rows x {len(grid[0]) if grid else 0} columns")

# Find the starting position 'S'
start_row = -1
start_col = -1
for row_idx, row in enumerate(grid):
    for col_idx, char in enumerate(row):
        if char == 'S':
            start_row = row_idx
            start_col = col_idx
            break
    if start_row != -1:
        break

print(f"Starting position: row {start_row + 1}, column {start_col + 1}\n")

# Use dynamic programming to count paths
# dp[row][col] = number of ways to reach position (row, col)
num_rows = len(grid)
num_cols = len(grid[0]) if grid else 0

# Initialize dp table
dp = [[0] * num_cols for _ in range(num_rows)]
dp[start_row][start_col] = 1

# Process each row
for row_idx in range(start_row, num_rows - 1):
    for col_idx in range(num_cols):
        if dp[row_idx][col_idx] == 0:
            # No paths reach this position
            continue

        current_paths = dp[row_idx][col_idx]
        cell = grid[row_idx][col_idx]

        # Determine what happens in the next row
        next_row = row_idx + 1
        if col_idx < len(grid[next_row]):
            next_cell = grid[next_row][col_idx]
        else:
            next_cell = None

        if next_cell == '.':
            # Continue downward in the same column
            dp[next_row][col_idx] += current_paths
        elif next_cell == '^':
            # Split into left and right paths
            # Left path (column - 1)
            if col_idx - 1 >= 0:
                dp[next_row][col_idx - 1] += current_paths
            # Right path (column + 1)
            if col_idx + 1 < num_cols:
                dp[next_row][col_idx + 1] += current_paths

# Count total paths that reach the last row
last_row = num_rows - 1
total_paths = sum(dp[last_row])

print("Processing complete:")
print(f"  Paths in row 1: {sum(dp[start_row])}")
print(f"  Paths in row 5: {sum(dp[min(start_row + 4, num_rows - 1)])}")
print(f"  Paths in row 10: {sum(dp[min(start_row + 9, num_rows - 1)])}")
print(f"  Paths in last row ({last_row + 1}): {total_paths}")

print(f"\n{'='*60}")
print(f"Total number of paths: {total_paths}")
print(f"{'='*60}")
