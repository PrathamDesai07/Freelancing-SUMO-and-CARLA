import yaml
import argparse
import sys

class ConfigLoader:
    def __init__(self, config_path, overrides=None):
        self.config = self._load_yaml(config_path)
        if overrides:
            self._apply_overrides(overrides)
        self._validate()

    @staticmethod
    def load(config_path, overrides=None):
        """Convenience method to return just the config dict"""
        return ConfigLoader(config_path, overrides).get()

    def _load_yaml(self, path):
        with open(path, 'r') as f:
            return yaml.safe_load(f)

    def _apply_overrides(self, overrides):
        for override in overrides:
            keys, value = override.split('=')
            keys = keys.split('.')
            d = self.config
            for k in keys[:-1]:
                d = d.setdefault(k, {})
            d[keys[-1]] = yaml.safe_load(value)

    def _validate(self):
        lane_width = self.config['network']['lane_width']
        if not (3.0 <= lane_width <= 3.5):
            raise ValueError(f"lane_width must be between 3.0 and 3.5 → got {lane_width}")

        vehicles = self.config['traffic_entities']['vehicles']
        if not (0 <= vehicles <= 100):
            raise ValueError(f"vehicles must be between 0 and 100 → got {vehicles}")

        step_length = self.config['simulation']['step_length']
        if step_length <= 0:
            raise ValueError(f"step_length must be > 0 → got {step_length}")

    def get(self):
        return self.config
