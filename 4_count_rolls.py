# Read the file and create the matrix
with open('4.csv', 'r') as f:
    lines = f.readlines()

# Parse the matrix (skip line numbers at the beginning)
matrix = []
for line in lines:
    if line.strip():  # Skip empty lines
        # Remove the line number prefix (e.g., "     1→")
        content = line.split('→')[1].strip() if '→' in line else line.strip()
        matrix.append(content)

rows = len(matrix)
cols = len(matrix[0]) if rows > 0 else 0

print(f"Matrix dimensions: {rows} rows x {cols} columns")

# Count rolls with fewer than 4 adjacent rolls
count = 0

# Define the 8 directions: up, down, left, right, and 4 diagonals
directions = [
    (-1, -1), (-1, 0), (-1, 1),  # top-left, top, top-right
    (0, -1),           (0, 1),   # left, right
    (1, -1),  (1, 0),  (1, 1)    # bottom-left, bottom, bottom-right
]

for i in range(rows):
    for j in range(len(matrix[i])):
        if matrix[i][j] == '@':
            # Count adjacent rolls
            adjacent_rolls = 0
            for di, dj in directions:
                ni, nj = i + di, j + dj
                # Check if the neighbor is within bounds
                if 0 <= ni < rows and 0 <= nj < len(matrix[ni]):
                    if matrix[ni][nj] == '@':
                        adjacent_rolls += 1

            # Check if this roll has fewer than 4 adjacent rolls
            if adjacent_rolls < 4:
                count += 1

print(f"\nNumber of rolls with fewer than 4 adjacent rolls: {count}")
