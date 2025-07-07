import carla
import numpy as np
import cv2
import os
import time
from datetime import datetime

def record_topdown(duration=60, resolution=(800, 600), save_path="output/video", filename=None):
    client = carla.Client("localhost", 2000)
    client.set_timeout(10.0)
    world = client.get_world()

    blueprint_library = world.get_blueprint_library()
    camera_bp = blueprint_library.find('sensor.camera.rgb')
    camera_bp.set_attribute("image_size_x", str(resolution[0]))
    camera_bp.set_attribute("image_size_y", str(resolution[1]))
    camera_bp.set_attribute("fov", "90")

    spectator = world.get_spectator()
    transform = carla.Transform(carla.Location(x=0, y=0, z=50), carla.Rotation(pitch=-90))
    spectator.set_transform(transform)

    camera_transform = carla.Transform(carla.Location(x=0, y=0, z=50), carla.Rotation(pitch=-90))
    camera = world.spawn_actor(camera_bp, camera_transform, attach_to=spectator)

    os.makedirs(save_path, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = filename or f"topdown_{timestamp}.mp4"
    full_path = os.path.join(save_path, filename)

    print(f"[Recorder] Recording to {full_path} for {duration} seconds...")

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(full_path, fourcc, 20.0, resolution)

    frames = []

    def save_frame(image):
        array = np.frombuffer(image.raw_data, dtype=np.uint8)
        array = array.reshape((resolution[1], resolution[0], 4))
        frame_bgr = array[:, :, :3][:, :, ::-1]
        video_writer.write(frame_bgr)

    camera.listen(lambda image: save_frame(image))

    time.sleep(duration)

    camera.stop()
    video_writer.release()
    print("[Recorder] Recording complete.")

if __name__ == "__main__":
    record_topdown(duration=60)
