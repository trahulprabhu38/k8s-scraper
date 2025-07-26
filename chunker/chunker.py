import pandas as pd
import os
import math

def split_input_csv(input_path, num_chunks, output_dir):
    df = pd.read_csv(input_path)
    chunk_size = math.ceil(len(df) / num_chunks)
    os.makedirs(output_dir, exist_ok=True)

    for i in range(num_chunks):
        chunk = df[i * chunk_size: (i + 1) * chunk_size]
        chunk.to_csv(f"{output_dir}/chunk_{i}.csv", index=False)

    print(f"✅ Split into {num_chunks} chunks in '{output_dir}'")

split_input_csv("input.csv", 20, "input_chunks")
