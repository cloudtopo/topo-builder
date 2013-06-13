#!/usr/bin/env python
# -*- coding: utf-8 -*-

from builder.jobmng.models import Job, Build, Setting
from builder.jobsrv.scheduler import Scheduler
from builder.jobsrv.event import Event
from builder.jobsrv import standard_job

jobSch = None

#loadevents从数据库中加载可调度的job, 返回events列表, event是可被schedule调度的对象
#测试时可返回..Event(testaction, second=range(0,60,5), args=["task1"])
def _loadevents():
    #使用局部变量job_list, 可以防止queryset的缓存，但如果loadevents每分钟调用一次，还是可能会job修改后要等一分钟才看到效果
    jobs = Job.objects.all()
    events=[]
    
    #如果有新触发的job
    for job in jobs:
        if job.type!="external" and job.state=="normal" and job.schedule:
            events.append(Event(standard_job.standard_job_callback, crontab=job.schedule, args=[job, "crontab"]))
        
    return events
        
def startserver():    
    global jobSch
    if jobSch is None:
        jobSch=Scheduler(_loadevents)
            
    jobSch.start()
    
def stopserver():
    global jobSch
    if not jobSch is None:
        jobSch.stop()

