from threading import Thread
import time
from utils import default_sleep_time

class Maintenance(Thread):
    def __init__(self, worker, sleep_time=default_sleep_time):
        super().__init__()
        self.worker = worker
        self.sleep_time = sleep_time  # do maintenance every @sleep_time seconds

    def run(self):
        while True:
            if self.worker.state.in_ring:
                self.worker.check_predecessor()
                self.worker.stabilize()
                self.worker.fix_finger()
            time.sleep(self.sleep_time)
