# ------------- sim/strategies/curve_bypass.py -------------
from sim.strategies.strategy_base import Strategy
import traci

class CurveBypass(Strategy):
    def apply(self, conflict):
        vid = conflict['vehicle']
        # quick detour: reduce speed & lateral offset via angle hack
        traci.vehicle.setSpeed(vid, traci.vehicle.getSpeed(vid)*0.5)
        print(f"[Strategy] Curve bypass (speed halved) for {vid}")