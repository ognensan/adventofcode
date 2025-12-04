#!/usr/bin/env python3

# Read the movements from the CSV file
with open('1.csv', 'r') as f:
    movements = [line.strip() for line in f if line.strip()]

# Method 1: Count only when landing exactly on 0
position = 50
land_count = 0
for movement in movements:
    direction = movement[0]
    value = int(movement[1:])
    if direction == 'R':
        position = (position + value) % 100
    else:
        position = (position - value) % 100
    if position == 0:
        land_count += 1

# Method 2: Count every time dial touches/crosses 0 during movement
position = 50
touch_count = 0
movement_with_touches = 0
movements_with_multiple_touches = 0
max_touches_in_one = 0

for movement in movements:
    direction = movement[0]
    value = int(movement[1:])

    touches = 0
    if direction == 'R':
        touches = (position + value) // 100
    else:  # L
        if position == 0:
            touches = value // 100
        elif value >= position:
            touches = 1 + (value - position) // 100

    touch_count += touches
    if touches > 0:
        movement_with_touches += 1
    if touches > 1:
        movements_with_multiple_touches += 1
    if touches > max_touches_in_one:
        max_touches_in_one = touches

    if direction == 'R':
        position = (position + value) % 100
    else:
        position = (position - value) % 100

print("=" * 70)
print("DIAL POSITION 0 ANALYSIS")
print("=" * 70)
print("Starting position: 50")
print(f"Total movements: {len(movements)}")
print()
print("METHOD 1: Counting only final landing position")
print(f"  Times landed exactly on 0: {land_count}")
print()
print("METHOD 2: Counting every touch/crossing during movement")
print(f"  Total zero touches/crossings: {touch_count}")
print(f"  Movements that touched 0 at least once: "
      f"{movement_with_touches}")
print(f"  Movements that touched 0 multiple times: "
      f"{movements_with_multiple_touches}")
print(f"  Maximum touches in a single movement: {max_touches_in_one}")
print()
print("DIFFERENCE")
print(f"  Additional touches from passing through 0: "
      f"{touch_count - land_count}")
print(f"  Average touches per movement: {touch_count / len(movements):.2f}")
print("=" * 70)
