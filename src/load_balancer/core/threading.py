from concurrent.futures import ThreadPoolExecutor
import queue
from os import cpu_count

THREAD_COUNT={
    'Max': cpu_count(),
    'Overclock': None
}

class DisposableThreadPoolExecutor(ThreadPoolExecutor):
    def terminate(self, wait=True, *, cancel_futures=False):
        with self._shutdown_lock:
            self._shutdown = True
            if cancel_futures:
                # Drain all work items from the queue, and then cancel their
                # associated futures.
                while True:
                    try:
                        work_item = self._work_queue.get_nowait()
                    except queue.Empty:
                        break
                    if work_item is not None:
                        work_item.future.cancel()

            # Send a wake-up to prevent threads calling
            # _work_queue.get(block=True) from permanently blocking.
            self._work_queue.put(None)
        if wait:
            for t in self._threads:
                t.join()

class ThreadHandler:
    def __init__(self, policy=THREAD_COUNT['Overclock']):
        if (policy == THREAD_COUNT['Overclock']):
            self.executor = DisposableThreadPoolExecutor()
        else:
            self.executor = DisposableThreadPoolExecutor(max_workers=policy)

    def terminate(self):
        self.executor.terminate()

    def submit(self, task, args):
        self.executor.submit(task, args)