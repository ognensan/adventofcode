#!/usr/bin/env python3

# Read the file
with open('5.csv', 'r') as f:
    content = f.read()

# Split by blank line
parts = content.strip().split('\n\n')
ranges_part = parts[0].strip().split('\n')

# Parse ranges
ranges = []
for line in ranges_part:
    if line.strip():
        start, end = map(int, line.split('-'))
        ranges.append((start, end))

print(f"Number of ranges: {len(ranges)}")

# Sort ranges by start position
ranges.sort()

# Merge overlapping ranges
merged_ranges = []
for start, end in ranges:
    if merged_ranges and start <= merged_ranges[-1][1] + 1:
        # Overlapping or adjacent - merge with previous range
        prev_start = merged_ranges[-1][0]
        prev_end = merged_ranges[-1][1]
        merged_ranges[-1] = (prev_start, max(prev_end, end))
    else:
        # Non-overlapping - add as new range
        merged_ranges.append((start, end))

print(f"Number of merged ranges: {len(merged_ranges)}")

# Count total unique numbers across all merged ranges
total_count = 0
for start, end in merged_ranges:
    count = end - start + 1
    total_count += count

print(f"Total unique numbers in all ranges: {total_count}")

# Show some example merged ranges
print("\nFirst 10 merged ranges:")
for i, (start, end) in enumerate(merged_ranges[:10]):
    count = end - start + 1
    print(f"  {start}-{end} ({count:,} numbers)")
