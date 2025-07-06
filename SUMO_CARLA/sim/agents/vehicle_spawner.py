# sim/agents/vehicle_spawner.py
import random
import traci

class VehicleSpawner:
    def __init__(self, config):
        self.vehicle_distribution = config["traffic_entities"]["vehicle_distribution"]
        self.behavior_profiles = config["traffic_entities"]["behavior_profiles"]
        self._defined_types = set()

    def _define_type_if_needed(self, type_id, params):
        if type_id in self._defined_types:
            return

        # Instead of copying, create from scratch using setParameter
        traci.vehicletype.setParameter(type_id, "accel", "2.6")
        traci.vehicletype.setParameter(type_id, "decel", "4.5")
        traci.vehicletype.setParameter(type_id, "sigma", "0.5")
        traci.vehicletype.setParameter(type_id, "length", "5.0")
        traci.vehicletype.setParameter(type_id, "minGap", "2.5")
        traci.vehicletype.setParameter(type_id, "maxSpeed", "27.8")
        traci.vehicletype.setParameter(type_id, "speedFactor", str(params["speedFactor"]))
        traci.vehicletype.setParameter(type_id, "impatience", str(params["impatience"]))

        self._defined_types.add(type_id)

    def spawn(self, total_count):
        counts = {
            v_type: int(total_count * pct / 100)
            for v_type, pct in self.vehicle_distribution.items()
        }

        vid = 0
        for v_type, n in counts.items():
            profile_name = random.choice(list(self.behavior_profiles.keys()))
            profile = self.behavior_profiles[profile_name]

            self._define_type_if_needed(v_type, profile)

            for _ in range(n):
                veh_id = f"veh_{vid}"
                traci.vehicle.add(veh_id, routeID="route0", typeID=v_type)
                vid += 1

        return counts
