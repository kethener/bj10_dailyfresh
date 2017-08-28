from celery import task
from django.conf import settings
from django.core.mail import send_mail
import time


@task
def register_success_send_mail(username, password, email):
    '''
    用户注册成功之后发送邮件
    '''
    msg = '<h1>欢迎您成为天天生鲜的注册会员</h1>请记好您的注册信息<br/>用户名：' + username + '<br/>密码：' + password
    send_mail('欢迎信息', '', settings.EMAIL_FROM, [email, ], html_message=msg)
    time.sleep(5)