# Read the file and create the matrix
with open('4.csv', 'r') as f:
    lines = f.readlines()

# Parse the matrix (skip line numbers at the beginning)
matrix = []
for line in lines:
    if line.strip():  # Skip empty lines
        # Remove the line number prefix (e.g., "     1→")
        content = line.split('→')[1].strip() if '→' in line else line.strip()
        matrix.append(list(content))  # Convert to list for mutability

rows = len(matrix)
cols = len(matrix[0]) if rows > 0 else 0

print(f"Matrix dimensions: {rows} rows x {cols} columns")

# Count initial rolls
initial_rolls = sum(row.count('@') for row in matrix)
print(f"Initial number of rolls: {initial_rolls}")

# Define the 8 directions
directions = [
    (-1, -1), (-1, 0), (-1, 1),  # top-left, top, top-right
    (0, -1),           (0, 1),   # left, right
    (1, -1),  (1, 0),  (1, 1)    # bottom-left, bottom, bottom-right
]


def count_adjacent_rolls(matrix, i, j):
    """Count adjacent rolls for position (i, j)"""
    adjacent_rolls = 0
    for di, dj in directions:
        ni, nj = i + di, j + dj
        # Check if the neighbor is within bounds
        if 0 <= ni < len(matrix) and 0 <= nj < len(matrix[ni]):
            if matrix[ni][nj] == '@':
                adjacent_rolls += 1
    return adjacent_rolls


# Iteratively remove rolls with fewer than 4 adjacent rolls
iteration = 0
total_removed = 0

while True:
    iteration += 1
    # Find all rolls with fewer than 4 adjacent rolls
    to_remove = []

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == '@':
                adjacent_rolls = count_adjacent_rolls(matrix, i, j)
                if adjacent_rolls < 4:
                    to_remove.append((i, j))

    # If no rolls to remove, we're done
    if not to_remove:
        print(f"\nNo more rolls to remove after iteration {iteration - 1}")
        break

    # Remove the rolls
    for i, j in to_remove:
        matrix[i][j] = '.'

    removed_this_iteration = len(to_remove)
    total_removed += removed_this_iteration

    print(f"Iteration {iteration}: Removed {removed_this_iteration} rolls "
          f"(total removed: {total_removed})")

# Count final rolls
final_rolls = sum(row.count('@') for row in matrix)
print(f"\nFinal number of rolls: {final_rolls}")
print(f"Total rolls removed: {total_removed}")
print(f"Verification: {initial_rolls} - {total_removed} = {final_rolls}")

# Write the result to a new file
with open('4_processed.csv', 'w') as f:
    for idx, row in enumerate(matrix, 1):
        # Format with line numbers like the original
        line_num = f"{idx:>6}→"
        f.write(line_num + ''.join(row) + '\n')

print("\nProcessed matrix saved to '4_processed.csv'")
