# File: sim/tools/export_results.py

import pandas as pd
import argparse
import os

def export_log(dir_path, output_format="csv"):
    files = [f for f in os.listdir(dir_path) if f.endswith(".parquet") or f.endswith(".csv")]
    files.sort()
    dfs = []
    for f in files:
        path = os.path.join(dir_path, f)
        dfs.append(pd.read_parquet(path) if f.endswith(".parquet") else pd.read_csv(path))
    combined = pd.concat(dfs, ignore_index=True)
    output_path = os.path.join(dir_path, f"combined.{output_format}")
    if output_format == "csv":
        combined.to_csv(output_path, index=False)
    else:
        combined.to_parquet(output_path, index=False)
    print(f"[Export] Merged file written to: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", type=str, required=True, help="Directory of logged parquet/csv")
    parser.add_argument("--format", type=str, default="csv", choices=["csv", "parquet"])
    args = parser.parse_args()
    export_log(args.dir, args.format)
