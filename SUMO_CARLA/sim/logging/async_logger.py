# sim/logging/async_logger.py
import os
import pandas as pd
from datetime import datetime
from collections import defaultdict

class AsyncLogger:
    def __init__(self, output_dir="output/logs", flush_steps=50, file_format="parquet"):
        self.output_dir = output_dir
        self.flush_steps = flush_steps
        self.format = file_format.lower()
        self.step_buffer = []
        self.write_count = 0
        self.current_dir = self._create_timestamp_dir()

        os.makedirs(self.current_dir, exist_ok=True)

    def _create_timestamp_dir(self):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        return os.path.join(self.output_dir, timestamp)

    def queue_step(self, step_data):
        self.step_buffer.extend(step_data)
        if len(self.step_buffer) >= self.flush_steps:
            self._flush()

    def _flush(self):
        if not self.step_buffer:
            return

        df = pd.DataFrame(self.step_buffer)
        filename = f"run_{self.write_count + 1:04d}.{self.format}"
        filepath = os.path.join(self.current_dir, filename)

        if self.format == "parquet":
            df.to_parquet(filepath, index=False)
        elif self.format == "csv":
            df.to_csv(filepath, index=False)
        else:
            raise ValueError(f"Unsupported log format: {self.format}")

        print(f"[Logger] Flushed {len(self.step_buffer)} records to {filepath}")
        self.write_count += 1
        self.step_buffer.clear()

    def close(self):
        self._flush()
