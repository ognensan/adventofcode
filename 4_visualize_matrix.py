import matplotlib.pyplot as plt
import numpy as np

# Read the processed file
with open('4_processed.csv', 'r') as f:
    lines = f.readlines()

# Parse the matrix
matrix = []
for line in lines:
    if line.strip():
        content = line.split('→')[1].strip() if '→' in line else line.strip()
        matrix.append(list(content))

rows = len(matrix)
cols = len(matrix[0]) if rows > 0 else 0

# Convert to numpy array (1 for @, 0 for .)
matrix_array = np.zeros((rows, cols))
for i in range(rows):
    for j in range(len(matrix[i])):
        if matrix[i][j] == '@':
            matrix_array[i][j] = 1

# Create the visualization
plt.figure(figsize=(14, 14))
plt.imshow(matrix_array, cmap='RdYlGn_r', interpolation='nearest')
plt.title(f'Final Matrix Visualization\n{int(matrix_array.sum())} rolls '
          f'remaining', fontsize=16, fontweight='bold')
plt.xlabel('Column', fontsize=12)
plt.ylabel('Row', fontsize=12)
plt.colorbar(label='Roll (@) = 1, Empty (.) = 0', shrink=0.8)
plt.tight_layout()
plt.savefig('final_matrix.png', dpi=150, bbox_inches='tight')
print("Visualization saved to 'final_matrix.png'")

# Also create a comparison with the original
with open('4.csv', 'r') as f:
    lines = f.readlines()

original_matrix = []
for line in lines:
    if line.strip():
        content = line.split('→')[1].strip() if '→' in line else line.strip()
        original_matrix.append(list(content))

original_array = np.zeros((rows, cols))
for i in range(rows):
    for j in range(len(original_matrix[i])):
        if original_matrix[i][j] == '@':
            original_array[i][j] = 1

# Create side-by-side comparison
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))

ax1.imshow(original_array, cmap='RdYlGn_r', interpolation='nearest')
ax1.set_title(f'Original Matrix\n{int(original_array.sum())} rolls',
              fontsize=14, fontweight='bold')
ax1.set_xlabel('Column')
ax1.set_ylabel('Row')

ax2.imshow(matrix_array, cmap='RdYlGn_r', interpolation='nearest')
ax2.set_title(f'Final Matrix (After Removal)\n{int(matrix_array.sum())} '
              f'rolls remaining', fontsize=14, fontweight='bold')
ax2.set_xlabel('Column')
ax2.set_ylabel('Row')

plt.tight_layout()
plt.savefig('matrix_comparison.png', dpi=150, bbox_inches='tight')
print("Comparison visualization saved to 'matrix_comparison.png'")

plt.show()
