# sim/tests/test_events.py

import traci
import time

from sim.events.ghost_pedestrian import GhostPedestrianEvent
from sim.events.slow_congestion import SlowCongestionEvent
from sim.events.triggers import should_trigger  # This handles logic for triggering

SUMO_BINARY = "sumo"  # or "sumo-gui"
NET_FILE = "xodr_sumo_carla_pipeline/demo_scene.net.xml"
ROUTE_FILE = "sim/assets/route.rou.xml"

def start_sumo():
    traci.start([SUMO_BINARY, "-n", NET_FILE, "-r", ROUTE_FILE, "--start"])
    time.sleep(0.5)

def stop_sumo():
    traci.close()

def test_ghost_event():
    print("[TEST] Ghost Pedestrian Event")
    params = {
        "edge": "1.0.00",
        "count": 3,
        "duration": 30
    }
    event = GhostPedestrianEvent(params)
    event.trigger()
    print("✓ Ghost Pedestrian Event Triggered\n")

def test_slow_congestion():
    print("[TEST] Slow Congestion Event")
    params = {
        "edge": "1.0.00",
        "slowdown": 0.3,
        "duration": 50
    }
    event = SlowCongestionEvent(params)
    event.trigger()
    print("✓ Slow Congestion Event Triggered\n")

def test_traffic_state_trigger():
    print("[TEST] Traffic-State Driven Trigger")
    step = 0
    max_steps = 100

    while step < max_steps:
        traci.simulationStep()
        try:
            avg_speed = traci.edge.getLastStepMeanSpeed("1.0.00")
        except traci.TraCIException:
            avg_speed = 0

        traffic_data = {"avg_speed": avg_speed}

        if should_trigger("traffic", traffic_data):
            event = SlowCongestionEvent({
                "edge": "1.0.00",
                "slowdown": 0.2,
                "duration": 40
            })
            event.trigger()
            print("✓ Traffic-State Triggered Slow Congestion Event\n")
            break  # Only trigger once for test
        step += 1

if __name__ == "__main__":
    start_sumo()
    try:
        test_ghost_event()
        test_slow_congestion()
        test_traffic_state_trigger()
    finally:
        stop_sumo()
