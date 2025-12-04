with open('3.csv', 'r') as f:
    lines = f.readlines()

total = 0
for line_num, line in enumerate(lines, 1):
    line = line.strip()
    if not line:
        continue

    # Get all digits (not positions, just the digit characters)
    digits = [char for char in line if char.isdigit()]

    # If we don't have 12 digits, skip
    if len(digits) < 12:
        print(f"Line {line_num}: only {len(digits)} digits available")
        continue

    # Greedy approach: pick the largest digit at each step
    # ensuring we have enough digits remaining
    result = []
    start_pos = 0
    digits_needed = 12

    for i in range(12):
        # We need digits_needed more digits (including this one)
        # So we can search up to position: len(digits) - digits_needed
        search_end = len(digits) - digits_needed + 1

        # Find the maximum digit in the valid range
        max_digit = '0'
        max_pos = start_pos
        for pos in range(start_pos, search_end):
            if digits[pos] > max_digit:
                max_digit = digits[pos]
                max_pos = pos

        result.append(max_digit)
        start_pos = max_pos + 1
        digits_needed -= 1

    max_num = int(''.join(result))
    print(f"Line {line_num}: max 12-digit number = {max_num}")
    total += max_num

print(f"\nTotal sum: {total}")
