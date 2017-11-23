import sys
from cli.haru import Haru
import jenkins

if __name__ == '__main__':
    argv = sys.argv[1:]
    haru = Haru(argv)

    # server = jenkins.Jenkins('http://jenkins.souche-inc.com/', username='maru', password='86880362')
    # user = server.get_whoami()
    # version = server.get_version()
    # print('Hello %s from Jenkins %s' % (user['fullName'], version))
    # print('My jobs count is %s', server.jobs_count())
    # plugins = server.get_plugins_info()
    # print('%s', server.get_info)
    # print('My plugins is %s', plugins)
    # server.create_job('auto-test', jenkins.EMPTY_CONFIG_XML)
    # config = server.get_job_config("弹个车单元测试")
    # print(config)