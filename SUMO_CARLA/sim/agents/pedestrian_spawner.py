import traci
import random

class PedestrianSpawner:
    def __init__(self, config):
        self.density = config['traffic_entities']['pedestrian_density']

    def compute_area(self, net_file):
        # Dummy area for example; replace with proper parsing if needed
        return 1000.0  # in m²

    def get_pedestrian_edges(self):
        """
        Return list of edge IDs where at least one lane allows pedestrians.
        """
        pedestrian_edges = set()

        for lane_id in traci.lane.getIDList():
            if ":":  # Skip internal lanes like ":gneJ1_0"
                continue
            try:
                allowed_classes = traci.lane.getAllowed(lane_id)
                if 0x08 in allowed_classes:  # 0x08 is pedestrian class
                    edge_id = lane_id.rsplit("_", 1)[0]
                    pedestrian_edges.add(edge_id)
            except traci.TraCIException:
                continue

        return list(pedestrian_edges)



    def spawn(self, net_file):
        area = self.compute_area(net_file)
        total_peds = int(area * self.density)

        pedestrian_edges = self.get_pedestrian_edges()
        if not pedestrian_edges:
            print("[PedestrianSpawner] No pedestrian-friendly edges found!")
            return 0

        for i in range(total_peds):
            pid = f"ped_{i}"
            edge = random.choice(pedestrian_edges)
            try:
                traci.person.add(pid, edgeID=edge, pos=0, depart=0)
                traci.person.appendWalkingStage(pid, edges=[edge], arrivalPos=30.0, duration=30)
            except traci.TraCIException as e:
                print(f"[PedestrianSpawner] Failed to spawn {pid} on {edge}: {e}")
                continue

        return total_peds
