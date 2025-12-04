from itertools import combinations

with open('3.csv', 'r') as f:
    lines = f.readlines()

total = 0
for line_num, line in enumerate(lines, 1):
    line = line.strip()
    if not line:
        continue

    # Get all digit positions
    digit_positions = []
    for i, char in enumerate(line):
        if char.isdigit():
            digit_positions.append((i, char))

    # If we don't have 12 digits, skip or handle accordingly
    if len(digit_positions) < 12:
        print(f"Line {line_num}: only {len(digit_positions)} digits available")
        continue

    max_num = 0
    # Try all combinations of 12 positions (maintaining order)
    for combo in combinations(range(len(digit_positions)), 12):
        # Form the 12-digit number from selected positions
        num_str = ''.join(digit_positions[i][1] for i in combo)
        num = int(num_str)
        max_num = max(max_num, num)

    print(f"Line {line_num}: max 12-digit number = {max_num}")
    total += max_num

print(f"\nTotal sum: {total}")
