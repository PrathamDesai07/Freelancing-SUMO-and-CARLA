## File: import_udatasmith.py
#!/usr/bin/env python3
import argparse
import shutil
import os

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--udatasmith', required=True, help='Path to .udatasmith file')
    return parser.parse_args()

def main():
    args = parse_args()
    dst = f"/opt/carla/ImportedScenes/{os.path.basename(args.udatasmith)}"
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    print(f"[import_udatasmith] Copying {args.udatasmith} → {dst}")
    shutil.copy(args.udatasmith, dst)

if __name__ == '__main__':
    main()