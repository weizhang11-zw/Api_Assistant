import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from Api_Assistant.common.NowTime_util import getNowtime


class Email(object):
    """
    发送邮件
    """

    def __init__(self, email_info):

        self.now_date = getNowtime()

        self.email_info = email_info

        self.Email_SMTP = smtplib.SMTP_SSL(self.email_info['server'], self.email_info['port'])

        self.user_from = ''

    def login_Email(self):

        self.user_from = self.email_info['user']
        login_email = self.Email_SMTP.login(self.email_info['user'], self.email_info['password'])
        return login_email

    def send_Email(self):

        msg = MIMEMultipart()

        filePath = self.get_report()
        report_file = open(filePath, 'rb').read()
        att = MIMEText(report_file, 'base64', 'utf-8')
        att["Content-Type"] = 'application/octet-stream'
        att["Content-Disposition"] = 'attachment; filename="API_report.html"'

        msg.attach(att)

        msg['From'] = self.email_info['user']
        msg['To'] = self.email_info['to']
        msg['Subject'] = self.email_info['subject']

        contents = MIMEText(report_file, 'html', 'utf-8')

        msg.attach(contents)

        try:
            self.login_Email()
            self.Email_SMTP.sendmail(self.user_from, self.email_info['to'].split(','), msg.as_string())
            print('邮件发送成功，请注意查收！'.center(30, '#'))
        except Exception as e:
            print('邮件发送失败：', e)

    @staticmethod
    def get_report(reports_path=r"../reports/"):

        lists = os.listdir(reports_path)
        lists.sort(key=lambda fn: os.path.getmtime(reports_path + "/" + fn))
        file_new = os.path.join(reports_path, lists[-1])
        return file_new

    def close(self):

        self.Email_SMTP.quit()
        print('logout'.center(30, '#'))
