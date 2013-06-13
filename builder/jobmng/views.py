#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time, re, urllib
import shutil
from django.template import RequestContext, loader
from django.http import HttpResponse,HttpResponseRedirect
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.utils.translation import ugettext as _
from django.conf import settings
from builder.jobmng.models import Job, Build, Setting
from builder.jobsrv.scheduler import Scheduler
from builder.jobsrv.event import Event
from builder.jobsrv import standard_job
from builder.jobsrv import process
from builder.jobsrv.standard_job import job_dir
from builder.jobsrv.server import jobSch


def _load_setting():
    if len(Setting.objects.filter(key="key")) == 0:
        return Setting()
    else:
        return Setting.objects.filter(key="key")[0]

def _load_common_props(request):
    setting = _load_setting()    
    
    auto_refresh = request.GET.get('refresh', '')
    if auto_refresh=='' or auto_refresh.lower()=='false':
        auto_refresh = False
    else:
        auto_refresh = True    

    pageno = request.GET.get('pageno', '')
    if re.match("[0-9]+",pageno):
        pageno = int(pageno)
        if pageno < 1:
            pageno = 1
    else:
        pageno = 1

    pagesize = request.GET.get('pagesize', '')
    if re.match("[0-9]+",pagesize):
        pagesize = int(pagesize)
        if pagesize < 10:
            pagesize = 10
    else:
        pagesize = 10
            
    if jobSch is None:
        running = False
    else:
        running = jobSch.is_running()
    
    app_description = settings.APP_DESCRIPTION
    return (setting, auto_refresh, pageno, pagesize, running, app_description)

def index(request):
    (setting, auto_refresh, pageno,pagesize,running, app_description) =  _load_common_props(request)           
    job_list = Job.objects.all()
    #对于每个job,加载其最后一次的编译结果
    build_list=[]
    for job in job_list:
        if len(job.build_set.order_by('-create_time')) > 0:
            build = job.build_set.order_by('-create_time')[0]
        else:
            build=Build()
            build.job=job
        build.job_builds_count = job.build_set.count()
        build_list.append(build)    
        
    t = loader.get_template('jobs_index.html')
    
    #使用RequestContext代替Context，就可以在模板中使用user变量
    c = RequestContext(request, {
        'job_list': job_list,
        'build_list': build_list,
        'auto_refresh': auto_refresh,
        'running': running,
        'job_running': standard_job.global_job_running,
        'app_description': app_description,
        'process_running': process.global_process_handle
    })
    return HttpResponse(t.render(c))
    
def _get_utf8(v):
    if isinstance(v,unicode):
        return v.encode("utf-8")
    elif isinstance(v,str):
        return v
    else:
        return str(v)       

def detail(request, job_id):
    (setting, auto_refresh, pageno, pagesize, running, app_description) =  _load_common_props(request)
    try:
        job = Job.objects.filter(id=job_id).get()
    except:
        job = None
        build_list = None

    #使用pagination接口取得分页数据
    if job!=None:
        build_list_all=job.build_set.order_by("-create_time")
        paginator = Paginator(build_list_all, pagesize)
        
        #如果请求的page不对，取第一页
        try:
            build_list = paginator.page(pageno)
        except (EmptyPage, InvalidPage):
            build_list = paginator.page(1)
    
    t = loader.get_template('jobs_detail.html')
    c = RequestContext(request, {
        'job': job,
        'build_list': build_list,
        'auto_refresh': auto_refresh,
        'pageno': pageno,
        'pagesize': pagesize,
        'running': running,
        'job_running':standard_job.global_job_running,
        'app_description': app_description,
        'process_running': process.global_process_handle
      })
    return HttpResponse(t.render(c))

def startserver(request):
    jobSch.start()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', "/"))    
    
def stopserver(request):
    jobSch.stop()
    
    #重现view/subprocess的bug的方法，下面两行代码
    #import subprocess
    #process = subprocess.Popen("ping localhost -n 5", shell=True)
     
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', "/"))

def reload(request, job_id):
    jobSch.reload_events()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', "/"))

#手动调度job的处理接口    
def dojob(request, job_id):
    try:
        job = Job.objects.filter(id=job_id).get()
    except:
        job = None
            
    if job is None:
        return HttpResponse(_('Can not find the job'))

    try:
        #手动job还是要遵循vcs策略的       
        jobSch.put(Event(standard_job.standard_job_callback, crontab=job.schedule, args=[job, "manual"]))
        #如果用 return HttpResponseRedirect("/")， 太快了，看不到新的状态，另外也可能会触发view和subprocess的bug，变通的方法是用一个比较快速的response
        #return HttpResponseRedirect("/")
        return HttpResponse(_('Trig job ok'))
    except:                
        return HttpResponse(_('Can not trig job now'))
        
#强制调度job并制定vcs的处理接口    
def forcejob(request, job_id, vcs_id):
    try:
        job = Job.objects.filter(id=job_id).get()
    except:
        job = None
            
    if job is None:
        return HttpResponse(_('Can not find the job'))

    if re.match(r"^\d+$",vcs_id) is None:
        return HttpResponse(_('You must specify a number as vcs id'))

    try:
        #手动job还是要遵循vcs策略的       
        jobSch.put(Event(standard_job.standard_job_callback, crontab=job.schedule, args=[job, vcs_id]))
        
        #如果用 return HttpResponseRedirect("/jobmng/" + job_id)， 太快了，看不到新的状态，另外也可能会触发view和subprocess的bug，变通的方法是用一个比较快速的response
        #return HttpResponseRedirect("/jobmng/" + job_id)
        return HttpResponse(_('Force job ok'))
    except:                
        return HttpResponse(_('Can not force job now'))    
       
#Cancel当前运行job    
def canceljob(request):
    print "Cancel", process.global_process_handle, standard_job.global_process_for_kill
    if process.global_process_handle == -1:              
        return HttpResponse(_('No running job process now'))
    else:
        process.Terminate(process.global_process_handle, standard_job.global_process_for_kill)
        return HttpResponseRedirect("/")                
        
def delete(request, job_id, build_ids):
    #现在admin也不是superuser，所以这里要用staff来判断
    if not request.user.is_staff:
        return HttpResponse(_('Please login to do this'))
    
    for build_id in build_ids.split("_"):    
        try:
            build = Build.objects.filter(id=build_id).get()
            if build.published:
                continue
        except:
            build = None
         
            
        if build is None:
            return HttpResponse(_('Can not find the build'))
        else:    
            build.delete()        
            try:
                job_id = build.job.id
                shutil.rmtree("../artifact/" + str(job_id) + "/" + str(build_id))
            except:
                pass
                
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', "/jobmng/" + str(job_id)))        
        
def clearjob(request,job_id):
    #现在admin也不是superuser，所以这里要用staff来判断
    if not request.user.is_staff:
        return HttpResponse(_('Please login to do this'))
        
    try:
        job = Job.objects.filter(id=job_id).get()
    except:
        job = None
            
    if job is None:
        return HttpResponse(_('Can not find the job'))
    else:
        for build in job.build_set.all():
            if not build.published:
                build.delete()        
                try:
                    shutil.rmtree("../artifact/" + str(job_id) + "/" + str(build.id))
                except:
                    pass    
                    
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', "/jobmng/" + str(job_id)))
    
def publish(request, build_id):
    try:
        build = Build.objects.filter(id=build_id).get()
    except:
        build = None
        
    if build is None:
        return HttpResponse(_('Can not find the build'))
    else:
        if build.published:
            build.published = False
        else:
            build.published = True
                
        build.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', "/jobmng/" + str(build.job.id)))
        
def trigcmd(request, job_id, build_id, cmd_id):
    return HttpResponse('<html><head><meta http-equiv="refresh" content="1;url=/jobmng/execcmd/' 
            + job_id + '/' + build_id + '/' + cmd_id +'"></head><body>wait...</body>')
    

def execcmd(request, job_id, build_id, cmd_id):
    #现在admin也不是superuser，所以这里要用staff来判断    
    #if not request.user.is_staff:
    #    return HttpResponse(_('Please login to do this'))
        
    try:
        build = Build.objects.filter(id=build_id).get()
    except:
        build = None
    
    job = build.job    
    if build is None:
        return HttpResponse(_('Can not find the build'))
            
    if cmd_id == '1':
        cmd_name = job.custom_cmd1_name
        cmd_cmd  = job.custom_cmd1_cmd
        cmd_path = job.custom_cmd1_path
        cmd_ret = job.custom_cmd1_ret
    elif cmd_id == '2':
        cmd_name = job.custom_cmd2_name
        cmd_cmd  = job.custom_cmd2_cmd
        cmd_path = job.custom_cmd2_path
        cmd_ret = job.custom_cmd2_ret
    elif cmd_id == '3':
        cmd_name = job.custom_cmd3_name
        cmd_cmd  = job.custom_cmd3_cmd
        cmd_path = job.custom_cmd3_path
        cmd_ret = job.custom_cmd3_ret
    else:
        return HttpResponse(_('Custom cmd should be 1~3'))   
        
    if cmd_cmd == '':
        return HttpResponse(_('Custom cmd can not execute'))
        
    vars = re.findall("{{(.*?)}}", cmd_cmd)
    for var in vars:
        try:
            transvar = eval(var)
        except:
            transvar = '####'
        cmd_cmd = cmd_cmd.replace("{{" + var + "}}", transvar)

    vars = re.findall("{{(.*?)}}", cmd_path)
    for var in vars:
        try:
            transvar = eval(var)
        except:
            transvar = '####'    
        cmd_path= cmd_path.replace("{{" + var + "}}", transvar)

    process.run(cmd_cmd, dispTarget=True, cwd=job_dir(job, cmd_path))
    if cmd_ret == "":
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', "/jobmng/" + str(job_id)))
    else:
        return HttpResponse(cmd_ret)
        