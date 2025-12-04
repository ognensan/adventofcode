def has_repeating_sequence(num):
    """Check if a number has repeating sequences of digits.

    (any number of repeats)
    """
    s = str(num)
    length = len(s)

    # Check all possible pattern lengths (from 1 to half the string length)
    for pattern_len in range(1, length // 2 + 1):
        # Only check if the string length is divisible by pattern length
        if length % pattern_len == 0:
            pattern = s[:pattern_len]
            # Pattern cannot have a leading zero
            if pattern[0] == '0':
                continue
            # Check if repeating this pattern creates the entire string
            if pattern * (length // pattern_len) == s:
                return True

    return False


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
