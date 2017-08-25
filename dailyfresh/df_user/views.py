# coding=utf-8
from django.shortcuts import render, redirect
from django.http import HttpResponseNotAllowed
from df_user.models import Passport
from django.views.decorators.http import require_POST, require_GET,require_http_methods
# Create your views here.

'''
制作装饰器
def require_POST(view_func):
    def wrapper(request, *args, **kwargs):
        if request.method == 'GET':
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseNotAllowed('not allowed')
    return wrapper
'''


@require_http_methods(['GET', 'POST'])
def register(request):
    """显示和注册页面"""
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')

        Passport.objects.add_one_passport(username=username, password=password, email=email)
        return render(request, '/user/login/')


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

