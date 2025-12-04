def has_repeating_sequence(num):
    """Check if a number is exactly two identical halves"""
    s = str(num)
    length = len(s)

    # The number must have even length to split in half
    if length % 2 != 0:
        return False

    # Split in half and check if both halves are equal
    mid = length // 2
    first_half = s[:mid]
    second_half = s[mid:]

    # Pattern cannot have a leading zero
    if first_half[0] == '0':
        return False

    return first_half == second_half


# Read the file
with open('2.csv', 'r') as f:
    content = f.read().strip()

# Parse the ranges
ranges = content.split(',')

total_invalid = 0
all_invalid_numbers = []

for range_str in ranges:
    start, end = map(int, range_str.split('-'))

    # Find invalid numbers in this range
    invalid_numbers = []
    for num in range(start, end + 1):
        if has_repeating_sequence(num):
            invalid_numbers.append(num)

    if invalid_numbers:
        print(f"\nRange {range_str}:")
        print(f"  Invalid numbers: {invalid_numbers}")
        print(f"  Count: {len(invalid_numbers)}")

    all_invalid_numbers.extend(invalid_numbers)
    total_invalid += len(invalid_numbers)

print(f"\n{'='*60}")
print(f"Total invalid numbers across all ranges: {total_invalid}")
print("\nAll invalid numbers:")
print(all_invalid_numbers)
print(f"\n{'='*60}")
print(f"Sum of all invalid numbers: {sum(all_invalid_numbers)}")
