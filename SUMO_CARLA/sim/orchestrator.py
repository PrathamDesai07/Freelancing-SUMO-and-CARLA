# sim/orchestrator.py
import argparse
import json
import os
import time

import traci

from sim.config.loader import ConfigLoader
from sim.agents.vehicle_spawner import VehicleSpawner
from sim.agents.pedestrian_spawner import PedestrianSpawner
from sim.events.ghost_pedestrian import GhostPedestrianEvent
from sim.events.slow_congestion import SlowCongestionEvent
from sim.events.triggers import should_trigger

def run_simulation(config, net_file, route_file, max_steps=1000):
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
    print("Simulation started...")

    vehicle_spawner = VehicleSpawner(config)
    pedestrian_spawner = PedestrianSpawner(config)

    vehicle_counts = vehicle_spawner.spawn(total_count=100)
    pedestrian_count = pedestrian_spawner.spawn(net_file)

    step = 0
    while step < max_steps:
        traci.simulationStep()

        # Gather traffic data (e.g. average speed on known edge)
        try:
            avg_speed = traci.edge.getLastStepMeanSpeed("1.0.00")
        except traci.TraCIException:
            avg_speed = 0

        traffic_data = {"avg_speed": avg_speed}

        # Check all trigger types
        for trigger_type in ["random", "traffic"]:
            if should_trigger(trigger_type, traffic_data):
                if trigger_type == "random":
                    event = GhostPedestrianEvent({"edge": "1.0.00"})
                elif trigger_type == "traffic":
                    event = SlowCongestionEvent({"edge": "1.0.00"})
                event.trigger()

        step += 1

    traci.close()
    print("Simulation finished.")

    os.makedirs("output", exist_ok=True)
    with open("output/sim_stats.json", "w") as f:
        json.dump({
            "vehicles": vehicle_counts,
            "pedestrians": pedestrian_count
        }, f, indent=2)

    print("Output saved to: output/sim_stats.json")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--net", required=True)
    parser.add_argument("--route", required=True)
    args = parser.parse_args()

    config = ConfigLoader.load(args.config)
    run_simulation(config, args.net, args.route)

if __name__ == "__main__":
    main()
