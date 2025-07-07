#!/bin/bash

set -e

# Wait for CARLA
PORT=2000
echo "[run_sim] Waiting for CARLA server on localhost:$PORT..."
while ! nc -z localhost $PORT; do
  sleep 1
done

echo "[run_sim] CARLA detected!"

# Set environment variables
export SUMO_HOME=/usr/share/sumo
export PYTHONPATH=/workspace

# Default arguments
CONFIG="config/defaults.yml"
NET="xodr_sumo_carla_pipeline/demo_scene.net.xml"
ROUTE="sim/assets/route.rou.xml"

# Override from CLI args
for ARG in "$@"; do
  case $ARG in
    --config=*) CONFIG="${ARG#*=}" ;;
    --net=*)    NET="${ARG#*=}" ;;
    --route=*)  ROUTE="${ARG#*=}" ;;
  esac
  shift

done

python3 /workspace/sim/orchestrator.py \
  --config "/workspace/$CONFIG" \
  --net "/workspace/$NET" \
  --route "/workspace/$ROUTE"
