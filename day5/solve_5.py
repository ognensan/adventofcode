#!/usr/bin/env python3

# Read the file
with open('5.csv', 'r') as f:
    content = f.read()

# Split by blank line
parts = content.strip().split('\n\n')
ranges_part = parts[0].strip().split('\n')
numbers_part = parts[1].strip().split('\n')

# Parse ranges
ranges = []
for line in ranges_part:
    if line.strip():
        start, end = map(int, line.split('-'))
        ranges.append((start, end))

# Parse numbers
numbers = []
for line in numbers_part:
    if line.strip():
        numbers.append(int(line))

# Count how many numbers fall in any range
count = 0
matching_numbers = set()

for num in numbers:
    for start, end in ranges:
        if start <= num <= end:
            if num not in matching_numbers:
                matching_numbers.add(num)
                count += 1
            break  # No need to check other ranges for this number

print(f"Number of ranges: {len(ranges)}")
print(f"Number of values to check: {len(numbers)}")
print(f"Numbers that fall in any range: {count}")
