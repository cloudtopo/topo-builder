#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scheduler import Scheduler
from event import Event
import process
import time

if __name__=="__main__":
    def log(line):
        flog.write(line)
    
    flog=file("_test.log", "wb")    
    print process.get_run_output("dir /s \\")