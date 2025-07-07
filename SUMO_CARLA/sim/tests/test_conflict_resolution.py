# ------------- sim/tests/test_conflict_resolution.py -------------
"""Spawn 2 vehicles + 1 pedestrian. Let them approach, detect conflict, resolve."""
import traci
import time

from sim.safety.conflict_detector import ConflictDetector
from sim.strategies.emergency_decel import EmergencyDecel
from sim.agents.vehicle_spawner import VehicleSpawner
from sim.agents.pedestrian_spawner import PedestrianSpawner
from sim.config.loader import ConfigLoader

SUMO_BINARY = "sumo"
NET = "xodr_sumo_carla_pipeline/demo_scene.net.xml"
ROUTE = "sim/assets/route.rou.xml"

cfg = {
    'history_steps': 20,
    'max_detect_dist': 20,
    'ttc_thresh': 3.0,
    'w_t': 0.7,
    'w_d': 0.3
}

def run():
    traci.start([SUMO_BINARY, "-n", NET, "-r", ROUTE, "--start"])
    detector = ConflictDetector(cfg)
    vehicle_spawner = VehicleSpawner(ConfigLoader.load("config/defaults.yml"))
    vehicle_spawner.spawn(2)
    PedestrianSpawner(ConfigLoader.load("config/defaults.yml")).spawn(NET)

    strategy = EmergencyDecel()

    step = 0
    while step < 200:
        traci.simulationStep()
        detector.update_buffers(step)
        conflicts = detector.detect(step)
        if conflicts:
            print(f"[TEST] Conflict detected at step {step}: {conflicts[0]}")
            strategy.apply(conflicts[0])
            break
        step += 1
        time.sleep(0.02)

    traci.close()

if __name__ == "__main__":
    run()
