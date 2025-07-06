# sim/events/base_event.py
class Event:
    def __init__(self, name, params=None):
        self.name = name
        self.params = params or {}

    def trigger(self):
        raise NotImplementedError("Subclasses must implement the trigger method")
