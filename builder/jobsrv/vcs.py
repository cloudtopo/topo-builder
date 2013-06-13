#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
VCS相关函数封装
Copyright 2009 Cloudtopo
"""
import re,os
import process
from util import StrUtil, FileUtil

class Vcs:
    
    def __init__(self, type):
        if type != "subversion":
            raise Exception(type + " not supported now")             
        
        self.type=type
    
    def get_new_ver(self, ver1, ver2):
        if ver1== 'HEAD' or ver2=='HEAD':
            return 'HEAD'
            
        if ver1 == '':
            return ver2
        elif ver2 == '':
            return ver1
        
        return str(max(int(ver1), int(ver2)))
    
    def _get_svn_para(self, user, password):
        if password is None:
            password = ''
            
        if user is None or user == '':
            return " --trust-server-cert --non-interactive"
        else:
            return ' --username ' + StrUtil.quote(user) + ' --password ' + StrUtil.quote(password) + ' --trust-server-cert --non-interactive'
            
    #get用于初次将文件从svn中取出            
    def get(self, address, work_copy, user, password, ver="HEAD", log=None):
        if  os.path.exists(work_copy):
            raise Exception(work_copy + " has exist")
        
        if (address.find("@") == -1):
            return process.run("svn checkout -r " + ver + " " + StrUtil.quote(address) + " " + StrUtil.quote(work_copy) + self._get_svn_para(user, password), log=log)
        else:
            return process.run("svn checkout " + StrUtil.quote(address) + " " + StrUtil.quote(work_copy) + self._get_svn_para(user, password), log=log)
    
    def get_work_ver(self, work_copy, user, password, log=None):
        (baseOutput,errno) = process.get_run_output("svn info -r BASE " + StrUtil.quote(work_copy) + self._get_svn_para(user, password))
        FileUtil.log(log, baseOutput)
        if errno != 0:
            raise Exception("get version of " + work_copy + " error")

        if re.search("Last Changed Rev: ([0-9]+)", baseOutput) is None:
            baseVer = re.search("\xd7\xee\xba\xf3\xd0\xde\xb8\xc4\xb5\xc4\xb0\xe6\xb1\xbe: ([0-9]+)", baseOutput).group(1)
        else:
            baseVer = re.search("Last Changed Rev: ([0-9]+)", baseOutput).group(1)
            
        return baseVer
    
    #传入一个仓库地址，得到最后修改的版本
    #注意这里不用svn info了，因为对于一个刚copy的分支，svn info得到的可能将是主干上最后一个修改的版本（只有那个目录本身可以看到copy那个版本）
    #所以这里用log命令代替了
    def get_rep_ver(self, rep, user, password, log=None):
        (headOutput,errno) = process.get_run_output("svn log -q -l 1 " + StrUtil.quote(rep) + self._get_svn_para(user, password))
        FileUtil.log(log, headOutput)
        
        if errno != 0:
            raise Exception("get version of " + rep + " error")
        
        #注意这地方要处理中英文版本，所以要识别GB码的‘版本’和‘ Revision’
        headVer = re.search("r([0-9]+) \|", headOutput).group(1)
        return headVer
        
    def check(self, work_copy, address, user, password, log=None):
        baseVer = self.get_work_ver(work_copy, user, password, log)
        headVer = self.get_rep_ver(address, user, password, log)
                            
        if headVer == baseVer:
            FileUtil.log(log, work_copy + ": No SVN change found!")
            return False
            
        return True 
                    
    def update(self, work_copy, user, password, ver="HEAD", log=None):
        if not os.path.exists(work_copy):
            raise Exception(work_copy + " not exist")
        
        return process.run("svn update -r " + ver + " " + StrUtil.quote(work_copy) + self._get_svn_para(user, password), log=log)
        
    def revert(self, work_copy, user, password, log=None):
        if not os.path.exists(work_copy):
            raise Exception(work_copy + " not exist")
        
        return process.run("svn revert " + StrUtil.quote(work_copy) + self._get_svn_para(user, password), log=log)        