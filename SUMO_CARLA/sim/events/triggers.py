# sim/events/triggers.py
import random

def should_trigger(mode, traffic_data=None):
    if mode == "manual":
        return True
    elif mode == "poisson":
        return random.expovariate(1.0) < 1.0
    elif mode == "bernoulli":
        return random.random() < 0.2
    elif mode == "traffic" and traffic_data:
        return traffic_data.get("avg_speed", 10) < 5
    return False
