# ------------- sim/safety/conflict_detector.py -------------
import math
import traci
from sim.safety.motion_buffer import MotionBuffer
from sim.safety.cost_function import risk_score

class ConflictDetector:
    """Detect vehicle–pedestrian or vehicle–vehicle conflicts via overlap & TTC."""
    def __init__(self, cfg):
        self.buf = MotionBuffer(length=cfg.get('history_steps', 25))
        self.cfg = cfg

    # -------------------------------------------------- #
    # Helpers                                            #
    # -------------------------------------------------- #
    def _euclidean(self, a, b):
        return math.hypot(a[0]-b[0], a[1]-b[1])

    def _ttc(self, v_rel, d):
        # simple TTC = dist / relSpeed  (avoid zero div)
        return d / max(abs(v_rel), 1e-3)

    # -------------------------------------------------- #
    def update_buffers(self, t):
        """Store latest positions for all vehicles + persons."""
        for vid in traci.vehicle.getIDList():
            self.buf.update(vid, t, traci.vehicle.getPosition(vid))
        for pid in traci.person.getIDList():
            self.buf.update(pid, t, traci.person.getPosition(pid))

    def detect(self, t):
        """Return list of conflict dicts."""
        conflicts = []
        veh_ids = traci.vehicle.getIDList()
        ped_ids = traci.person.getIDList()
        # vehicle–pedestrian
        for v in veh_ids:
            v_pos = traci.vehicle.getPosition(v)
            v_speed = traci.vehicle.getSpeed(v)
            for p in ped_ids:
                p_pos = traci.person.getPosition(p)
                dist = self._euclidean(v_pos, p_pos)
                if dist > self.cfg['max_detect_dist']:
                    continue
                ttc = self._ttc(v_speed, dist)
                if ttc < self.cfg['ttc_thresh']:
                    score = risk_score(ttc, dist, self.cfg['w_t'], self.cfg['w_d'])
                    conflicts.append({
                        'type': 'veh-ped',
                        'vehicle': v,
                        'pedestrian': p,
                        'distance': dist,
                        'ttc': ttc,
                        'score': score
                    })
        return sorted(conflicts, key=lambda x: x['score'], reverse=True)
