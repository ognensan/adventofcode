#!/usr/bin/env python3

# Read the original file
with open('6.csv', 'r') as f:
    lines = f.readlines()

# Parse rows
rows = []
for line in lines:
    if '→' in line:
        line = line.split('→', 1)[1]
    rows.append(line.rstrip('\n'))

# Find operator row
operator_row_idx = -1
for i, row in enumerate(rows):
    non_space = [c for c in row if c not in [' ', '\t']]
    if non_space and all(c in ['*', '+'] for c in non_space):
        operator_row_idx = i
        break

number_rows = rows[:operator_row_idx]
operator_row = rows[operator_row_idx]

# Analyze operator row to find column positions
operator_positions = []
for i, char in enumerate(operator_row):
    if char in ['*', '+']:
        operator_positions.append((i, char))

# Calculate column definitions
columns = []
for idx in range(len(operator_positions)):
    start_pos = operator_positions[idx][0]
    operator = operator_positions[idx][1]

    if idx < len(operator_positions) - 1:
        next_pos = operator_positions[idx + 1][0]
        width = next_pos - start_pos
    else:
        width = len(operator_row) - start_pos

    columns.append({
        'start': start_pos,
        'width': width,
        'operator': operator
    })

# Process all columns
column_results = []

for col_idx, col in enumerate(columns):
    # Extract vertical strings for this column
    vertical_strings = []

    for pos_offset in range(col['width']):
        char_pos = col['start'] + pos_offset
        vertical_string = ''

        for row in number_rows:
            if char_pos < len(row):
                vertical_string += row[char_pos]

        vertical_strings.append(vertical_string)

    # Parse numbers from vertical strings
    all_numbers = []
    for v_str in vertical_strings:
        num_str = v_str.replace(' ', '')
        if num_str.isdigit() and num_str:
            all_numbers.append(int(num_str))

    # Calculate
    if col['operator'] == '+':
        result = sum(all_numbers)
    elif col['operator'] == '*':
        result = 1
        for n in all_numbers:
            result *= n
    else:
        result = 0

    column_results.append(result)

# Grand total
grand_total = sum(column_results)

print(f"Processed {len(columns)} columns")
print(f"\n{'='*60}")
print(f"Grand Total: {grand_total}")
print(f"{'='*60}")
