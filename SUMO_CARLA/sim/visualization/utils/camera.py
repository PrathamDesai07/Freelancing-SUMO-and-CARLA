# sim/visualization/utils/camera.py
import carla
def setup_spectator_camera(world, resolution):
    """Returns the spawned camera sensor."""
    bp_lib = world.get_blueprint_library()
    cam_bp = bp_lib.find("sensor.camera.rgb")
    cam_bp.set_attribute("image_size_x", str(resolution[0]))
    cam_bp.set_attribute("image_size_y", str(resolution[1]))
    cam_bp.set_attribute("fov", "90")

    spectator = world.get_spectator()
    loc     = spectator.get_transform().location + carla.Location(z=50)
    rot     = carla.Rotation(pitch=-90)

    cam = world.spawn_actor(cam_bp, carla.Transform(loc, rot))
    return cam
