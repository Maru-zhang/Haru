import click
import glob
import os
import jenkins
import platform
import configparser
import logging
from jinja2 import Template
from jinja2 import Environment, FileSystemLoader
from git import Repo
from git.exc import InvalidGitRepositoryError

SCC_WEILCOME_COPYWRITE = '''
❤️❤️❤️❤️❤️❤️❤️❤️❤️️❤️❤️❤️️❤️❤️❤️❤️❤️❤️❤️❤️❤️️❤️❤️❤️️
Welcome to use Haru.
❤️❤️❤️❤️❤️❤️❤️❤️❤️️❤️❤️❤️️❤️❤️❤️❤️❤️❤️❤️❤️❤️️❤️❤️❤️️
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

    def server(self):
        jenkinsURL = haru.getJenkinsURL()
        jenkinsName = haru.getJenkinsUserName()
        jenkinsPassword = haru.getJenkinsPassword()
        server = jenkins.Jenkins(jenkinsURL, username=jenkinsName, password=jenkinsPassword)
        return server

    # 获取jenkins的主机地址
    def getJenkinsURL(self):
        self._check_config()
        try:
            self.config.read(self.config_file_path()) 
            return self.config["jenkins"]["url"]
        except:
            logger.error("读取jenkins-url错误!")

    # 获取自己的jenkins的用户名
    def getJenkinsUserName(self):
        self._check_config()
        try:
            self.config.read(self.config_file_path()) 
            return self.config["jenkins"]["name"]
        except:
            logger.error("读取jenkins-name错误!")

    # 获取自己的jenkins的密码
    def getJenkinsPassword(self):
        self._check_config()
        try:
            if self.config["jenkins"] is None:
                self.config.read(self.config_file_path())
            return self.config["jenkins"]["password"]
        except:
            logger.error("读取jenkins-password错误!")

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
            self.config["jenkins"][key]
        except KeyError:
            value = input(message)
            config = configparser.ConfigParser()
            config.read(self.config_file_path())
            config['jenkins'][key] = value
            with open(self.config_file_path(), 'w') as configfile:
                config.write(configfile)

def loginable(func):
    def wrapper(*args, **kw):
        jenkinsURL = haru.getJenkinsURL()
        jenkinsName = haru.getJenkinsUserName()
        jenkinsPassword = haru.getJenkinsPassword()
        server = jenkins.Jenkins(jenkinsURL, username=jenkinsName, password=jenkinsPassword)
        return func(*args, **kw)
    return wrapper

haru = Haru()

@click.group()
def cli():
    pass

@click.command()
def init():
    result = glob.glob(r'*.xcworkspace')
    if len(result) == 0:
        logger.error("没有找到xcworkspace文件!")
    elif len(result) == 1:
        workspace = result[0]
        try:
            git_url = Repo(".").remotes.origin.url
        except InvalidGitRepositoryError as e:
            git_url = input('没有在当前目录找到Git,请输入项目的远程Git地址: ')
        value = input("请输入单测的target: ")
        if not value:
            logger.error("项目名称不能为空")
            return
        project = input("请输入jenkins项目名称，默认名称为" + value + "-UnitTest: ")
        if project == '':
            project = value + "-UnitTest"
        try:
            j2_env = Environment(loader=FileSystemLoader(THIS_DIR), trim_blocks=True)
            xmlconfig = j2_env.get_template('./template/default.xml').render(
            gitremote=git_url,
            workspace=workspace, 
            target=value,
            branch="master")
            server = haru.server()
            server.create_job(project, xmlconfig)
            logger.info("创建项目成功!")
        except Exception as e:
            logger.error(e)
    else:
        logger.error("There are more than one workspace.")

@click.command()
@click.argument('jobname')
def build(jobname):
    try:
        branch = click.prompt('请输入你所要构建的分支', type=str)
        email = click.prompt('请输入构建完成之后所需要通知的邮箱: ', type=str)
        if not branch:
            branch = "master"
        server = haru.server()
        server.build_job(jobname, {"branch": branch, "observer": email})
        click.echo(jobname + '已经开始构建!')
    except Exception as e:
        logger.error(e)

@click.command()
@click.argument('jobname')
def delete(jobname):
    try:
        server = haru.server()
        server.delete_job(jobname)
        click.echo(jobname + '已经成功删除!')
    except Exception as e:
        logger.error(e)

@click.command()
@click.argument('job')
@click.option('--number', default="", help='构建号码, 默认为最新的构建号码')
def fetch(job, number):
    try:
        server = haru.server()
        last_build_number = number
        if not number:
            last_build_number = server.get_job_info(job)['lastCompletedBuild']['number']
        console = server.get_build_console_output(job, number=last_build_number)
        click.echo(console)
    except Exception as e:
        click.echo(e)
      

cli.add_command(init)
cli.add_command(build)
cli.add_command(fetch)
cli.add_command(delete)

if __name__ == '__main__':
    cli()
