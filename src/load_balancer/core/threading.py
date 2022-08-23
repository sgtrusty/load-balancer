'''
 # SpinachSocket - a metric load balancer with multi-threading
 # Copyright (C) 2022  Santiago González <https://github.com/sgtrusty>
 #             ~ Assembled through trust in coffee. ~
 #
 # This program is free software; you can redistribute it and/or modify
 # it under the terms of the CC BY-NC-ND 4.0 as published by
 # the Creative Commons; either version 2 of the License, or
 # (at your option) any later version.
 #
 # This program is distributed in the hope that it will be useful,
 # but WITHOUT ANY WARRANTY; without even the implied warranty of
 # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 # CC BY-NC-ND 4.0 for more details.
 #
 # You should have received a copy of the CC BY-NC-ND 4.0 along
 # with this program; if not, write to the  Creative Commons Corp.,
 # PO Box 1866, Mountain View, CA 94042.
 #
'''
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