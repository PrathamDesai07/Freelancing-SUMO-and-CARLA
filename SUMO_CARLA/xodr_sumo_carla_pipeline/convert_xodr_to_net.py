#!/usr/bin/env python3
"""Convert <scene>.xodr → <scene>.net.xml and pass basic lanewidth.
If lane_count > 1 we'll patch the .net.xml afterwards (SUMO ≥1.18 removed the
old --opendrive.add-lane-count flag)."""
import argparse
import subprocess
import yaml
from pathlib import Path


def parse_cfg(cfg_path: Path):
    cfg = {
        "lanewidth": 3.5,
        "lanes": 1,
    }
    if cfg_path.exists():
        user = yaml.safe_load(cfg_path.read_text())
        cfg.update({
            "lanewidth": user.get("lane", {}).get("width", cfg["lanewidth"]),
            "lanes": user.get("lane", {}).get("count", cfg["lanes"]),
        })
    return cfg


def build_cmd(xodr: str, net_out: str, lane_width: float):
    return [
        "netconvert",
        "--opendrive-files", xodr,
        "--output-file", net_out,
        "--default.lanewidth", str(lane_width),
        "--no-warnings",
    ]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--xodr", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--cfg", default="lane_cfg.yml")
    args = ap.parse_args()

    cfg = parse_cfg(Path(args.cfg))
    cmd = build_cmd(args.xodr, args.out, cfg["lanewidth"])
    print("[convert_xodr_to_net]", " ".join(cmd))
    subprocess.run(cmd, check=True)

    # Patch lane count if needed
    if cfg["lanes"] > 1:
        subprocess.run(["python3", "patch_net_lanes.py", "--net", args.out,
                        "--lanes", str(cfg["lanes"])], check=True)

if __name__ == "__main__":
    main()
