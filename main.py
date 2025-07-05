"""
check_pipeline.py – Quick health check for CARLA + SUMO setup
---------------------------------------------------------------
✔ Verifies CARLA server is running and accessible on port 2000
✔ Verifies SUMO is installed and can bind to TraCI port 8813 using a dummy.sumocfg
"""

import socket
import subprocess
import time
import sys
from pathlib import Path

CARLA_PORT = 2000
SUMO_PORT = 8813

def wait_for_port(port, timeout=10):
    print(f"🔍 Waiting for port {port} ...", end="")
    t0 = time.time()
    while time.time() - t0 < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('localhost', port)) == 0:
                print(" ✅ Available")
                return True
        time.sleep(0.5)
    print(" ❌ Timed out")
    return False

def check_carla():
    try:
        import carla
        print("🐍 Python CARLA module found ✅")
    except ImportError:
        print("❌ 'carla' Python module not installed.")
        print("   Try: pip install carla==0.9.15")
        return

    if not wait_for_port(CARLA_PORT, timeout=10):
        print("❌ CARLA server not responding on port 2000")
        return

    try:
        client = carla.Client("localhost", 2000)
        client.set_timeout(5.0)
        world = client.get_world()
        print(f"🚗 Connected to CARLA: Map = {world.get_map().name}")
    except Exception as e:
        print(f"❌ Failed to connect to CARLA: {e}")

def check_sumo():
    dummy_cfg = Path("tests/sumocfg/dummy.sumocfg")
    if not dummy_cfg.exists():
        print("❌ Cannot find dummy.sumocfg at tests/sumocfg/")
        return

    try:
        print("🚦 Launching test SUMO instance using dummy.sumocfg ...")
        proc = subprocess.Popen(
            ["sumo", "-c", str(dummy_cfg), "--remote-port", str(SUMO_PORT)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        if wait_for_port(SUMO_PORT, timeout=5):
            print("✅ SUMO started and listening")
        else:
            print("❌ SUMO did not bind to port")
    except FileNotFoundError:
        print("❌ SUMO binary not found. Is it installed and in PATH?")
    finally:
        proc.terminate()
        proc.wait()

if __name__ == "__main__":
    print("🔧 Checking CARLA...")
    check_carla()
    print("\n🔧 Checking SUMO...")
    check_sumo()
