# sim/events/ghost_pedestrian.py
import traci
from sim.events.base_event import Event

class GhostPedestrianEvent(Event):
    def __init__(self, params):
        super().__init__("ghost_pedestrian", params)

    def trigger(self):
        pid = self.params.get("id", "ghost_0")
        edge = self.params.get("edge", "1.0.00")
        duration = self.params.get("duration", 30)

        traci.person.add(pid, edgeID=edge, pos=0, depart=0)
        traci.person.appendWalkingStage(pid, edges=[edge], arrivalPos=30.0, duration=duration)
        print(f"Event triggered: {self.name}")
