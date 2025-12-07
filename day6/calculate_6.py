#!/usr/bin/env python3

# Read the file
with open('6.csv', 'r') as f:
    lines = f.readlines()

# Parse the data - skip empty lines and split by whitespace
rows = []
for line in lines:
    line = line.strip()
    if line and not line.startswith('→'):
        # Remove the line number prefix (e.g., "1→", "2→", etc.)
        if '→' in line:
            line = line.split('→', 1)[1]
        # Split by whitespace
        values = line.split()
        rows.append(values)

# Debug: print number of rows and columns
print(f"Number of rows: {len(rows)}")
print(f"Number of columns: {len(rows[0]) if rows else 0}")

# The last row contains the operators
operators = rows[4]  # Row 5 (index 4) contains the operators
number_rows = rows[:4]  # Rows 1-4 (indices 0-3) contain numbers

# Process each column
column_results = []
num_columns = len(operators)

for col_idx in range(num_columns):
    operator = operators[col_idx]

    # Get all numbers in this column (from rows 1-4)
    numbers = []
    for row in number_rows:
        if col_idx < len(row):
            numbers.append(int(row[col_idx]))

    # Apply the operator
    if operator == '+':
        result = sum(numbers)
    elif operator == '*':
        result = 1
        for num in numbers:
            result *= num
    else:
        print(f"Unknown operator '{operator}' at column {col_idx}")
        result = 0

    column_results.append(result)
    # Uncomment the line below to see detailed column calculations
    # print(f"Column {col_idx + 1}: numbers={numbers}, "
    #       f"operator={operator}, result={result}")

# Calculate grand total
grand_total = sum(column_results)

print(f"\n{'='*60}")
print(f"Grand Total: {grand_total}")
print(f"{'='*60}")
