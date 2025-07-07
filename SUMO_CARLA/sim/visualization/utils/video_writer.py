# sim/visualization/utils/video_writer.py
import cv2
import queue
import threading

class AsyncVideoWriter:
    def __init__(self, filename, resolution=(800, 600), fps=20):
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        self.writer = cv2.VideoWriter(filename, fourcc, fps, resolution)
        self.q = queue.Queue(maxsize=100)
        self.stop_flag = False
        self.t = threading.Thread(target=self._loop, daemon=True)
        self.t.start()

    def write(self, frame):
        try:
            self.q.put_nowait(frame)
        except queue.Full:
            # drop frame if queue is full
            pass

    def _loop(self):
        while not self.stop_flag or not self.q.empty():
            try:
                frame = self.q.get(timeout=0.5)
                self.writer.write(frame)
            except queue.Empty:
                continue

    def close(self):
        self.stop_flag = True
        self.t.join()
        self.writer.release()
