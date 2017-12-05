#!/usr/bin/env python
# coding=utf-8

import sys
import glob
import os
import jenkins
from jinja2 import Template
from jinja2 import Environment, FileSystemLoader
from utils.logger import logger

# Capture our current directory
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
class Worker:

    def default_init(self, args=None, haru=None):
        result = glob.glob(r'*.xcworkspace')
        if len(result) == 0:
            print("没有找到xcworkspace文件!")
            print(haru.getJenkinsURL())
        elif len(result) == 1:
            workspace = result[0]
            jenkinsURL = haru.getJenkinsURL()
            jenkinsName = haru.getJenkinsUserName()
            jenkinsPassword = haru.getJenkinsPassword()
            value = input("请输入单测的target: ")
            project = input("请输入jenkins项目名称，默认为%s-UnitTest", value)
            if project == '':
                project = value + "-UnitTest"
            j2_env = Environment(loader=FileSystemLoader(THIS_DIR), trim_blocks=True)
            xmlconfig = j2_env.get_template('./template/default.xml').render(workspace=workspace, target=value)
            try:
                server = jenkins.Jenkins(jenkinsURL)
                server.create_job(project, xmlconfig)
                print("创建项目成功!")
            except Exception as e:
                print(e)
        else:
            print("There are more than one workspace.")

    def default_query(args):
        print(sys._getframe().f_code.co_name)

    def default_delete(args):
        print(sys._getframe().f_code.co_name)
    
    def default_update(args):
        print(sys._getframe().f_code.co_name)
