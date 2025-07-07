# ------------- sim/strategies/emergency_decel.py -------------
from sim.strategies.strategy_base import Strategy

class EmergencyDecel(Strategy):
    def apply(self, conflict):
        vid = conflict['vehicle']
        traci.vehicle.setSpeed(vid, 0.0)
        print(f"[Strategy] Emergency decel applied to {vid}")