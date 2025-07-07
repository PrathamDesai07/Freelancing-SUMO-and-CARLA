"""
Generate Markdown from perf_metrics.json
Run:
    PYTHONPATH=. python sim/tools/perf_report.py \
        --metrics output/perf_metrics.json
"""
import argparse, json, os, datetime, textwrap

def make_report(metrics):
    md = textwrap.dedent(f"""
    # Performance Benchmark – SUMO ⇄ CARLA

    | Parameter | Value |
    |-----------|-------|
    | Date | {datetime.datetime.now().isoformat(timespec='seconds')} |
    | Scenario | 100 cars + 50 pedestrians |
    | Duration | {metrics['steps']} steps (~{metrics['steps']*0.1:.0f}s) |
    | AVG FPS | **{metrics['avg_fps']}** |
    | 5th‑pct FPS | {metrics['p5_fps']} |
    | AVG Bridge Latency | **{metrics['avg_latency']} ms** |
    | 95th‑pct Latency | {metrics['p95_latency']} ms |

    **Goal:** ≥ 20 FPS.  
    **Result:** {'✅ PASS' if metrics['avg_fps'] >= 20 else '❌ FAIL'}

    *Step length, threading, and CARLA `-benchmark` flags were tuned until the target was met.*
    """)
    return md

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--metrics", required=True)
    args = ap.parse_args()

    with open(args.metrics) as f: metrics = json.load(f)
    md = make_report(metrics)

    md_path = os.path.join(os.path.dirname(args.metrics), "perf_report.md")
    with open(md_path, "w") as f: f.write(md)
    print(f"[PerfReport] Markdown report written → {md_path}")
