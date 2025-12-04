def has_repeating_sequence(num):
    """Check if a number has repeating sequences of digits"""
    s = str(num)
    length = len(s)

    # Check all possible pattern lengths (from 1 to half the string length)
    for pattern_len in range(1, length // 2 + 1):
        # Only check if the string length is divisible by pattern length
        if length % pattern_len == 0:
            pattern = s[:pattern_len]
            # Check if repeating this pattern creates the entire string
            if pattern * (length // pattern_len) == s:
                return True, pattern
    return False, None


# Check some of the large numbers
test_numbers = [6666666666, 3687536875, 628628628, 42424242, 59595959]

print("Verifying large invalid numbers:")
for num in test_numbers:
    result, pattern = has_repeating_sequence(num)
    if result:
        repeated = pattern * (len(str(num)) // len(pattern))
        print(f"{num}: repeating pattern '{pattern}' -> {repeated}")
    else:
        print(f"{num}: NOT repeating")

# What's the contribution of the top 10 largest numbers?
with open('2.csv', 'r') as f:
    content = f.read().strip()

ranges = content.split(',')
all_invalid = []

for range_str in ranges:
    start, end = map(int, range_str.split('-'))
    for num in range(start, end + 1):
        result, _ = has_repeating_sequence(num)
        if result:
            all_invalid.append(num)

all_invalid.sort(reverse=True)
print("\nTop 10 largest invalid numbers:")
for i, num in enumerate(all_invalid[:10], 1):
    print(f"{i}. {num}")

print(f"\nSum of top 10: {sum(all_invalid[:10])}")
print(f"Total sum: {sum(all_invalid)}")
print(f"Total count: {len(all_invalid)}")
