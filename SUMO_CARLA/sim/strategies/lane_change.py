# ------------- sim/strategies/lane_change.py -------------
from sim.strategies.strategy_base import Strategy
import traci

class LaneChange(Strategy):
    def apply(self, conflict):
        vid = conflict['vehicle']
        try:
            lane_idx = traci.vehicle.getLaneIndex(vid)
            traci.vehicle.changeLane(vid, 1-lane_idx, 50)
            print(f"[Strategy] Lane change for {vid}")
        except traci.TraCIException:
            print(f"[Strategy] Lane change failed for {vid}")