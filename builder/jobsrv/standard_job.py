#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import time,os,re,traceback,locale
import process, email, hook
from vcs import Vcs
from builder.jobmng.models import Build,Setting
from builder.jobsrv.util import StrUtil,FileUtil

LOG_FILE = "_topo_builder_log.txt"
host_name = ""

#定义两个全局变量，用于保存当前正在运行的job id，以及stop时需要kill的进程
global_job_running = -1
global_process_for_kill = ""

#取相对artifact的目录
def build_dir(job, build, dir=""):
    path=dir
    if dir.find(":") == -1:
        #相对路径，先要取得workspace路径
        jobdir=os.path.join(os.path.dirname(__file__), "../../artifact/" + str(job.id) + "/" + str(build.id))
        path=os.path.abspath(os.path.join(jobdir, dir))
    
    return path    

#取相对workspace的目录
def job_dir(job, dir=""):
    path=dir
    if dir.find(":") == -1:
        #相对路径，先要取得workspace路径
        jobdir=os.path.join(os.path.dirname(__file__), "../../workspace/" + str(job.id))
        path=os.path.abspath(os.path.join(jobdir, dir))
    
    return path    

#取得一条命令的执行对象和参数两个部分
def get_file_and_para(cmd):
    if not re.search('("[^"]*")(.*)', cmd) is None:
        #如果命令以双引号开头
        return (re.search('("[^"]*")(.*)', cmd).group(1), re.search('("[^"]*")(.*)', cmd).group(2))
    elif not re.search("('[^']*')(.*)", cmd) is None:
        #如果命令以单引号开头
        return (re.search("('[^']*')(.*)", cmd).group(1), re.search("('[^']*')(.*)", cmd).group(2))
    else:
        #否则的话，注意用*而不是+匹配总能匹配上，所以没有判断是否None
        return (re.search("([^ ]*)(.*)", cmd).group(1), re.search("([^ ]*)(.*)", cmd).group(2))
                 
#job_log用于记一个字符串到job的log文件中
def job_log(job, build, content, newline=False, screen=True):
    if screen:
        print content
    FileUtil.log(build_dir(job, build, LOG_FILE), content, newline)

def job_email(job, build, setting, ifSuccess=True):
    #host_name在下面赋值了，所以一定要加global指示，否则如果只引用，不改变，可以不加global
    global host_name
    if host_name == "":
        try:
            (host_name,errno) = process.get_run_output("hostname")
            host_name = host_name.replace("\r\n","")
        except:
            pass
    
    title = job.name
    if build.version != "":
        title += " version " + build.version        
    
    if  host_name != "":
        title += " build on " + host_name
    
    if build.success:
        title += " successful."
    else:    
        title += " fail, code:" + build.code
        if build.phrase != "":
            title += ", phrase:" + build.phrase
    
    text= "Please visit Topo Builder to get this build detail, The id is:" + str(build.id)
    if setting.server_url != "":
        text += ": " + setting.server_url + "/jobmng/" + str(job.id)
    
    try:   
        if ifSuccess and build.success and job.success_email != "":        
            email.send_email("noreply@topobuider.com", job.success_email, setting.smtp_server, setting.smtp_port,setting.smtp_username, setting.smtp_password, 
                                title,text, tls=setting.smtp_tls)

        if (not ifSuccess) and (not build.success) and (job.fail_email != ""):
            email.send_email("noreply@topobuider.com", job.fail_email, setting.smtp_server, setting.smtp_port,setting.smtp_username, setting.smtp_password, 
                            title,text, tls=setting.smtp_tls)
    except:
        print "send email fail"
                
#job命令执行前的处理，注意这里不要删除/修改workspace的文件，因为pre_job有可能决定不做build，那么
#上次的build结果不要受到影响，这样可以从workspace看到最后一次build的中间结果
def pre_job(job, context):
    #这个最先记录，这样统计的job执行时间比较准确
    print "pre_do_job:" + job.name
    context['starttime'] = time.time()
    
    #加载设置
    if len(Setting.objects.filter(key="key")) == 0:
        context['setting'] = Setting()
    else:
        context['setting'] = Setting.objects.filter(key="key")[0]
    
    #建立work目录
    if not os.path.exists(job_dir(job)):
        os.makedirs(job_dir(job))

    #调用用户的hook，如果返回False，就不往下做了
    print "call user hook:" + job.name
    if not hook.pre_job_hook(job, context):
        return False
           
    #如果定义了VCS，并且vcs上的版本无变化，那么不需要做下去了
    if job.vcs_type != 'none':
        print "check vcs:" + job.name
        context['vcsVer'] = check_vcs(job, context) 
        if context['vcsVer'] == '':
            return False
    
    return True

#做job的vcs版本目录同步, 注意所有目录会更新到同一版本(不一定是HEAD版本，而是最后修改版本）
def check_vcs(job, context):
    context['vcs'] = Vcs(job.vcs_type)
    
    #如果scheduler参数是全数字，相当于强制一个版本来做，否则不管是manual还是cron，都从服务器上检测
    if re.match(r"^\d+$",context['scheduler']) is None:
        doVcs = False
    else:
        return context['scheduler']
    
    #这个记录最新版本，因为有些目录虽然没有更新，但是它版本号很高，更新时要用统一的最高版本来更新        
    vcsVer = ''
    vcs = context['vcs']
    
    log= job_dir(job, LOG_FILE)    
    for view in job.vcs_set.all():
        vcs_user = view.vcs_user
        vcs_pass = view.vcs_pass
        work_copy=job_dir(job, view.work_copy)
        print "check vcs:" + work_copy
        #如果address指定了版本，那么只在本地work_copy没有的时候才触发构建
        if view.address.find("@") != -1:
            if not os.path.isdir(work_copy):
                doVcs=True
        elif view.trigger_type == 'yes':
            #有新版本时触发，那么需要比较版本head和base
            if os.path.isdir(work_copy):
                baseVer = vcs.get_work_ver(work_copy,vcs_user,vcs_pass)
                headVer = vcs.get_rep_ver(view.address,vcs_user,vcs_pass)
                vcsVer = vcs.get_new_ver(vcsVer, headVer)
                if baseVer != headVer:
                    doVcs=True
            else:
                doVcs=True
                vcsVer=vcs.get_new_ver(vcsVer, vcs.get_rep_ver(view.address, vcs_user, vcs_pass))    
        else:
            if view.trigger_type == 'forced':
                doVcs=True
                
            #不管是强制触发构建还是不触发，版本总是要刷新的    
            if os.path.isdir(work_copy):
                baseVer = vcs.get_work_ver(work_copy,vcs_user,vcs_pass)
                headVer = vcs.get_rep_ver(view.address,vcs_user,vcs_pass)
                vcsVer = vcs.get_new_ver(vcsVer, headVer)
            else:    
                vcsVer = vcs.get_new_ver(vcsVer, vcs.get_rep_ver(view.address, vcs_user, vcs_pass))
    
    if doVcs:            
        return vcsVer
    else:
        return ''                 

def do_vcs(job, build, context, vcsVer):    
    vcs = context['vcs']    
    log = build_dir(job, build, LOG_FILE)
    for view in job.vcs_set.all():
        work_copy = job_dir(job, view.work_copy)
        vcs_user = view.vcs_user
        vcs_pass = view.vcs_pass        
        #处理revert，clean不要做了，太危险，因为如果用户设错work copy可能导致整个磁盘文件被删
        #用户要做，可以在自己的脚本里做。
        if view.revert and os.path.isdir(work_copy):
            if vcs.revert(work_copy, vcs_user, vcs_pass, log=log) != 0:
                raise Exception('vcs ' + work_copy + ' revert error')
        
        #处理update，如果这个vcs的address指定了版本(比如@10)，就不更新了    
        if not os.path.isdir(work_copy):
            if vcs.get(view.address, work_copy, vcs_user, vcs_pass, ver=vcsVer, log=log) != 0:
                raise Exception('vcs ' + work_copy + ' checkout error')
        elif view.address.find("@") == -1:
            if vcs.update(work_copy, vcs_user, vcs_pass, ver=vcsVer, log=log) != 0:
                raise Exception('vcs ' + work_copy + ' update error')
            
            
#具体做job的过程
def do_job(job, context):
    build=context['build']

    #build dir应该不存在，如果存在，那么抛异常
    if os.path.exists(build_dir(job, build)):
        raise Exception('Build dir ' + build_dir(job, build) + " has already existed")
    else:    
        os.makedirs(build_dir(job, build))

    #从do_job开始记录log，所以先删除原有log
    if os.path.isfile(build_dir(job, build, LOG_FILE)):
        os.remove(build_dir(job, build,LOG_FILE))            
        
    #调用用户命令
    try:
        #调用用户hook
        hook.pre_do_job_hook(job, build, context, job_log)    
                        
        if job.vcs_type != 'none':
            do_vcs(job, build, context, context['vcsVer'])   
        
        #准备环境变量, 注意utf8要用编码处理一下，locale字符串(job_dir)就不需要了
        os.environ["topo_builder_job"]=job.name.encode(locale.getdefaultlocale()[1])
        os.environ["topo_builder_job_id"]=str(job.id)
        os.environ["topo_builder_build_id"]=str(build.id)
        os.environ["topo_builder_ver"]=build.version.encode(locale.getdefaultlocale()[1])
        os.environ["topo_builder_artifact"]=job_dir(job, job.artifact)
        
        #job.cmd不做job_dir处理，因为可能别是写python...，所以要求创建job的人这里就写绝对路径，或者path里可以找到的相对路径
        
        context['code'] = process.run(job.cmd, log=build_dir(job, build, LOG_FILE), 
                     dispTarget=True, cwd=job_dir(job, job.cmd_dir), sync=(job.type == "standard"), terminatable=True)

        build.artifact = str(job.id) + "/" + str(build.id) + "/"
        build.code = str(context['code']) #数据库里，这个是字符串，内存里是int，方便用户写大于小于
        build.save()
                                        
        #调用用户hook
        hook.post_do_job_hook(job, build, context, job_log)    
                                        
    except Exception, e:
        job_log(job, build, traceback.format_exc())
    finally:
        #移动整个artifact,如果是文件,直接移动到build目录下,如果是目录,移动整个目录
        job_log(job, build, "move artifact\r\n")
        if not StrUtil.empty_str(job.artifact):
            if os.path.exists( build_dir(job, build, job.artifact) ):
                #无论是文件还是目录,artifact都应该不存在
                raise Exception('Build artifact ' + job.artifact + " has already existed")
            else:                
                FileUtil.move_file_or_folder(job_dir(job, job.artifact), build_dir(job, build, job.artifact))    
            
    
#job命令执行后的一些处理
def post_job(job, context):    
    build = context['build']

    #duration
    build.duration = long(time.time() - context['starttime'])
    context['duration'] = build.duration
    
    #log     
    try:
        context['log']=file(build_dir(job, build, LOG_FILE), "rb").read()
    except:
        context['log']=''
 
    #将环境中的变量放到局部变量中，因为下面计算要用
    #这样用户在表达式中不用写context[], 直接用duration/code/phrase/log什么就可以了
    for key in context.iterkeys():
        #注意赋值是个statement，不是expression，所以用exec而不是eval
        exec(key + "= context['"+ key + "']")
                
    #求值phrase
    context['phrase'] = ''
    if not (job.phrase_exp is None or job.phrase_exp==''):
        try:
            #确保是utf-8字符串，否则save会出错，并锁住数据库
            context['phrase'] = eval(job.phrase_exp).decode("utf-8").encode("utf-8")
            build.phrase = context['phrase']
        except Exception, e:   
            print traceback.format_exc()
    
    #求值success
    phrase = context['phrase']       
    if not (job.success_exp is None or job.success_exp==''):
        try:
            build.success = eval(job.success_exp)
        except Exception, e:
            print traceback.format_exc()    
            
    build.save()          
                
    #发送成功邮件，失败邮件不在这里发
    job_email(job, build, context['setting'])    
                                        
def job_process(job, context):
    if pre_job(job, context):
        #pre_job返回值决定要不要做这次build，如果需要，则先构造一条关联的build记录
        build=Build(job=job, create_time=datetime.now(), success=False, duration=0, running=True, 
                             version='' if job.vcs_type == 'none' else context['vcsVer'])
        build.save()
        context['build']=build
        
        try:
            do_job(job, context)
            post_job(job, context)
        finally:
            #未知的异常，不再处理了，只是将build结束掉就好了 
            build.running=False
            build.save()
            job_email(job, build, context['setting'], ifSuccess=False)    

            #调用用户finish_cmd
            try:
                os.environ["topo_builder_build_duration"]=str(build.duration)
                os.environ["topo_builder_build_success"]=str(build.success)
                os.environ["topo_builder_build_phrase"]=build.phrase.decode("utf-8").encode(locale.getdefaultlocale()[1])
                if job.finish_cmd:
                    process.run(job.finish_cmd, log=build_dir(job, build, LOG_FILE), dispTarget=True, terminatable=True)
            except Exception, e:
                print traceback.format_exc()

            #调用用户hook
            try:
                hook.post_job_hook(job, build, context)
            except Exception, e:
                print traceback.format_exc()
    
#标准job的回调函数, 在调度队列里被调用,arg表示sceduler的类型：manual或crontab
#注意目前这个job是阻塞式的, 意味一个job在执行, 其他job不能得到执行
#将来可能支持多线程job,那么注意局部变量的使用
def standard_job_callback(job, arg):
    global global_job_running
    global global_process_for_kill
    print "schedule job:" + job.name
    
    context={}
    context['scheduler'] = arg
    try:
        global_job_running = job.id
        global_process_for_kill = job.process_for_kill
        job_process(job, context)
    finally:        
        global_job_running = -1
        global_process_for_kill = ""
        
    print "finish schedule"   
