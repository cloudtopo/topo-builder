# -*- coding: utf-8 -*-
"""
Topo Builder Jobmng模型定义
可以在manage shell下通过from builder.jobmng.models import Job, Build来引入model并测试
"""
from django.db import models
from django.utils.translation import ugettext as _

#1.1的django
#from django.core.validators import RegexValidator

#枚举的定义
JobType = (
    ('standard', 'Standard'),
    ('asynchronous', 'Asynchronous'),
    ('external', 'External'),
)
JobState = (
    ('normal', 'Normal'),
    ('disable', 'Disable'),
    ('hide', 'Hide'),
)
VcsType = (
    ('subversion', 'Subversion'),
    ('none', 'None'),
)
VcsTriggerType = (
    ('yes', u'有新版本时触发构建'),
    ('forced', u'无条件触发构建'),
    ('no', u'不触发构建'),
)

class Setting(models.Model):
    #系统配置
    #这样配置一个不能改的key，保证最多一条记录
    key = models.CharField(max_length=200,default="key",editable=False,primary_key=True)
    #系统级别
    need_login=models.BooleanField(verbose_name=_("Need Login"), default=False,
                                    help_text=u"是否需要登录才能看到builder界面")
    server_url=models.CharField(verbose_name=_("Builder URL"), max_length=200, blank=True, 
                                help_text=u"Topo Builder的URL，这个会用在邮件通知中，比如http://your.buildserver.ip:8000")
    #smtp相关的设置
    smtp_server = models.CharField(verbose_name=_("SMTP Server"), max_length=200, blank=True,
                                    help_text=u"SMTP服务器地址，比如smtp.gmail.com，如果不配置则不会发送邮件")
    smtp_port = models.IntegerField(verbose_name=_("SMTP Port"), default=587,
                                    help_text=u"SMTP服务器端口号，比如Gmail就设置为587")
    smtp_username = models.CharField(verbose_name=_("SMTP Username"), max_length=200,blank=True,
                                     help_text=u"SMTP账号，比如yourname@gmail.com")
    smtp_password = models.CharField(verbose_name=_("SMTP Password"), max_length=200,blank=True,
                                       help_text=u"SMTP账号密码")
    smtp_tls = models.BooleanField(verbose_name=_("SMTP TLS"), 
                                    help_text=u"SMTP服务器是否需要TLS链接，比如对于Gmail，需要勾选上")
    
    def __unicode__(self):
        return "Topo Builder Setting" 
        
            
class Job(models.Model):
    #基本参数,对两种job都有用
    name= models.CharField(verbose_name=_("Name"), max_length=200, 
                            help_text=u"Job名称，显示时用，简明扼要的说明这个Job，比如'每日构建'")
    notes = models.TextField(verbose_name=_("Notes"), max_length=1024, blank=True,
                            help_text=u"Job说明，可以写较长的一段话说明这个job")
    create_time = models.DateTimeField(verbose_name=_("Create Time"))    
    type=models.CharField(verbose_name=_("Type"), max_length=32, default="standard",choices=JobType, 
                          help_text=u"一般选择standard类型，asynchronous是异步调度，external则用于存储外部的job")
    
    #如果是standardJob,那么下面的参数有意义
    #job是否暂时停止调度
    state=models.CharField(verbose_name=_("State"), max_length=32, default="normal", choices=JobState, 
                            help_text=u"一般选择normal，设置为disable、hide则暂时停止任务调度，设置为hide在首页上不显示")
    #调度cron格式的schedule
    schedule=models.CharField(verbose_name=_("Schedule"), max_length=100,blank=True,
                              help_text=u"Job的执行周期，使用类cron格式，在标准cron格式上增加一个秒字段,比如*/10 * * * * *表示每10秒调度一次，留空则不会被调度")
    #VCS类型,目前可支持SVN等, 注意一个vcs配置可以对多个目录，如果这里设置为None，那么设置了下面的vcs也没用。
    vcs_type=models.CharField(verbose_name=_("Version Control Type"), max_length=32, default="none", choices=VcsType,
                              help_text=u"目前只支持Subversion，如果没有配置版本库，选择None")
    #命令Job执行的命令
    cmd=models.CharField(verbose_name=_("Build Command"), max_length=1024,
                        help_text=u"要执行的构建命令或用户脚本，这里同时要写命令行参数，比如ping localhost -n 3，环境变量也会同时传入")
    #命令Job执行的当前目录
    cmd_dir=models.CharField(verbose_name=_("Build Command Directory"), max_length=1024, blank=True, 
                            help_text=u"执行命令的当前目录，如果写相对目录, 需要相对job的workspace目录, 也可以写绝对路径")
    #额外的待删除的进程，如果定义了，那么在stop任务时会杀掉这些进程，这里填写用分号分隔的多个进程名    
    process_for_kill=models.CharField(verbose_name=_("Kill Process On Stop"), max_length=1024, blank=True, 
                                      help_text=u"在停止构建时会杀掉的进程，这里填写用分号分隔的多个taskkill过滤器名,比如imagename eq firefox.exe")
    #输出文件,可以是一个文件或目录，空的话表示没有任何输出
    artifact = models.CharField(verbose_name=_("Artifact"), max_length=1024, blank=True, 
                                help_text=u"指定用于输出文件的目录，也是相对于job的workspace目录")
    #结果判定表达式, 可以用code/phrase/log/duration等变量来写一个返回boolean的表达式
    success_exp=models.CharField(verbose_name=_("Result Expression"), max_length=1024, default="True",
                                help_text=u"一个返回True/False的python表达式,可以使用的变量有code，duration，log，phrase，比如code==0 and log.find('success') != -1")
    #抓取phrase的正则表达式, 如果不定义, 那么phrase为空
    phrase_exp=models.CharField(verbose_name=_("Phrase Expression"), max_length=1024, blank=True, 
                                help_text=u"抓取一个表示构建结果描述信息字符串的python表达式，比如re.search('result:(.*)', log).group(1)")
    #成功时发送邮件通知对象
    success_email=models.CharField(verbose_name=_("Email On Success"), max_length=1024, blank=True, 
                                    help_text=u"构建成功时的邮件通知列表,可以用分号分隔多个邮件地址")
    #失败时发送邮件通知对象
    fail_email=models.CharField(verbose_name=_("Email On Failure"), max_length=1024, blank=True, 
                                help_text=u"构建失败时的邮件通知列表,可以用分号分隔多个邮件地址")
    
    #构建完成后要执行的用户命令或脚本
    finish_cmd=models.CharField(verbose_name=_("Finish Command"), max_length=1024, blank=True,
                                help_text=u"构建完成后要执行的用户命令或脚本，比如mycmd.bat，环境变量会传入构建参数")

    #Topo的build对象创建地址
    #topo_url_create_build=models.CharField(verbose_name=_("Topo URL for Create Build"), max_length=1024, blank=True,
    #                            help_text=u"用于在Topo中创建Build对象的URL，可以使用{{build.id}}来引用build的属性。比如http://192.168.1.1/html/client/topo/#groupType=group;groupUrl=10309;portletName=devmng;pageType=entity;dataModel=dmBuild;entityId=-1;f_name={{build.version}};f_repoTag={{build.version}};f_description={{job.name}};")

    #自定义命令
    custom_cmd1_name=models.CharField(verbose_name=_("Customer Command 1 Name"), max_length=1024, blank=True,
                                help_text=u"用户自定义命令1的名称")
    custom_cmd1_cmd=models.CharField(verbose_name=_("Custome Command 1 Cmd"), max_length=1024, blank=True,
                                help_text=u"用户自定义命令1的命令")
    custom_cmd1_path=models.CharField(verbose_name=_("Custome Command 1 Path"), max_length=1024, blank=True,
                                help_text=u"用户自定义命令1的执行路径")
    custom_cmd1_ret=models.CharField(verbose_name=_("Custome Command 1 Return"), max_length=10240, blank=True,
                                help_text=u"用户自定义命令1的返回")

    custom_cmd2_name=models.CharField(verbose_name=_("Customer Command 2 Name"), max_length=1024, blank=True,
                                help_text=u"用户自定义命令2的名称")
    custom_cmd2_cmd=models.CharField(verbose_name=_("Custome Command 2 Cmd"), max_length=1024, blank=True,
                                help_text=u"用户自定义命令2的命令")
    custom_cmd2_path=models.CharField(verbose_name=_("Custome Command 2 Path"), max_length=1024, blank=True,
                                help_text=u"用户自定义命令2的执行路径")
    custom_cmd2_ret=models.CharField(verbose_name=_("Custome Command 2 Return"), max_length=10240, blank=True,
                                help_text=u"用户自定义命令2的返回")

    custom_cmd3_name=models.CharField(verbose_name=_("Customer Command 3 Name"), max_length=1024, blank=True,
                                help_text=u"用户自定义命令3的名称")
    custom_cmd3_cmd=models.CharField(verbose_name=_("Custome Command 3 Cmd"), max_length=1024, blank=True,
                                help_text=u"用户自定义命令3的命令")
    custom_cmd3_path=models.CharField(verbose_name=_("Custome Command 3 Path"), max_length=1024, blank=True,
                                help_text=u"用户自定义命令3的执行路径")
    custom_cmd3_ret=models.CharField(verbose_name=_("Custome Command 3 Return"), max_length=10240, blank=True,
                                help_text=u"用户自定义命令3的返回")
    
    def __unicode__(self):
        return self.name 

            
class Vcs(models.Model):
    job = models.ForeignKey(Job, verbose_name=_("Job"), help_text=u"选择Vcs所属的job")
    name= models.CharField(verbose_name=_("Name"), max_length=200, help_text=u"Vcs名称，显示时用, 比如'客户端'")
    #VCS地址
    address = models.CharField(verbose_name=_("Vcs Address"), max_length=200, 
                                help_text=u"Vcs地址，用来得到相应的代码，比如svn://your-svn-server/prj/client")
    vcs_user = models.CharField(verbose_name=_("Vcs Username"), max_length=100, blank=True,
                                help_text=u"Vcs用户名，比如user")
    vcs_pass = models.CharField(verbose_name=_("Vcs Password"), max_length=100, blank=True,
                                help_text=u"Vcs用户密码，比如pass")
    #这里大部分情况下应该设置一个相对路径(相对于workspace), 对应VCS的本地路径
    work_copy = models.CharField(verbose_name=_("Work Copy Directory"), max_length=200, 
                                help_text=u"Vcs对应的本地路径，是一个相对目录，相对于job的Workspace，比如client")
    #设置这个路径触发编译的方式
    trigger_type = models.CharField(verbose_name=_("Trigger Type"), max_length=32, choices=VcsTriggerType, 
                                    help_text=u"触发类型，不管选择那种触发，在构建时目录都会和服务器同步")
    #设置等待时间主要是防止取到一个中间版本, 单位秒，目前不支持
    wait_time = models.IntegerField(verbose_name=_("Wait Time"), default=0, editable=False, blank=True)
    #如果设置这个,那么这个目录每次会清空,并从服务器重新获取
    clean= models.BooleanField(verbose_name=_("Clean On Build"), editable=False, 
                                help_text=u"如果设置这个选项,那么这个本地目录每次会被清空,然后再从服务器重新获取")
    #如果设置这个,那么这个目录每次会Revert到服务器版本,可以防止本地文件误改动导致下次构建的失败
    revert= models.BooleanField(verbose_name=_("Revert On build"), 
                                help_text=u"如果设置这个选项,那么这个本地目录每次会被Revert到服务器版本,这样可以防止本地文件误改动导致下次构建失败")
    
    def __unicode__(self):
        return self.job.name + " " + self.name 
    
class Build(models.Model):
    job = models.ForeignKey(Job)
    create_time = models.DateTimeField(verbose_name=_("Create Time"))
    #是否正在编译
    running=models.BooleanField(verbose_name=_("Running"), )
    #成功/失败
    success= models.BooleanField(verbose_name=_("Success"), )
    #返回code，之所以用char，是因为可以缺省为空，表示未知
    code=models.CharField(verbose_name=_("Return Code"), max_length=20, blank=True)
    #可以是一段字符串,表明构建的具体结果,比如编译失败,比如冒烟失败
    phrase=models.CharField(verbose_name=_("Phrase"), max_length=100, blank=True)
    #版本
    version=models.CharField(verbose_name=_("Version"), max_length=100, blank=True)
    #这次构建的耗时,单位秒
    duration=models.IntegerField(verbose_name=_("Duration"), )
    #构建的输出文件URL	这个应该指向构建服务器的一个URL,保存了这次构建的输出文件
    artifact = models.CharField(verbose_name=_("Artifact"), max_length=1024, blank=True)
    #是否是一个发布
    published=models.BooleanField(verbose_name=_("Published"), default=False)
    
    def __unicode__(self):
        return self.job.name + " " + self.version + " " + str(self.create_time)
        
