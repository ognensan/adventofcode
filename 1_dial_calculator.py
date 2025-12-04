#!/usr/bin/env python3

# Read the movements from the CSV file
with open('1.csv', 'r') as f:
    movements = [line.strip() for line in f if line.strip()]

# Starting position
position = 50
zero_count = 0
zero_positions = []

print(f"Starting position: {position}")
print()

# Process each movement
for i, movement in enumerate(movements, 1):
    # Parse the movement
    direction = movement[0]
    value = int(movement[1:])

    # Apply the movement
    if direction == 'R':
        position = (position + value) % 100
    else:  # L
        position = (position - value) % 100

    # Check if we hit 0
    if position == 0:
        zero_count += 1
        zero_positions.append(i)

print()
print("=" * 60)
print(f"Total times the dial reached 0: {zero_count}")
print(f"At movement numbers: {zero_positions}")
