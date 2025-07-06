#!/usr/bin/env python3
import yaml
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: generate_tls.py <scene_name>")
        sys.exit(1)

    scene_name = sys.argv[1]
    output_file = f"{scene_name}.tll.xml"

    with open("/teamspace/studios/this_studio/SUMO_CARLA/xodr_sumo_carla_pipeline/lane_cfg.yml") as f:
        cfg = yaml.safe_load(f)

    cycle = cfg.get("default", {}).get("signal_cycle", [30, 5, 45])
    if len(cycle) < 3:
        cycle = [30, 5, 45]

    with open(output_file, "w") as f:
        f.write("<additional>\n")
        f.write(f'  <tlLogic id="TL0" type="static" programID="0" offset="0">\n')
        f.write(f'    <phase duration="{cycle[0]}" state="Gr"/>\n')
        f.write(f'    <phase duration="{cycle[1]}" state="yr"/>\n')
        f.write(f'    <phase duration="{cycle[2]}" state="rG"/>\n')
        f.write(f'  </tlLogic>\n')
        f.write("</additional>\n")
    print(f"[generate_tls] Wrote TLS file {output_file}")

if __name__ == "__main__":
    main()
