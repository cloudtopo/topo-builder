#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
进程相关函数封装
Copyright 2009 Cloudtopo
"""
import asyncprocess,sys,os

#多少次刷一次LOG
FLUSH_LOG_INTEVAL = 3

#正在运行的process的句柄
global_process_handle = -1

#注意在使用这个函数时,如果输出很多, 比如dir\s 可能导致内存消耗很大直到耗尽
def get_run_output(target, useCall=True, useShell=True, cwd=None):
    #好奇怪的解决方法，加shell=True可以保证所有的target都不会报异常，而且对于bat，也必须要用shell=True
    #加call是因为如果target是bat（比如ant），那么就必须有call才能通过后面得到returncode，否则总为0
    #用下面的os.system是不行的，因为这种方法得不到returncode
    #return os.system(target + " 2>&1 | tee -a _draco_integration.log")
    if useCall:
        target = "call " + target
    process = asyncprocess.Popen(target, shell=useShell, stdout=asyncprocess.PIPE, stderr=asyncprocess.STDOUT, cwd=cwd)
    (stdoutput,erroutput) = process.communicate()
    return (stdoutput,process.returncode)

def run(target, useCall=True, useShell=True, log=None, prtscr=True, dispTarget=True, cwd=None, sync=True, terminatable=False):
    #好奇怪的解决方法，加shell=True可以保证所有的target都不会报异常，而且对于bat，也必须要用shell=True
    #加call是因为如果target是bat（比如ant），那么就必须有call才能通过后面得到returncode，否则总为0
    #用下面的os.system是不行的，因为这种方法得不到returncode
    #return os.system(target + " 2>&1 | tee -a _draco_integration.log")
    
    global global_process_handle
    
    if log!=None:
        flog= file(log, "ab")
    
    try:    
        if dispTarget:
            if log != None:
                flog.write(target + "\r\n")
            if prtscr:
                print target
                
        if useCall:
            target = "call " + target
        
        process = asyncprocess.Popen(target, shell=useShell, stdout=asyncprocess.PIPE, stderr=asyncprocess.STDOUT, cwd=cwd)
        if terminatable:        
            global_process_handle = process.pid
        
        count=0    
        while True:
            if sync:
                #如果设置同步读取方式，使用同步方式来读取标准输出，同步是python subprocess的标准做法，但如果这个进程退出时留了子进程，这时会阻塞
                #process要输出本地locale的字符串，否则会异常
                buff = process.stdout.readline()
            else:
                #如果设置异步读取方式，使用异步方式来读取标准输出, 异步方式
                buff = process.asyncread(timeout=.5)
            
            if buff != '':
                count += 1
            
            if buff == '' and process.poll() != None: 
                break
            
            if log!=None and buff != '':
                flog.write(buff)
                if count % FLUSH_LOG_INTEVAL == 0:
                    flog.flush()
                
            if prtscr and buff != '':
                sys.stdout.write(buff)
           
        process.wait()
    
    finally: 
        global_process_handle = -1
           
        if log!=None:
            flog.close()
        
    return process.returncode

def Terminate(handle, extra_process="", deleteTree=True):
    #不能使用win32process.TerminateProcess，因为win32process.TerminateProcess不能中止进程的子进程。
    if handle is None:
        return None
        
    if deleteTree:        
        get_run_output("taskkill /F /T /PID " + str(handle), useCall=False)
    else:
        get_run_output("taskkill /F /PID " + str(handle), useCall=False)

    for process in extra_process.split(";"):
        if process != "":
            get_run_output('taskkill /F /FI "' + process + '"', useCall=False)
