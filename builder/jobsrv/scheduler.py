#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
实现一个thread scheduler, 可周期性加载事件列表
"""

from datetime import datetime, timedelta
from Queue import Queue
import threading,time

class Scheduler(object):
    def __init__(self, loadevents, loadtime=timedelta(seconds=5)):
        #这个running只是控制crontab的event是否运行，手动event总是可以运行的
        self.running=False
        self.loadevents = loadevents
        self.reload_events = False
        self.loadtime = loadtime
        self.lock = threading.Lock()
        self.queue = Queue(1)
        self.thread = threading.Thread(target=self._run)
        #当设置为True, 就不用管这个线程了, 当主线程退出, 这个线程会自动退出, 
        #否则即使主线程退出, 进程仍会等待这个线程而不会退出
        self.thread.setDaemon(True)
        self.thread.start()

    #暂时还没用
    def _acquire_lock(self):
        self.lock.acquire()

    def _release_lock(self):
        self.lock.release()

    def is_running(self):
        return self.running
                  
    def start(self):
        self.running = True
            
    def stop(self):
        self.running = False
    
    def put(self, item, block=False, timeout=3):
        self.queue.put(item, block, timeout)
            
    def reload_events(self):
        self.reload_events = True
                            
    def _run(self):
        #开始运行时加载事件列表, 注意考虑到多线程的情况, 这里变量用局部变量
        events = self.loadevents()
        lastload=datetime.now()
        
        #线程主循环
        while True:
            #按秒调度
            time.sleep(1)
            
            #处理一次性事件
            while not self.queue.empty():
                self.queue.get().do()
            
            if self.running:    
                #处理cron事件
                for e in events:
                    #每次check都重新去datetime now, 这样可以在上次event执行后得到修正后的时间
                    e.check(datetime(*datetime.now().timetuple()[:6]))
               
                #检查是否需要加载事件, 每分钟加载一次
                if (datetime.now() - lastload > self.loadtime) or self.reload_events:
                    events = self.loadevents()
                    lastload=datetime.now()
                    self.reload_events = False