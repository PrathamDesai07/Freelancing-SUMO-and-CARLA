import carla

def test_connection(host='localhost', port=2000, timeout=10):
    try:
        print(f"[INFO] Connecting to CARLA at {host}:{port}...")
        client = carla.Client(host, port)
        client.set_timeout(timeout)

        world = client.get_world()
        print(f"[SUCCESS] Connected to world: {world.get_map().name}")

        blueprint_library = world.get_blueprint_library()
        print(f"[INFO] Found {len(blueprint_library)} blueprints.")

        vehicle_bp = blueprint_library.filter('vehicle.*')[0]
        print(f"[INFO] Example vehicle blueprint: {vehicle_bp.id}")

        print("[SUCCESS] CARLA connection test passed!")
    except Exception as e:
        print(f"[ERROR] Failed to connect to CARLA: {e}")

if __name__ == "__main__":
    test_connection()
