#!/usr/bin/env python
# coding=utf-8

import sys
import argparse
import jenkins
import platform
import configparser
import pathlib
import os

from cli.worker import Worker
from utils.logger import logger

SCC_WEILCOME_COPYWRITE = '''
❤️
Welcome to use Haru.
'''

config_path = os.getenv("HOME") + "/.config/haru/"
config_file_name = "config.ini"

class Haru(object):
    
    def __init__(self, args=None, **kwargs):
        # setup safe args
        if args is None:
            args = []

        # setup property
        self.parser = argparse.ArgumentParser(description=SCC_WEILCOME_COPYWRITE)
        self.config = configparser.ConfigParser()
        self.worker = Worker()
        subparser = self.parser.add_subparsers(help='describe')

        # setup sub-commands
        init_action = subparser.add_parser('init', help='Initialize Unit Test CI Job.')
        init_action.set_defaults(func=self.worker.default_init)
        init_action.add_argument('--local', help='add local config file')
        query_action = subparser.add_parser('search', help='Query Unit Test CI Job.')
        query_action.set_defaults(func=self.worker.default_query)
        update_action = subparser.add_parser('update', help='Update Unit Test CI Job.')
        update_action.set_defaults(func=self.worker.default_update)
        delete_action = subparser.add_parser('delete', help='Delete Unit Test CI Job.')
        delete_action.set_defaults(func=self.worker.default_delete)
        
        # start parser
        self.args = self.parser.parse_args(args, namespace=self.worker)
        self.args.func(self.args, self)

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