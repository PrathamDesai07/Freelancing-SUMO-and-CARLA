import os

# Define the folder structure
folders = [
    "/teamspace/studios/this_studio/Freelancing-SUMO-and-CARLA/maps",
    "/teamspace/studios/this_studio/Freelancing-SUMO-and-CARLA/net",
    "/teamspace/studios/this_studio/Freelancing-SUMO-and-CARLA/routes",
    "/teamspace/studios/this_studio/Freelancing-SUMO-and-CARLA/configs",
    "/teamspace/studios/this_studio/Freelancing-SUMO-and-CARLA/scripts",
    "/teamspace/studios/this_studio/Freelancing-SUMO-and-CARLA/logs"
]

def create_folders():
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"[+] Created: {folder}")

if __name__ == "__main__":
    create_folders()
    print("\n✅ Folder setup complete.")
