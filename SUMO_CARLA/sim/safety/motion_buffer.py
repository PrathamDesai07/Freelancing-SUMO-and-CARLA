# ------------- sim/safety/motion_buffer.py -------------
from collections import deque

class MotionBuffer:
    """Fixed-length buffer of (time, x, y) per entity for TTC/TTR calc."""
    def __init__(self, length=25):
        self.length = length
        self._data = {}

    def update(self, ent_id, t, pos):
        buf = self._data.setdefault(ent_id, deque(maxlen=self.length))
        buf.append((t, pos))

    def get_history(self, ent_id):
        return list(self._data.get(ent_id, []))