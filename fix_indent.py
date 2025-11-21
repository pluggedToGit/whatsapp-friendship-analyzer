"""Fix indentation in simple_test.py"""

with open('simple_test.py', 'r') as f:
    lines = f.readlines()

# Find the try block (line 51, 0-indexed = 50)
# Everything from line 51 onwards until the except clause needs +4 spaces indent

output_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    
    # Lines 0-50: keep as is
    if i < 51:
        output_lines.append(line)
    # Line 51: the try: statement - keep as is
    elif i == 51:
        output_lines.append(line)
    # Lines 52-935: add 4 spaces if they start with non-whitespace or 4 spaces
    elif i >= 52 and i < 936:
        # Skip completely empty lines
        if line.strip() == '':
            output_lines.append(line)
        # Already has 8+ spaces - keep as is (already indented for try)
        elif line.startswith('        '):
            output_lines.append(line)
        # Has 4 spaces - add 4 more
        elif line.startswith('    ') and not line.startswith('        '):
            output_lines.append('    ' + line)
        # No indent - shouldn't happen in this block, but add 8 spaces
        else:
            output_lines.append('        ' + line)
    # Line 936: except clause - should align with try (4 spaces from for loop)
    elif i == 936:
        if 'except' in line:
            output_lines.append('        ' + line.strip() + '\n')
        else:
            output_lines.append(line)
    # Line 937+: inside except, need 8 spaces base + 4 more = 12 spaces total
    elif i >= 937:
        if line.strip() == '':
            output_lines.append(line)
        elif line.startswith('        '):
            output_lines.append('    ' + line)
        elif line.startswith('    '):
            output_lines.append('        ' + line)
        else:
            output_lines.append('            ' + line)
    
    i += 1

with open('simple_test.py', 'w') as f:
    f.writelines(output_lines)

print("Fixed indentation!")
