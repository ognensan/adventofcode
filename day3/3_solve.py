with open('3.csv', 'r') as f:
    lines = f.readlines()

total = 0
for line_num, line in enumerate(lines, 1):
    line = line.strip()
    if not line:
        continue

    max_num = 0
    # Try all pairs where first digit position < second digit position
    for i in range(len(line)):
        if line[i].isdigit():
            for j in range(i + 1, len(line)):
                if line[j].isdigit():
                    two_digit = int(line[i] + line[j])
                    max_num = max(max_num, two_digit)

    print(f"Line {line_num}: max two-digit number = {max_num}")
    total += max_num

print(f"\nTotal sum: {total}")
