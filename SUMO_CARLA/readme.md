# SUMO-CARLA Agent Spawning Platform 🚗🚶‍♀️🧠

[![Docker Build](https://github.com/your-username/sumo-carla-platform/actions/workflows/docker.yml/badge.svg)](https://github.com/your-username/sumo-carla-platform/actions/workflows/docker.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This project integrates agent-based simulation between **SUMO** (Simulation of Urban Mobility) and **CARLA** (Car Learning to Act), enabling dynamic spawning of vehicles and pedestrians with configurable behaviors, densities, and routes. It supports Docker deployment and CI/CD via GitHub Actions.

## 📋 Table of Contents

- [Features](#-features)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Configuration](#-configuration)
- [Docker Deployment](#-docker-deployment)
- [Local Development](#-local-development)
- [Testing](#-testing)
- [CI/CD](#-cicd)
- [Project Structure](#-project-structure)
- [Requirements](#-requirements)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

### 🚗 Vehicle Spawner
- Dynamically spawns vehicles based on YAML-configured distributions
- Vehicle types: `private`, `taxi`, `bus`
- Supports route assignment and behavior profiles:
  - **Aggressive**: Fast, impatient driving
  - **Normal**: Default driving profile
  - **Conservative**: Slower, cautious driving

### 🚶 Pedestrian Spawner
- Spawns pedestrians based on configurable density (people/m²)
- Automatically selects walkable edges
- Assigns random walk paths with arrival duration

### ⚙️ YAML-Based Configuration
```yaml
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
```

### 🧠 Simulation Orchestration
The `orchestrator.py` coordinates:
- SUMO startup
- Vehicle & pedestrian spawning
- Trigger-based events (e.g., congestion)
- Async CSV/Parquet logging
- Output saved to `output/` directory

### 🧾 Output Artifacts
```json
// output/sim_stats.json
{
  "vehicles": {
    "private": 60,
    "taxi": 10,
    "bus": 30
  },
  "pedestrians": 50
}
```

Logs per step saved in: `output/logs/agent_log_<timestamp>.csv`

## 🛠 Installation

### Prerequisites
- Python ≥ 3.8
- SUMO ≥ 1.4.0
- CARLA ≥ 0.9.15
- Docker (recommended for runtime)
- NVIDIA GPU (for CARLA)

### Install Python Dependencies
```bash
pip install -r requirements.txt
```

## 🚀 Quick Start

### Using Docker (Recommended)

1. **Build Docker Image**
```bash
docker build -t sim_orchestrator:latest .
```

2. **Run Simulation**
```bash
sudo docker run --rm -it --gpus all --net=host \
  -v $(pwd):/workspace \
  sim_orchestrator:latest \
  --config=config/defaults.yml \
  --net=xodr_sumo_carla_pipeline/demo_scene.net.xml \
  --route=sim/assets/route.rou.xml
```

### Local Development

1. **Start CARLA Server**
```bash
sudo docker run --rm -it --gpus all --privileged --net=host \
   --shm-size=2g \
   carlasim/carla:0.9.15 \
   bash -c "./CarlaUE4.sh -opengl -carla-server -nosound -RenderOffScreen -quality-level=Low"
```

2. **Convert .xodr to .net.xml**
```bash
netconvert --opendrive-files xodr_sumo_carla_pipeline/demo_scene.xodr \
           -o xodr_sumo_carla_pipeline/demo_scene.net.xml
```

3. **Run Simulation**
```bash
PYTHONPATH=. python sim/orchestrator.py \
  --config config/defaults.yml \
  --net xodr_sumo_carla_pipeline/demo_scene.net.xml \
  --route sim/assets/route.rou.xml
```

## ⚙️ Configuration

The simulation is configured via YAML files in the `config/` directory. Key parameters include:

- **Traffic Entities**: Number and distribution of vehicles and pedestrians
- **Behavior Profiles**: Driving characteristics for different agent types
- **Logging**: Output format and verbosity
- **Simulation**: Duration, time step, and other runtime parameters

Example configuration:
```yaml
simulation:
  duration: 3600  # seconds
  step_length: 0.1
  
traffic_entities:
  vehicles: 150
  pedestrians: 75
  pedestrian_density: 0.08
  
behavior_profiles:
  aggressive:
    speedFactor: 1.3
    impatience: 0.9
    tau: 0.5
```

## 🐳 Docker Deployment

### Dockerfile Highlights
- Base: `nvidia/cuda:12.4.0-runtime-ubuntu22.04`
- Entrypoint: `/usr/local/bin/run_sim.sh`
- Runs `orchestrator.py` with passed arguments
- GPU support for CARLA rendering

### Environment Variables
- `DISPLAY`: For GUI applications (optional)
- `CARLA_ROOT`: CARLA installation directory
- `SUMO_HOME`: SUMO installation directory

## 🧪 Testing

### Unit Tests
```bash
PYTHONPATH=. python sim/tests/test_spawners.py --config config/defaults.yml
```

### Integration Tests
```bash
# Run full simulation test
PYTHONPATH=. python sim/tests/test_integration.py
```

### Smoke Tests
```bash
# 30-second headless test
./run_sim.sh --config config/test.yml --duration 30
```

## 🔁 CI/CD

GitHub Actions workflow (`.github/workflows/docker.yml`) includes:
- Build and push Docker image on push/tag to main
- Run 30s headless smoke test using CARLA & SUMO
- Output FPS and runtime statistics
- Automated testing on multiple Python versions

## 📁 Project Structure

```
SUMO_CARLA/
├── sim/
│   ├── agents/              # Agent spawning logic
│   │   ├── vehicle_spawner.py
│   │   └── pedestrian_spawner.py
│   ├── config/              # Configuration files
│   │   ├── defaults.yml
│   │   └── test.yml
│   ├── events/              # Event handling
│   ├── tests/               # Unit and integration tests
│   ├── visualization/       # Visualization utilities
│   └── orchestrator.py      # Main simulation orchestrator
├── xodr_sumo_carla_pipeline/
│   └── demo_scene.xodr      # OpenDRIVE scene file
├── output/                  # Simulation outputs
│   ├── logs/
│   └── sim_stats.json
├── run_sim.sh              # Simulation runner script
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
└── .github/
    └── workflows/
        └── docker.yml     # CI/CD pipeline
```

## 📋 Requirements

| Component | Version |
|-----------|---------|
| Python    | ≥ 3.8   |
| SUMO      | ≥ 1.4.0 |
| CARLA     | ≥ 0.9.15|
| TraCI     | via pip |
| Docker    | Latest  |
| NVIDIA GPU| Required|

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup
```bash
# Clone the repository
git clone https://github.com/your-username/sumo-carla-platform.git
cd sumo-carla-platform

# Install development dependencies
pip install -r requirements-dev.txt

# Run pre-commit hooks
pre-commit install
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [SUMO](https://www.eclipse.org/sumo/) - Traffic simulation framework
- [CARLA](https://carla.org/) - Autonomous driving simulator
- [TraCI](https://sumo.dlr.de/docs/TraCI.html) - Traffic Control Interface

## 📞 Support

- 📧 Email: your-email@example.com
- 🐛 Issues: [GitHub Issues](https://github.com/your-username/sumo-carla-platform/issues)
- 📖 Documentation: [Wiki](https://github.com/your-username/sumo-carla-platform/wiki)

---

**Status Summary**
- ✅ Agent spawning logic (vehicle + pedestrian)
- ✅ Configurable YAML parameters
- ✅ Async logging to CSV/Parquet
- ✅ Headless CARLA recording
- ✅ Dockerfile + Entrypoint
- ✅ GitHub Actions for CI/CD
- ✅ Smoke test automation
