## File: patch_net_lanes.py

#!/usr/bin/env python3
"""Add extra lanes to every edge so that each direction has >= desired count."""
import argparse
import xml.etree.ElementTree as ET


def duplicate_lanes(net_path: str, lane_target: int):
    tree = ET.parse(net_path)
    root = tree.getroot()
    for edge in root.findall("edge"):
        for lane_dir in edge:
            if lane_dir.tag != "lane":
                continue
        # count existing lanes
        lanes = edge.findall("lane")
        if len(lanes) >= lane_target:
            continue
        last_lane = lanes[-1]
        for i in range(len(lanes), lane_target):
            new_lane = ET.SubElement(edge, "lane", last_lane.attrib)
            new_lane.set("id", f"{edge.attrib['id']}_{i}")
    tree.write(net_path)
    print(f"[patch_net_lanes] Patched lanes to {lane_target} in {net_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--net", required=True)
    parser.add_argument("--lanes", type=int, required=True)
    args = parser.parse_args()
    duplicate_lanes(args.net, args.lanes)

if __name__ == "__main__":
    main()

