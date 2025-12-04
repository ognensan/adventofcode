from PIL import Image, ImageDraw, ImageFont

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

# Create image - each cell is 5x5 pixels
cell_size = 5
img_width = cols * cell_size
img_height = rows * cell_size

# Create the image
img = Image.new('RGB', (img_width, img_height), color='white')
pixels = img.load()

# Color the pixels
roll_count = 0
for i in range(rows):
    for j in range(len(matrix[i])):
        if matrix[i][j] == '@':
            roll_count += 1
            # Color this cell red
            for pi in range(cell_size):
                for pj in range(cell_size):
                    x = j * cell_size + pj
                    y = i * cell_size + pi
                    pixels[x, y] = (200, 50, 50)  # Red

# Save the image
img.save('final_matrix.png')
print("Final matrix visualization saved to 'final_matrix.png'")
print(f"Image size: {img_width}x{img_height} pixels")
print(f"Rolls shown: {roll_count}")

# Also create a comparison image
with open('4.csv', 'r') as f:
    lines = f.readlines()

original_matrix = []
for line in lines:
    if line.strip():
        content = line.split('→')[1].strip() if '→' in line else line.strip()
        original_matrix.append(list(content))

# Create comparison image (side by side)
comparison_width = img_width * 2 + 60  # 60 pixels gap
comparison_height = img_height + 60  # 60 pixels for title

comparison = Image.new('RGB', (comparison_width, comparison_height),
                       color='white')
draw = ImageDraw.Draw(comparison)

# Draw original matrix
original_roll_count = 0
for i in range(rows):
    for j in range(len(original_matrix[i])):
        if original_matrix[i][j] == '@':
            original_roll_count += 1
            for pi in range(cell_size):
                for pj in range(cell_size):
                    x = 30 + j * cell_size + pj
                    y = 50 + i * cell_size + pi
                    in_bounds = (0 <= x < comparison_width and
                                 0 <= y < comparison_height)
                    if in_bounds:
                        comparison.putpixel((x, y), (200, 50, 50))  # Red

# Draw final matrix
for i in range(rows):
    for j in range(len(matrix[i])):
        if matrix[i][j] == '@':
            for pi in range(cell_size):
                for pj in range(cell_size):
                    x = img_width + 60 + j * cell_size + pj
                    y = 50 + i * cell_size + pi
                    in_bounds = (0 <= x < comparison_width and
                                 0 <= y < comparison_height)
                    if in_bounds:
                        comparison.putpixel((x, y), (50, 150, 50))  # Green

# Add labels
try:
    font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 20)
except Exception:
    font = ImageFont.load_default()

draw.text((30, 10), f"Original: {original_roll_count} rolls",
          fill='black', font=font)
draw.text((img_width + 60, 10), f"Final: {roll_count} rolls",
          fill='black', font=font)

comparison.save('matrix_comparison.png')
print("Comparison visualization saved to 'matrix_comparison.png'")
print(f"Original: {original_roll_count} rolls → Final: {roll_count} rolls")
print(f"Removed: {original_roll_count - roll_count} rolls")
