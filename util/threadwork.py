#!/usr/bin/python
# -*- coding:utf-8 -*-

import time
from Queue import Queue
from threading import Thread

class Worker(Thread):

    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()
    
    def run(self):
        while True:
            func, args, kargs = self.tasks.get()
            try:
                func(*args, **kargs)
            except Exception, e:
                print e
            self.tasks.task_done()

class ThreadPool:

    def __init__(self, num_threads):
        self.tasks  = Queue(num_threads)
        for _ in range(num_threads):
            Worker(self.tasks)

    def add_task(self, func, *args, **kargs):
        self.tasks.put((func, args, kargs))

    def wait_completion(self):
        self.tasks.join()


def print_time(hello, world):
    time.sleep(2)
    print str(time.time()) + hello + world

if __name__ == '__main__':
    pool = ThreadPool(5)
    for i in range(10):
        pool.add_task(print_time,'world','hello')
    pool.wait_completion()
    
