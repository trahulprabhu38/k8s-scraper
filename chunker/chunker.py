import os

input_file = "input.csv"
output_dir = "../input_chunks"
num_chunks = 580

# Ensure output folder exists
os.makedirs(output_dir, exist_ok=True)

# Read all lines
with open(input_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

header = lines[0]            # First line is the header
data_lines = lines[1:]       # All other lines are data

total_lines = len(data_lines)
base_size = total_lines // num_chunks
remainder = total_lines % num_chunks

start = 0
for i in range(num_chunks):
    end = start + base_size + (1 if i < remainder else 0)
    chunk = data_lines[start:end]
    
    with open(f"{output_dir}/input_chunk_{i}.csv", "w", encoding="utf-8") as out:
        out.write(header)           # Write the header first
        out.writelines(chunk)      # Then the chunk data
    
    start = end
