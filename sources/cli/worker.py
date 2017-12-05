#!/usr/bin/env python
# coding=utf-8

import sys
import glob
import os
import jenkins
from jinja2 import Template
from jinja2 import Environment, FileSystemLoader
from utils.logger import logger
from git import Repo
from git.exc import InvalidGitRepositoryError

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
            try:
                git_url = Repo(".").remotes.origin.url
            except InvalidGitRepositoryError as e:
                git_url = input('没有在当前目录找到Git,请输入项目的远程Git地址: ')
            value = input("请输入单测的target: ")
            if not value:
                print("项目名称不能为空")
                return
            project = input("请输入jenkins项目名称，默认名称为" + value + "-UnitTest: ")
            if project == '':
                project = value + "-UnitTest"
            try:
                j2_env = Environment(loader=FileSystemLoader(THIS_DIR), trim_blocks=True)
                xmlconfig = j2_env.get_template('./template/default.xml').render(
                gitremote=git_url,
                workspace=workspace, 
                target=value)
                server = jenkins.Jenkins(jenkinsURL, username="maru", password="86880362")
                user = server.get_whoami()
                version = server.get_version()
                print('Hello %s from Jenkins %s' % (user['fullName'], version))
                server.create_job(project, xmlconfig)
                print("创建项目成功!")
            except Exception as e:
                print(e)
        else:
            print("There are more than one workspace.")

    def default_query(self, args=None, haru=None):
        print(sys._getframe().f_code.co_name)

    def default_delete(self, args=None, haru=None):
        server = jenkins.Jenkins("http://jenkins.souche-inc.com/", username="maru", password="86880362")
        server.delete_job("-UnitTest")
        print(sys._getframe().f_code.co_name)
    
    def default_update(args):
        print(sys._getframe().f_code.co_name)
