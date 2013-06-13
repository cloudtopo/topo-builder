#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
支持Cron时间格式的Event
    对Cron做了简单扩展, 支持秒
    支持两种格式的schedule定义, 一种是完全cron格式字符串, 一种是range格式
"""
from datetime import datetime, timedelta
import time,traceback

# Some utility classes / functions first
class AllMatch(set):
    """Universal set - match everything"""
    def __contains__(self, item): return True

#全局变量, 表示完全匹配
allMatch = AllMatch()

def conv_to_set(obj):  
    if isinstance(obj, (int,long)):
        # 如果只指定一个数字,那么也转换成一个列表
        return set([obj])  
    if not isinstance(obj, set):
        obj = set(obj)
    return obj

def conv_crontab_set(tab, rangemin, rangemax):
    obj=set()
    try:
        elements=tab.split(',')
        for e in elements:
            if len(e.split("/")) == 1:
                iter=1
            else:
                iter=int(e.split("/")[1])
            
            minmax=e.split("/")[0]
            if minmax=="*":
                min=rangemin
                max=rangemax            
            elif len(minmax.split("-")) ==1:
                min=int(minmax.split("-")[0])
                max=min
            else:
                min=int(minmax.split("-")[0])
                max=int(minmax.split("-")[1])
                #要考虑23-7这种颠倒的情况, cron是允许的
                if max < min:
                    max = max - rangemin + rangemax
            
            #注意python的range函数和cron的2-3/2在边界处理上是不一致的, max要加一
            for i in range(min, max+1, iter):
                if i > rangemax:
                    obj.add(i - rangemax + rangemin)
                else:    
                    obj.add(i)
    except Exception, e:
        print 'error in crontab element:'+ tab                
            
    return obj   
       
# The actual Event class
class Event(object):
    #按range来定义event, 比如Event(testaction, second=range(0,60,5), args=["task1"])
    def __init__(self, action, second=allMatch, min=allMatch, hour=allMatch, 
                               day=allMatch, month=allMatch, dow=allMatch, 
                                args=(), kwargs={}):
                                    
        self.seconds = conv_to_set(second)                            
        self.mins = conv_to_set(min)
        self.hours= conv_to_set(hour)
        self.days = conv_to_set(day)
        self.months = conv_to_set(month)
        self.dow = conv_to_set(dow)
        self.action = action
        self.args = args
        self.kwargs = kwargs
    
    #按cron格式来定义event, 比如Event(testaction, crontab="* 23-7/2 * * * *", args=["task1"])    
    def __init__(self, action, crontab, args=(), kwargs={}):
        tabs=crontab.split(' ')
        if len(tabs) == 6:                                    
            self.seconds = conv_crontab_set(tabs[0],0,59)                            
            self.mins = conv_crontab_set(tabs[1],0,59)
            self.hours= conv_crontab_set(tabs[2],0,23)
            self.days = conv_crontab_set(tabs[3],1,31)
            self.months = conv_crontab_set(tabs[4],1,12)
            self.dow = conv_crontab_set(tabs[5],0,6) #0表示星期天
        else:
            print "error in cron tab:" + crontab
            self.seconds = set()                            
            self.mins = set()
            self.hours= set()
            self.days = set()
            self.months = set()
            self.dow = set()
                
        self.action = action
        self.args = args
        self.kwargs = kwargs

    def matchtime(self, t):
        """Return True if this event should trigger at the specified datetime"""
        return ((t.second     in self.seconds) and
                (t.minute     in self.mins) and
                (t.hour       in self.hours) and
                (t.day        in self.days) and
                (t.month      in self.months) and
                (t.weekday()  in self.dow))

    def check(self, t):
        if self.matchtime(t):
            self.do()
    
    def do(self):
        try:
            self.action(*self.args, **self.kwargs)
        except Exception, e:
            #不能在执行action时异常，否则线程会不再执行
            print traceback.format_exc()
                        