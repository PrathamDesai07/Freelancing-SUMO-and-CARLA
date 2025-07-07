# ------------- sim/strategies/strategy_base.py -------------
import abc
import traci

class Strategy(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def apply(self, conflict):
        pass