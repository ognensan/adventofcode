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

print(f"Starting position: row {start_row + 1}, column {start_col + 1}")

# Simulate the flow
# Track active streams as a set of column indices
active_streams = {start_col}
split_count = 0

# Process each row starting from the row after the starting position
for row_idx in range(start_row + 1, len(grid)):
    row = grid[row_idx]
    new_streams = set()

    # For each active stream, check what's in this row
    for col in active_streams:
        if col < 0 or col >= len(row):
            # Stream goes out of bounds
            continue

        cell = row[col]

        if cell == '.':
            # Continue downward in the same column
            new_streams.add(col)
        elif cell == '^':
            # Split into left and right
            split_count += 1
            # Add left stream (column - 1)
            if col - 1 >= 0:
                new_streams.add(col - 1)
            # Add right stream (column + 1)
            if col + 1 < len(row):
                new_streams.add(col + 1)

    # Update active streams for next row
    active_streams = new_streams

    # Debug: show first few rows
    if row_idx - start_row <= 5:
        print(f"Row {row_idx + 1}: {len(active_streams)} active streams, "
              f"{split_count} total splits so far")

print(f"\n{'='*60}")
print(f"Total number of splits: {split_count}")
print(f"{'='*60}")
