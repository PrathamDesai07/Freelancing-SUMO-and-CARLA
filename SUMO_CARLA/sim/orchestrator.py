# sim/orchestrator.py
import argparse
import json
import os
import time
from datetime import datetime

import traci

from sim.config.loader import ConfigLoader
from sim.agents.vehicle_spawner import VehicleSpawner
from sim.agents.pedestrian_spawner import PedestrianSpawner
from sim.events.ghost_pedestrian import GhostPedestrianEvent
from sim.events.slow_congestion import SlowCongestionEvent
from sim.events.triggers import should_trigger

# NEW ▶ async logger
try:
    from sim.logging.async_logger import AsyncLogger
except ImportError:
    AsyncLogger = None   # fallback if module not present


# --------------------------------------------------
def run_simulation(config, net_file, route_file, max_steps=1000):
    """
    Main simulation loop.
    """
    sumo_binary = config["sumo_binary"]
    sumo_cmd = [
        sumo_binary,
        "-n", net_file,
        "-r", route_file,
        "--start",
        "--no-step-log",
        "--time-to-teleport", "-1"
    ]

    traci.start(sumo_cmd)
    print("Simulation started…")

    # Spawners
    vehicle_spawner = VehicleSpawner(config)
    pedestrian_spawner = PedestrianSpawner(config)

    vehicle_counts = vehicle_spawner.spawn(total_count=100)
    pedestrian_count = pedestrian_spawner.spawn(net_file)

    # ── Async logger setup ──────────────────────────
    log_cfg = config.get("logging", {})
    logger = None
    if log_cfg.get("enabled", False) and AsyncLogger:
        logger = AsyncLogger(
            output_dir="output/logs",
            flush_steps=log_cfg.get("flush_steps", 50),
            file_format=log_cfg.get("format", "parquet").lower()
        )
        print("[AsyncLogger] Enabled")

    # ── Main loop ───────────────────────────────────
    for step in range(max_steps):
        traci.simulationStep()

        # 1) Aggregate traffic data for event triggers
        try:
            avg_speed = traci.edge.getLastStepMeanSpeed("1.0.00")
        except traci.TraCIException:
            avg_speed = 0.0
        traffic_data = {"avg_speed": avg_speed}

        # 2) Trigger events if needed
        for trigger_type in ("random", "traffic"):
            if should_trigger(trigger_type, traffic_data):
                event = (GhostPedestrianEvent if trigger_type == "random"
                         else SlowCongestionEvent)({"edge": "1.0.00"})
                event.trigger()

        # 3) Build entity snapshots → logger
        if logger:
            snapshots = []
            for vid in traci.vehicle.getIDList():
                x, y = traci.vehicle.getPosition(vid)
                snapshots.append({
                    "step": step,
                    "entity_id": vid,
                    "entity_type": "vehicle",
                    "x": x, "y": y,
                    "speed": traci.vehicle.getSpeed(vid),
                    "edge_id": traci.vehicle.getRoadID(vid),
                    "lane_id": traci.vehicle.getLaneID(vid),
                })
            for pid in traci.person.getIDList():
                x, y = traci.person.getPosition(pid)
                snapshots.append({
                    "step": step,
                    "entity_id": pid,
                    "entity_type": "pedestrian",
                    "x": x, "y": y,
                    "speed": traci.person.getSpeed(pid),
                    "edge_id": traci.person.getRoadID(pid),
                    "lane_id": traci.person.getLaneID(pid),
                })
            logger.queue_step(snapshots)

    # ── Shutdown ────────────────────────────────────
    traci.close()
    if logger:
        logger.close()
    print("Simulation finished.")

    # Save summary
    os.makedirs("output", exist_ok=True)
    with open("output/sim_stats.json", "w") as f:
        json.dump({
            "vehicles": vehicle_counts,
            "pedestrians": pedestrian_count
        }, f, indent=2)
    print("Output saved to: output/sim_stats.json")


# --------------------------------------------------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--net", required=True)
    parser.add_argument("--route", required=True)
    parser.add_argument("--steps", type=int, default=1000)
    args = parser.parse_args()

    config = ConfigLoader.load(args.config)
    run_simulation(
        config=config,
        net_file=args.net,
        route_file=args.route,
        max_steps=args.steps
    )


if __name__ == "__main__":
    main()
