import sys
import logging
import argparse

logger = logging.getLogger()

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

class Haru(object):
    
    def __init__(self, args=None, **kwargs):
        
        # setup safe args
        if args is None:
            args = []

        # setup property
        self.parser = argparse.ArgumentParser(description=SCC_WEILCOME_COPYWRITE)
        subparser = self.parser.add_subparsers(help='sub-command help')

        # setup sub-commands
        init_action = subparser.add_parser('init', help='Unit Test CI Initialize Help')
        query_action = subparser.add_parser('search', help='Unit Test CI Query Help')
        update_action = subparser.add_parser('update', help='Unit Test CI Update Help')
        delte_action = subparser.add_parser('delete', help='Unit Test CI Delete Help')
        
        # start parser
        self.args = self.parser.parse_args(args)
        print(self.args)