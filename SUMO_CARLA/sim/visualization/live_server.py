# sim/visualization/live_server.py
"""Single‑file Flask application that:
1. Streams a CARLA top‑down MJPEG feed (live headless draw)
2. Serves a simple HTML/JS frontend with play/pause + slider
3. Implements /replay endpoint that renders trajectory frames on‑demand
   from a combined CSV log (original vs. intervened trajectories).

Run:
    PYTHONPATH=. python sim/visualization/live_server.py \
        --csv output/logs/<timestamp>/combined.csv \
        --host 0.0.0.0 --port 8080

Dependencies: flask, carla, opencv‑python, pandas, matplotlib
"""

import argparse
import io
import os
import threading
import time
from datetime import datetime

import carla
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, Response, send_file, render_template_string, request

################################################################################
# Live camera stream (MJPEG)
################################################################################

class LiveCameraStreamer:
    def __init__(self, resolution=(800, 600)):
        self.width, self.height = resolution
        self.frame_lock = threading.Lock()
        self.current_frame = None  # BGR uint8
        self._init_carla_camera(resolution)

    def _init_carla_camera(self, resolution):
        client = carla.Client("localhost", 2000)
        client.set_timeout(10.0)
        world = client.get_world()

        bp_lib = world.get_blueprint_library()
        cam_bp = bp_lib.find("sensor.camera.rgb")
        cam_bp.set_attribute("image_size_x", str(resolution[0]))
        cam_bp.set_attribute("image_size_y", str(resolution[1]))
        cam_bp.set_attribute("fov", "90")

        spectator = world.get_spectator()
        transform = spectator.get_transform()
        transform.location.z += 50
        transform.rotation.pitch = -90

        camera = world.spawn_actor(cam_bp, transform)
        camera.listen(self._on_image)
        self.camera = camera
        print("[LiveCameraStreamer] camera started")

    def _on_image(self, image):
        array = np.frombuffer(image.raw_data, dtype=np.uint8)
        array = array.reshape((image.height, image.width, 4))[:, :, :3]
        frame_bgr = cv2.cvtColor(array, cv2.COLOR_RGB2BGR)
        with self.frame_lock:
            self.current_frame = frame_bgr

    def mjpeg_generator(self):
        while True:
            with self.frame_lock:
                frame = self.current_frame.copy() if self.current_frame is not None else None
            if frame is not None:
                ret, jpeg = cv2.imencode('.jpg', frame)
                if ret:
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
            time.sleep(0.05)  # 20 FPS max

################################################################################
# Trajectory replay renderer
################################################################################

class TrajectoryReplay:
    """Render PNG for a given time‑step showing original vs intervened paths."""

    def __init__(self, csv_path):
        if not os.path.isfile(csv_path):
            raise FileNotFoundError(csv_path)
        print(f"[Replay] loading {csv_path}")
        self.df = pd.read_csv(csv_path)
        self.max_step = int(self.df["step"].max())

    def render_step(self, step):
        step_df = self.df[self.df["step"] == step]
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.set_aspect("equal")
        ax.set_xlim(self.df["x"].min() - 5, self.df["x"].max() + 5)
        ax.set_ylim(self.df["y"].min() - 5, self.df["y"].max() + 5)
        ax.set_title(f"Step {step}")
        ax.axis("off")

        for _, row in step_df.iterrows():
            color = "red" if row["entity_type"] == "vehicle" else "blue"
            ax.plot(row["x"], row["y"], marker="o", color=color)

        buf = io.BytesIO()
        plt.savefig(buf, format="png", bbox_inches="tight")
        plt.close(fig)
        buf.seek(0)
        return buf

################################################################################
# Flask App
################################################################################

def create_app(csv_path=None, host="0.0.0.0", port=8080):
    app = Flask(__name__)

    # Live camera
    camera_streamer = LiveCameraStreamer()

    # Optional replay
    replay = TrajectoryReplay(csv_path) if csv_path else None

    # ---------------- HTML template ----------------
    HTML = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8" />
      <title>CARLA Top‑Down Viewer</title>
      <style>
        body { font-family: Arial, sans-serif; background:#111; color:#eee; text-align:center }
        #stream { border:2px solid #444; }
        #slider { width: 80%; }
      </style>
    </head>
    <body>
      <h2>Live Top‑Down View (MJPEG)</h2>
      <img id="stream" src="/stream" width="800" height="600" />

      {% if replay %}
      <h2>Trajectory Replay</h2>
      <input type="range" id="slider" min="0" max="{{ max_step }}" value="0" />
      <button onclick="play()">Play</button>
      <button onclick="pause()">Pause</button><br/>
      <img id="replay" src="/replay?step=0" width="600" height="600" />
      {% endif %}

      <script>
        let playing = false;
        let step = 0;
        const maxStep = {{ max_step if replay else 0 }};
        const slider = document.getElementById('slider');
        const replayImg = document.getElementById('replay');

        if (slider) {
          slider.oninput = () => {
            step = slider.value;
            replayImg.src = `/replay?step=${step}&_=${Date.now()}`;
          };
        }

        function play() {
          playing = true;
        }
        function pause() {
          playing = false;
        }

        setInterval(() => {
          if (playing && step < maxStep) {
            step++;
            slider.value = step;
            replayImg.src = `/replay?step=${step}&_=${Date.now()}`;
          }
        }, 200);
      </script>
    </body>
    </html>
    """

    # ---------------- routes ----------------------
    @app.route("/stream")
    def stream():
        return Response(camera_streamer.mjpeg_generator(), mimetype="multipart/x-mixed-replace; boundary=frame")

    if replay:
        @app.route("/replay")
        def replay_png():
            step = int(request.args.get("step", 0))
            step = max(0, min(step, replay.max_step))
            buf = replay.render_step(step)
            return send_file(buf, mimetype="image/png")

    @app.route("/")
    def index():
        return render_template_string(HTML, replay=bool(replay), max_step=replay.max_step if replay else 0)

    return app

################################################################################
# CLI
################################################################################

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", help="CSV log for trajectory replay", default=None)
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()

    app = create_app(csv_path=args.csv)
    print(f"[LiveServer] running on http://{args.host}:{args.port}")
    app.run(host=args.host, port=args.port, debug=False, threaded=True)
