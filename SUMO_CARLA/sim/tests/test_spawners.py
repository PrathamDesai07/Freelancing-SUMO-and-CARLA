## File: sim/tests/test_spawners.py

import json
import traci
from sim.config.loader import ConfigLoader
from sim.agents.vehicle_spawner import VehicleSpawner
from sim.agents.pedestrian_spawner import PedestrianSpawner

def run_test():
    config = ConfigLoader.load("config/defaults.yml")
    sumo_binary = "sumo"
    sumo_cmd = [sumo_binary, "-c", "sim/assets/simulation.sumocfg"]
    traci.start(sumo_cmd)
    
    vs = VehicleSpawner(config)
    ps = PedestrianSpawner(config)

    vehicle_counts = vs.spawn(100)
    pedestrian_count = ps.spawn("demo_scene.net.xml")

    result = {
        "vehicles": vehicle_counts,
        "pedestrians": pedestrian_count
    }
    with open("/teamspace/studios/this_studio/SUMO_CARLA/logs/spawn_log.json", "w") as f:
        json.dump(result, f, indent=2)

    traci.close()

if __name__ == "__main__":
    run_test()