"""
Run: PYTHONPATH=. python sim/tests/performance_test.py \
         --config config/defaults.yml \
         --net   xodr_sumo_carla_pipeline/demo_scene.net.xml \
         --route sim/assets/route.rou.xml
"""

import argparse, json, os, time
import statistics as stats
import traci

from sim.config.loader import ConfigLoader
from sim.agents.vehicle_spawner import VehicleSpawner
from sim.agents.pedestrian_spawner import PedestrianSpawner

RESULTS_DIR = "output"
os.makedirs(RESULTS_DIR, exist_ok=True)

def run_test(cfg, net, route, sim_time=300):
    sumo_cmd = [cfg["sumo_binary"], "-n", net, "-r", route,
                "--step-length", str(cfg["simulation"]["step_length"]),
                "--start", "--no-step-log", "--time-to-teleport", "-1" ]
    traci.start(sumo_cmd)
    v_spawner = VehicleSpawner(cfg); p_spawner = PedestrianSpawner(cfg)

    v_spawner.spawn(100); p_spawner.spawn(net)

    fps_hist, latency_hist = [], []
    end_time = time.time() + sim_time
    while time.time() < end_time:
        t0 = time.perf_counter()
        traci.simulationStep()
        t1 = time.perf_counter()
        latency_hist.append((t1 - t0)*1000.0)      # ms
        fps_hist.append(1.0/(t1 - t0) if t1>t0 else 0)

    traci.close()
    return {
        "avg_fps"      : round(stats.mean(fps_hist), 2),
        "p5_fps"       : round(stats.quantiles(fps_hist, n=20)[0], 2),
        "avg_latency"  : round(stats.mean(latency_hist), 2),
        "p95_latency"  : round(stats.quantiles(latency_hist, n=20)[-1], 2),
        "steps"        : len(fps_hist)
    }

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config"); ap.add_argument("--net"); ap.add_argument("--route")
    ap.add_argument("--seconds", type=int, default=300)
    args = ap.parse_args()

    cfg = ConfigLoader.load(args.config)
    metrics = run_test(cfg, args.net, args.route, sim_time=args.seconds)

    out_json = os.path.join(RESULTS_DIR, "perf_metrics.json")
    with open(out_json, "w") as f: json.dump(metrics, f, indent=2)
    print(f"[PerfTest] metrics → {out_json}\n", json.dumps(metrics, indent=2))
