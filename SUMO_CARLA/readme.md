SUMO-CARLA Agent Spawning Platform 🚗🚶‍♀️🧠
This project integrates agent-based simulation between SUMO (Simulation of Urban Mobility) and CARLA (Car Learning to Act), enabling dynamic spawning of vehicles and pedestrians with configurable behaviors, densities, and routes. It supports Docker deployment and CI/CD via GitHub Actions.

✅ Features Completed
1. 🚗 Vehicle Spawner
Dynamically spawns vehicles based on YAML-configured distributions.

Vehicle types: private, taxi, bus.

Supports route assignment and behavior profiles:

aggressive: fast, impatient

normal: default profile

conservative: slower, cautious

2. 🚶 Pedestrian Spawner
Spawns pedestrians based on configurable density (people/m²).

Automatically selects walkable edges.

Assigns random walk paths with arrival duration.

3. ⚙️ YAML-Based Configuration
yaml
Copy
Edit
traffic_entities:
  pedestrian_density: 0.05
  vehicles: 100
  pedestrians: 50
  vehicle_distribution:
    private: 60
    taxi: 10
    bus: 30
behavior_profiles:
  aggressive:
    speedFactor: 1.2
    impatience: 1.0
  normal:
    speedFactor: 1.0
    impatience: 0.5
  conservative:
    speedFactor: 0.8
    impatience: 0.2
logging:
  enabled: true
  format: csv
4. 🧠 Simulation Orchestration
orchestrator.py coordinates:

SUMO startup

Vehicle & pedestrian spawning

Trigger-based events (e.g., congestion)

Async CSV/Parquet logging

Output is saved to output/.

5. 🧾 Output Artifacts
json
Copy
Edit
// output/sim_stats.json
{
  "vehicles": {
    "private": 60,
    "taxi": 10,
    "bus": 30
  },
  "pedestrians": 50
}
Logs per step saved in:

output/logs/agent_log_<timestamp>.csv

🐳 Dockerized Deployment
✅ Dockerfile Highlights
Base: nvidia/cuda:12.4.0-runtime-ubuntu22.04

Entrypoint: /usr/local/bin/run_sim.sh

Runs orchestrator.py with passed arguments

🏗 Build Docker Image
bash
Copy
Edit
docker build -t sim_orchestrator:latest .
▶️ Run Simulation with Docker
bash
Copy
Edit
sudo docker run --rm -it --gpus all --net=host \
  -v $(pwd):/workspace \
  sim_orchestrator:latest \
  --config=config/defaults.yml \
  --net=xodr_sumo_carla_pipeline/demo_scene.net.xml \
  --route=sim/assets/route.rou.xml
🔁 GitHub Actions CI/CD
✅ .github/workflows/docker.yml Includes:
On push or tag to main:

Build + push Docker image

Run 30s headless smoke test using CARLA & SUMO

Outputs FPS and runtime stats

📁 Directory Structure
lua
Copy
Edit
SUMO_CARLA/
├── sim/
│   ├── agents/
│   ├── config/
│   ├── events/
│   ├── tests/
│   ├── visualization/
│   └── orchestrator.py
├── xodr_sumo_carla_pipeline/
│   └── demo_scene.xodr
├── output/
│   └── sim_stats.json
├── run_sim.sh
├── requirements.txt
├── Dockerfile
└── .github/
    └── workflows/docker.yml
🐍 Local Run (Non-Docker)
Start CARLA

bash
Copy
Edit
sudo docker run --rm -it --gpus all --privileged --net=host \
   --shm-size=2g \
   carlasim/carla:0.9.15 \
   bash -c "./CarlaUE4.sh -opengl -carla-server -nosound -RenderOffScreen -quality-level=Low"
Convert .xodr to .net.xml

bash
Copy
Edit
netconvert --opendrive-files xodr_sumo_carla_pipeline/demo_scene.xodr \
           -o xodr_sumo_carla_pipeline/demo_scene.net.xml
Run Simulation

bash
Copy
Edit
PYTHONPATH=. python sim/orchestrator.py \
  --config config/defaults.yml \
  --net xodr_sumo_carla_pipeline/demo_scene.net.xml \
  --route sim/assets/route.rou.xml
Unit Tests

bash
Copy
Edit
PYTHONPATH=. python sim/tests/test_spawners.py --config config/defaults.yml
📋 Requirements
Component	Version
Python	≥ 3.8
SUMO	≥ 1.4.0
CARLA	≥ 0.9.15
TraCI	via traci pip
Docker	Recommended for runtime

Install Python dependencies:

bash
Copy
Edit
pip install -r requirements.txt
✅ Status Summary
✅ Agent spawning logic (vehicle + pedestrian)

✅ Configurable YAML parameters

✅ Async logging to CSV/Parquet

✅ Headless CARLA recording

✅ Dockerfile + Entrypoint

✅ GitHub Actions for CI/CD

✅ Smoke test automation

