# coding=utf-8
import time
from datetime import datetime,timedelta
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponseNotAllowed
from .models import Passport
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from df_user.tasks import register_success_send_mail
from django.views.decorators.http import require_POST,require_GET,require_http_methods
# Create your views here.

# def require_POST(view_func):
#     def wrapper(request, *args, **kwargs):
#         if request.method == 'GET':
#             return view_func(request, *args, **kwargs)
#         else:
#             return HttpResponseNotAllowed('not allowed')
#     return wrapper


@require_http_methods(['GET', 'POST'])
def register(request):
    '''
    显示用户注册页面
    '''
    if request.method == 'GET':
        # 显示用户注册页面
        return render(request, 'register.html')
    else:
        # 1.接收用户的注册信息
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')

        # 2.将用户的注册信息添加进数据库
        # msg = '欢迎您成为天天生鲜会员，祝您购物愉快'
        # send_mail('会员激活', '', settings.EMAIL_FROM, ['kethener@163.com'], html_message=msg)
        '''
        passport = Passport()
        passport.username = username
        passport.password = password
        passport.email = email
        # 添加进数据库
        passport.save()
        '''
        Passport.objects.add_one_passport(username=username, password=password, email=email)
        register_success_send_mail.delay(username=username, password=password, email=email)

        # 3.跳转到登录页面
        return redirect('/user/login/')


def check_user_name_exist(request):
    username = request.GET.get('username')
    passport = Passport.objects.get_one_passport(username=username)

    if passport is None:
        return JsonResponse({'res': 1})
    else:
        return JsonResponse({'res': 0})


@require_POST
def register_handle(request):
    '''
    进行用户注册
    '''
    # 1.接收用户的注册信息
    username = request.POST.get('user_name')
    password = request.POST.get('pwd')
    email = request.POST.get('email')
    # 2.将用户的注册信息添加进数据库
    passport = Passport()
    passport.username = username
    passport.password = password
    passport.email = email
    # 添加进数据库
    passport.save()
    # 3.跳转到登录页面
    return redirect('/user/login/')


def login(request):
    """显示登陆页面"""
    return render(request, 'login.html')


def login_check(request):
    '''
    进行用户登录校验
    '''
    # 1.获取用户名和密码
    username = request.POST.get('username')
    password = request.POST.get('password')
    # 2.根据用户名和密码查找账户信息
    passport = Passport.objects.get_one_passport(username=username, password=password)
    # 3.判断返回值返回json数据
    if passport is None:
        # 用户名或密码错误
        return JsonResponse({'res': 0})
    else:
        # 用户名密码正确
        jres = JsonResponse({'res': 1})
        # 判断是否需要记住用户名
        remember = request.POST.get("remember")
        #print(type(remember))
        if remember == 'true':
            # 设置一个cookie信息username,记住用户名
            jres.set_cookie('username', username, expires=datetime.now()+timedelta(days=14))
        return jres#HttpResponse

