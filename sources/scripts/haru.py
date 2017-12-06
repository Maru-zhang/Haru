import click
import glob
import os
import jenkins
import platform
import configparser
import pathlib
import logging
from jinja2 import Template
from jinja2 import Environment, FileSystemLoader
from git import Repo
from git.exc import InvalidGitRepositoryError

SCC_WEILCOME_COPYWRITE = '''
❤️
Welcome to use Haru.
'''
# Capture our current directory
THIS_DIR = os.path.dirname(os.path.abspath(__file__))

config_path = os.getenv("HOME") + "/.config/haru/"
config_file_name = "config.ini"

logger = logging.getLogger()

click.echo(SCC_WEILCOME_COPYWRITE)

class Haru(object):
    
    def __init__(self):
        self.config = configparser.ConfigParser()

    # 获取jenkins的主机地址
    def getJenkinsURL(self):
      self._check_config()
      try:
        self.config.read(self.config_file_path()) 
        return self.config["jenkins"]["url"]
      except Exception as e:
        print("读取jenkins-url错误!")

    # 获取自己的jenkins的用户名
    def getJenkinsUserName(self):
      self._check_config()
      try:
        self.config.read(self.config_file_path()) 
        return self.config["jenkins"]["name"]
      except:
        print("读取jenkins-name错误!")

    # 获取自己的jenkins的密码
    def getJenkinsPassword(self):
      self._check_config()
      try:
        if self.config["jenkins"] is None:
          self.config.read(self.config_file_path())
        return self.config["jenkins"]["password"]
      except:
        print("读取jenkins-password错误!")

    def _check_config(self):
      # fuck windows
      if platform.system() == 'Windows':
        logger.error("sorry,not support Windows yet.")
        return
      # basic jenkins config
      self.guard_jenkins(key='url', message='please type in your jenkins url: ')
      self.guard_jenkins(key='name', message='please type in your jenkins user name: ')
      self.guard_jenkins(key='password', message='please type in your jenkins password: ')
      
    def config_file_path(self):
      return config_path + config_file_name

    def guard_jenkins(self, key, message):
      self.config.read(self.config_file_path())
      try:
        jenkins_url = self.config["jenkins"][key]
      except KeyError:
        value = input(message)
        config = configparser.ConfigParser()
        config.read(self.config_file_path())
        config['jenkins'][key] = value
        with open(self.config_file_path(), 'w') as configfile:
          config.write(configfile)

haru = Haru()

@click.group()
def cli():
    pass

@click.command()
def initjob():
        result = glob.glob(r'*.xcworkspace')
        if len(result) == 0:
            print("没有找到xcworkspace文件!")
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
                server = jenkins.Jenkins(jenkinsURL, username=jenkinsName, password=jenkinsPassword)
                user = server.get_whoami()
                version = server.get_version()
                print('Hello %s from Jenkins %s' % (user['fullName'], version))
                # server.create_job(project, xmlconfig)
                print("创建项目成功!")
            except Exception as e:
                print(e)
        else:
            print("There are more than one workspace.")

cli.add_command(initjob)

if __name__ == '__main__':
    cli()