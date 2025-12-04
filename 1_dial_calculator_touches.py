#!/usr/bin/env python3

def count_zero_touches_manual(start_pos, direction, value):
    """Manually count by simulating each step"""
    count = 0
    pos = start_pos
    for step in range(value):
        if direction == 'R':
            pos = (pos + 1) % 100
        else:  # L
            pos = (pos - 1) % 100
        if pos == 0:
            count += 1
    return count, pos


# Read the movements from the CSV file
with open('1.csv', 'r') as f:
    movements = [line.strip() for line in f if line.strip()]

# Starting position
position = 50
touch_count = 0
touch_details = []

print(f"Starting position: {position}")
print()
print("Verifying logic with first few movements...")

# Process each movement
for i, movement in enumerate(movements, 1):
    # Parse the movement
    direction = movement[0]
    value = int(movement[1:])

    # Calculate how many times we touch/cross 0 in this movement
    touches_in_movement = 0

    if direction == 'R':
        # Moving right by 'value' positions
        # We cross 0 each time we pass through 100, 200, 300, etc.
        # From position P, moving right by V: crossings = floor((P + V) / 100)
        touches_in_movement = (position + value) // 100

    else:  # L
        # Moving left by 'value' positions
        # We cross 0 when we go backwards past it
        # From position P, moving left by V:
        # - If P = 0: we touch 0 at steps 100, 200, ... so floor(V/100) times
        # - If V < P: no crossings (we stay above 0)
        # - If V >= P and P > 0: we cross 0 at least once
        #   crossings = 1 + floor((V - P) / 100)
        if position == 0:
            touches_in_movement = value // 100
        elif value >= position:
            touches_in_movement = 1 + (value - position) // 100
        else:
            touches_in_movement = 0

    # Verify with manual calculation for first 5 movements with touches
    if i <= 100 and touches_in_movement > 0:
        manual_touches, manual_pos = count_zero_touches_manual(
            position, direction, value
        )
        if direction == 'R':
            formula_pos = (position + value) % 100
        else:
            formula_pos = (position - value) % 100
        if manual_touches != touches_in_movement:
            print(f"MISMATCH at movement {i}: {movement} from {position}")
            print(f"  Formula: {touches_in_movement}, "
                  f"Manual: {manual_touches}")

    # Update the total count
    touch_count += touches_in_movement

    # Calculate new position
    if direction == 'R':
        new_position = (position + value) % 100
    else:
        new_position = (position - value) % 100

    # Record details if we touched 0
    if touches_in_movement > 0:
        touch_details.append({
            'movement_num': i,
            'movement': movement,
            'from': position,
            'to': new_position,
            'touches': touches_in_movement
        })

    position = new_position

print()
print("=" * 60)
print(f"Total times the dial touched/crossed 0: {touch_count}")
print()

# Show some examples of movements with multiple touches
multi_touch = [d for d in touch_details if d['touches'] > 1]
print(f"Movements that touched 0 multiple times: {len(multi_touch)}")
print()
print("First 10 movements with multiple touches:")
for detail in multi_touch[:10]:
    msg = (f"  Movement #{detail['movement_num']}: {detail['movement']} "
           f"(from {detail['from']} to {detail['to']}) - "
           f"touched {detail['touches']} times")
    print(msg)

print()
print(f"Total movements that touched 0 at least once: {len(touch_details)}")
print(f"Total zero-touches across all movements: {touch_count}")
