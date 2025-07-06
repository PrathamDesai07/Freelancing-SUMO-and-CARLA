#!/usr/bin/env bash
# Usage: sudo ./scene_import.sh demo_scene
set -e

SCENE=$1
SCENE_DIR="xodr_sumo_carla_pipeline"
XODR="${SCENE_DIR}/${SCENE}.xodr"
NET="${SCENE}.net.xml"
UDS="${SCENE_DIR}/${SCENE}.udatasmith"
CFG="${SCENE_DIR}/lane_cfg.yml"
TLS="${SCENE}.tll.xml"

echo "[scene_import] Step 1: convert XODR → NET"
python3 ${SCENE_DIR}/convert_xodr_to_net.py --xodr "$XODR" --out "$NET" --cfg "$CFG"

echo "[scene_import] Step 2: generate TLS file"
python3 ${SCENE_DIR}/generate_tls.py --cfg "${CFG}" --out "$TLS"

echo "[scene_import] Step 3: copy Datasmith"
python3 ${SCENE_DIR}/import_udatasmith.py --udatasmith "$UDS"

echo "[scene_import] ✔ Done. Outputs: $NET  $TLS  + assets in /opt/carla/ImportedScenes"
