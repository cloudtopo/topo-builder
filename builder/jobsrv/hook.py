#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
hook
Copyright 2009 Cloudtopo
"""

"""
这个hook在job执行前被触发，一定会被执行。
参数：
  job：这个job变量
  context：这个job执行的上下文
返回：  
  如果返回True，job继续往下，
  如果返回False则job不再执行下去了。
"""
def pre_job_hook(job, context):
    return True

"""
这个hook在真正job执行前被触发
参数：
  job：这个job变量，可以使用其属性，比如name,state等
  build：这次构建的build变量，可以使用其属性，比如version等
  context：这次构建的上下文
  logger：可以在log中记录日志的logger变量, 这样使用logger(job, build, "test log\r\n")
返回：  
  返回值无意义
"""
def pre_do_job_hook(job, build, context, logger):        
    return

"""
这个hook在真正job执行后被触发，如果执行过程中有异常，这里不会被调用
参数：
  job：这个job变量，可以使用其属性，比如name,state等
  build：这次构建的build变量，可以使用其属性，比如version等
  context：这次构建的上下文
  logger：可以在log中记录日志的logger变量, 这样使用logger(job, build, "test log\r\n")
返回：  
  返回值无意义
"""
def post_do_job_hook(job, build, context, logger):
    return

"""
这个hook在job执行完后触发, 不论执行中是否异常，这个hook总被调用（post_do_job_hook和post_job_hook可能会都被调用）
参数：
  job：这个job变量，可以使用其属性，比如name,state等
  build：这次构建的build变量，可以使用其属性，比如version等
  context：这次构建的上下文
返回：  
  返回值无意义
"""
def post_job_hook(job, build, context):
    return
    