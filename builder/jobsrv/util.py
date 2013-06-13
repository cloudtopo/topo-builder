#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
进程相关函数封装
Copyright 2009 Cloudtopo
"""
import shutil,os


class StrUtil:
    #quote函数是在字符串前后加"，适用于调用shell命令时
    @staticmethod
    def quote(s):
        return '"'+s+'"'
    
    @staticmethod    
    def empty_str(s):
        return s is None or s ==''
       

class FileUtil:
    
    @staticmethod
    def copy_file_or_folder(src, dest):
        if not os.path.exists(src):
            return
            
        if os.path.isfile(src):
            shutil.copy(src, dest)
        else:    
            shutil.copytree(src,dest)
    
    @staticmethod
    def move_file_or_folder(src, dest):
        if not os.path.exists(src):
            return
        
        #必须保证dest不存在，这个move相当于rename    
        shutil.move(src, dest)
                        
    @staticmethod
    def del_tree(src):
        if not os.path.exists(src):
            return

        shutil.rmtree(src)
    
    @staticmethod
    def log(logfile, content, newline=False):
        if logfile is None:
            return
            
        flog= file(logfile, "ab")
        if newline:
            flog.write(content + "\r\n")
        else:
            flog.write(content)
            
        flog.close()
               