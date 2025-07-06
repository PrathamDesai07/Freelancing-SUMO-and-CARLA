# sim/events/slow_congestion.py
import traci
from sim.events.base_event import Event

class SlowCongestionEvent(Event):
    def __init__(self, params):
        super().__init__("slow_congestion", params)

    def trigger(self):
        edge = self.params.get("edge", "1.0.00")
        new_speed = self.params.get("speed", 5.0)
        traci.edge.setMaxSpeed(edge, new_speed)
        print(f"Event triggered: {self.name}")

