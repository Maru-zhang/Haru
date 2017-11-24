#!/usr/bin/env python
# coding=utf-8

import sys
import logging
import argparse
import jenkins
import platform
import configparser
import pathlib
import os

from cli.worker import Worker

SCC_JENKINS_JOBS_TEST_STANDARD_CONFIG = '''
<?xml version='1.0' encoding='UTF-8'?>
<project>
  <actions/>
  <description></description>
  <keepDependencies>false</keepDependencies>
  <properties>
    <jenkins.model.BuildDiscarderProperty>
      <strategy class="hudson.tasks.LogRotator">
        <daysToKeep>2</daysToKeep>
        <numToKeep>10</numToKeep>
        <artifactDaysToKeep>-1</artifactDaysToKeep>
        <artifactNumToKeep>-1</artifactNumToKeep>
      </strategy>
    </jenkins.model.BuildDiscarderProperty>
  </properties>
  <scm class="hudson.plugins.git.GitSCM" plugin="git@3.3.0">
    <configVersion>2</configVersion>
    <userRemoteConfigs>
      <hudson.plugins.git.UserRemoteConfig>
        <url>http://git.souche.com/destiny/DSTAssistant</url>
        <credentialsId>df0a15e9-a200-4075-9954-06bce6b699a7</credentialsId>
      </hudson.plugins.git.UserRemoteConfig>
    </userRemoteConfigs>
    <branches>
      <hudson.plugins.git.BranchSpec>
        <name>*/postloan</name>
      </hudson.plugins.git.BranchSpec>
    </branches>
    <doGenerateSubmoduleConfigurations>false</doGenerateSubmoduleConfigurations>
    <submoduleCfg class="list"/>
    <extensions/>
  </scm>
  <assignedNode>mac-pro</assignedNode>
  <canRoam>false</canRoam>
  <disabled>false</disabled>
  <blockBuildWhenDownstreamBuilding>false</blockBuildWhenDownstreamBuilding>
  <blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding>
  <triggers>
    <hudson.triggers.SCMTrigger>
      <spec>H */2 * * *</spec>
      <ignorePostCommitHooks>false</ignorePostCommitHooks>
    </hudson.triggers.SCMTrigger>
  </triggers>
  <concurrentBuild>false</concurrentBuild>
  <builders>
    <hudson.tasks.Shell>
      <command>pod install
xcodebuild test -workspace DSTAssistant.xcworkspace -scheme DSTAssistant -destination &apos;platform=iOS Simulator,name=iPhone X,OS=11.0.1&apos; | /usr/local/bin/xcpretty -r junit</command>
    </hudson.tasks.Shell>
  </builders>
  <publishers>
    <hudson.tasks.junit.JUnitResultArchiver plugin="junit@1.20">
      <testResults>Build/reports/junit.xml</testResults>
      <keepLongStdio>false</keepLongStdio>
      <healthScaleFactor>1.0</healthScaleFactor>
      <allowEmptyResults>true</allowEmptyResults>
    </hudson.tasks.junit.JUnitResultArchiver>
  </publishers>
  <buildWrappers>
    <hudson.plugins.ws__cleanup.PreBuildCleanup plugin="ws-cleanup@0.33">
      <deleteDirs>false</deleteDirs>
      <cleanupParameter></cleanupParameter>
      <externalDelete></externalDelete>
    </hudson.plugins.ws__cleanup.PreBuildCleanup>
  </buildWrappers>
</project>
'''

SCC_WEILCOME_COPYWRITE = '''
❤️
Welcome to use Haru.
'''

logger = logging.getLogger()
config_path = os.getenv("HOME") + "/.config/haru/"
config_file_name = "config.ini"

def _default_init(self):
    print("init")

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
        query_action = subparser.add_parser('search', help='Query Unit Test CI Job.')
        query_action.set_defaults(func=self.worker.default_query)
        update_action = subparser.add_parser('update', help='Update Unit Test CI Job.')
        update_action.set_defaults(func=self.worker.default_update)
        delete_action = subparser.add_parser('delete', help='Delete Unit Test CI Job.')
        delete_action.set_defaults(func=self.worker.default_delete)
        
        # start parser
        self.args = self.parser.parse_args(args, namespace=self.worker)
        self.args.func(self.args)
        print(self.args)
        print(platform.system())
        print(vars(self.args))

    def check_config(self):
      # fuck windows
      if platform.system() == 'Windows':
        logger.error("sorry,not support Windows yet.")
        return
      # basic jenkins config
      self.guard_jenkins(key='url', message='please type in your jenkins url: ')
      self.guard_jenkins(key='name', message='please type in your ci user name: ')
      self.guard_jenkins(key='password', message='please type in your ci password: ')
      
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

    def prepare_load(self):
      # create config directory if not exit
      if not os.path.exists(config_path + config_file_name):
        os.makedirs(config_path, exist_ok=True)
        config = configparser.ConfigParser()
        config["default"] = {}
        config["jenkins"] = {}
        with open(config_path + config_file_name, 'w') as configfile:
          config.write(configfile)

    def load_local_config(self):

      # create config directory if not exit
      os.makedirs(config_path, exist_ok=True)

      config = configparser.ConfigParser()
      config["default"] = {}
      config["jenkins"] = {}
      


      

      
