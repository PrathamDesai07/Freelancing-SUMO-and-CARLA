import traci
import sumolib
import os
import subprocess
import time

sumo_binary = "sumo"  # or "sumo-gui"
net_file = "simple.net.xml"
rou_file = "simple.rou.xml"

sumo_cmd = [sumo_binary, "-n", net_file, "-r", rou_file, "--step-length", "1.0"]

traci.start(sumo_cmd)

for step in range(10):
    print(f"Step {step}")
    traci.simulationStep()

traci.close()
