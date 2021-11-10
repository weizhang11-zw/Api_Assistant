import unittest
from Api_Assistant.common.HTMLTestRunnerNew_util import HTMLTestRunner
from Api_Assistant.common import NowTime_util
from Api_Assistant.testcase import run_main
from Api_Assistant.common.SendEmail_util import Email
from Api_Assistant.common.configparam_util import ConfigEngine

"""执行测试套件"""
suite = unittest.TestSuite()

loader = unittest.TestLoader()


suite.addTest(loader.loadTestsFromModule(run_main))

filename = '../reports/' + NowTime_util.getNowtime() + 'report.html'

fp = open(filename, 'wb')
runner = HTMLTestRunner(
    stream=fp,
    title='接口自动化测试报告',
    description='接口自动化测试报告详细信息',
    verbosity=2
)

runner.run(suite)


"""发送邮件"""
ConfigEngine = ConfigEngine()
user = ConfigEngine.get_config('Email', 'user')
to = ConfigEngine.get_config('Email', 'to')
server = ConfigEngine.get_config('Email', 'server')
port = ConfigEngine.get_config('Email', 'port')
username = ConfigEngine.get_config('Email', 'username')
password = ConfigEngine.get_config('Email', 'password')
subject = ConfigEngine.get_config('Email', 'subject')

email_dict = {
    "user": user,
    "to": to,
    "server": server,
    'port': port,
    "username": username,
    "password": password,
    "subject": subject
}

sendmail = Email(email_dict).send_Email()








