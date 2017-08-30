from datetime import datetime, timedelta
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from df_user.models import Passport

from df_user.tasks import register_success_send_mail  # 导入自定义发送函数类

# from django.conf import settings
# from django.core.mail import send_mail  # 导入发送邮件函数
# Create your views here.


@require_http_methods(['GET', 'POST'])
def register(request):
    """显示用户注册页面"""
    # 判断用户请求页面的方式
    if request.method == 'GET':
        # 显示用户注册页面
        return render(request, 'register.html')
    else:
        # 1.接收用户的注册信息
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        # 2.将用户的注册信息添加到数据库中
        Passport.objects.add_one_passport(username, password, email)
        # 3. 给注册用户的邮箱发邮件
        # msg = '<h1>欢迎您成为天天生鲜的注册会员</h1>请记好您的注册信息<br/>用户名：'+username + '<br/>密码：'+password
        # send_mail('欢迎信息', '', settings.EMAIL_FROM, [email, ], html_message=msg)
        register_success_send_mail.delay(username=username, password=password, email=email)
        # 跳转到登陆页面
        return redirect('/user/login/')


def login(request):
    """显示登陆页面"""
    # 1.获取cookie username的信息　request.COOKIES
    if 'username' in request.COOKIES:
        username = request.COOKIES['username']
    else:
        username = ''
    return render(request, 'login.html', {'username': username})


def login_check(request):
    """进行用户名登陆校验"""
    # 1.获取用户名和密码
    username = request.POST.get('username')
    password = request.POST.get('password')
    # 2. 根据用户名和密码查找账户信息
    passport = Passport.objects.get_one_passport(username=username, password=password)
    # 3.判断发挥只返回json数据
    if passport is None:
        # 用户名或密码错误
        return JsonResponse({'res': 0})
    else:
        # 用户名密码正确
        jres = JsonResponse({'res': 1})
        # 判断是否需要记住用户名
        remember = request.POST.get('remember')
        # print(type(remember))
        if remember == 'true':
            # 设置一个cookie 信息 username, 记住用户名
            jres.set_cookie('username', username, expires=datetime.now() + timedelta(days=14))
        return jres


def check_user_name_exist(request):
    """校验用户名是否存在"""
    # 1.接收用户名
    username = request.GET.get('username')
    # 2.根据用户名查找账户信息
    passport = Passport.objects.get_one_passport(username=username)
    # 3.判断返回值返回json数据
    if passport is None:
        # 用户名不存在，可以使用{'res':1}
        return JsonResponse({'res': 1})
    else:
        # 用户名已经注册{'res':0}
        return JsonResponse({'res': 0})

