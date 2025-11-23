#!/usr/bin/env python3
import re
import json
import os

# Read the app.ron file
with open(os.path.expanduser("~/Library/Application Support/yammanappaify/app.ron"), 'r') as f:
    content = f.read()

# Split by "assignments:[" to find each preset's assignments
parts = content.split("assignments:[")

# The first part doesn't have assignments, so skip it
# Extract the 5 assignments arrays
presets = ["wisetree", "blackhole", "cat", "cat2", "colorful"]
assignments_data = {}

for i, preset_name in enumerate(presets, start=1):
    if i < len(parts):
        # Get the assignments part
        assignments_text = parts[i]
        
        # Find the closing bracket - assignments end with "])"
        end_pos = assignments_text.find("])")
        if end_pos == -1:
            # Try just "]" if "])" not found
            end_pos = assignments_text.find("],")
            if end_pos == -1:
                continue
        
        # Extract just the numbers
        numbers_str = assignments_text[:end_pos]
        
        # Parse the numbers
        numbers = [int(x.strip()) for x in numbers_str.split(',') if x.strip().isdigit()]
        
        print(f"Found {len(numbers)} assignments for {preset_name}")
        assignments_data[preset_name] = numbers

# Save each preset's assignments to its JSON file (no spaces after commas)
for preset_name, assignments in assignments_data.items():
    output_file = f"presets/{preset_name}/assignments.json"
    with open(output_file, 'w') as f:
        # Write without spaces to match Rust parser expectations
        f.write('[' + ','.join(map(str, assignments)) + ']')
    print(f"Saved {output_file}")

print(f"\n✅ Extracted assignments for {len(assignments_data)} presets")
