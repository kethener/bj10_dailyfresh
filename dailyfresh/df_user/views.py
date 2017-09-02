from django.shortcuts import render,redirect
from django.http import HttpResponseNotAllowed, JsonResponse
# from django.core.mail import send_mail # 导入发送邮件函数
# from django.conf import settings
from df_user.models import Passport,Address
from django.views.decorators.http import require_POST, require_GET,require_http_methods
from df_user.tasks import register_success_send_mail  # 导入发送邮件任务函数
from utils.decorators import login_required  # 导入用户登录判断装饰器函数
from datetime import datetime, timedelta

# import time

# Create your views here.

# def require_POST(view_func):
#     def wrapper(request, *args, **kwargs):
#         if request.method == 'GET':
#             return view_func(request, *args, **kwargs)
#         else:
#             return HttpResponseNotAllowed('not allowed')
#     return wrapper

# =====================================注册=============================================


@require_http_methods(['GET', 'POST'])
def register(request):
    """显示用户注册页面"""
    if request.method == 'GET':
        # 显示用户注册页面
        return render(request, 'register.html')
    else:
        # 1.接收用户的注册信息
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        # 2.将用户的注册信息添加进数据库
        Passport.objects.add_one_passport(username=username, password=password, email=email)
        # 3.给注册用户的邮箱发邮件 smtp
        # msg = '<h1>欢迎您成为天天生鲜的注册会员</h1>请记好您的注册信息<br/>用户名：'+username + '<br/>密码：'+password
        # send_mail('欢迎信息', '', settings.EMAIL_FROM, [email,], html_message=msg)
        # time.sleep(5)
        register_success_send_mail.delay(username=username,password=password, email=email)
        # 4.跳转到登录页面
        return redirect('/user/login/')


def check_user_name_exist(request):
    """
    校验用户名是否存在
    """
    # 1.接收用户名
    username = request.GET.get('username')
    # 2.根据用户名查找账户信息
    passport = Passport.objects.get_one_passport(username=username)
    # 3.判断返回值返回json数据
    if passport is None:
        # 用户名可用 {'res':1}
        return JsonResponse({'res': 1})
    else:
        # 用户名已注册 {'res':0}
        return JsonResponse({'res': 0})


@require_POST
def register_handle(request):
    """
    进行用户注册
    """
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

# =====================================登录=============================================


# /user/login/
def login(request):
    """
    显示登录页面
    """
    # 1.获取cookie username的信息 request.COOKIES
    if 'username' in request.COOKIES:
        username = request.COOKIES['username']
    else:
        username = ''
    return render(request, 'login.html', {'username':username})


def login_check(request):
    """
    进行用户登录校验
    """
    # 1.获取用户名和密码
    username = request.POST.get('username')
    password = request.POST.get('password')
    # 2.根据用户名和密码查找账户信息
    passport = Passport.objects.get_one_passport(username=username, password=password)
    # 3.判断返回值返回json数据
    if passport is None:
        # 用户名或密码错误
        return JsonResponse({'res':0})
    else:
        # 用户名密码正确
        # 获取用户之前访问的url地址
        # if request.session.has_key('pre_url_path'):
        #     next = request.session.get('pre_url_path')
        # else:
        #     next = '/' # 默认跳转到首页
        next = request.session.get('pre_url_path', '/')
        jres = JsonResponse({'res': 1, 'next': next})
        # 判断是否需要记住用户名
        remember = request.POST.get("remember")
        # print(type(remember))
        if remember == 'true':
            # 设置一个cookie信息username,记住用户名
            jres.set_cookie('username', username, expires=datetime.now()+timedelta(days=14))
        # 记住用户的登录状态
        request.session['is_login'] = True
        request.session['passport_id'] = passport.id
        request.session['username'] = username

        return jres  # HttpResponse


def logout(request):
    """
    退出登录
    """
    # 清空登录用户的session信息
    request.session.flush()
    # 跳转到首页
    return redirect('/')


# /user/address/
@require_http_methods(['GET','POST'])
@login_required
def address(request):
    """
    用户中心-地址页
    """
    passport_id = request.session.get('passport_id')
    if request.method == 'GET':
        # 显示用户中心地址页面
        # 1.查询用户的默认收货地址信息
        addr = Address.objects.get_default_address(passport_id=passport_id)
        return render(request, 'user_center_site.html', {'addr':addr, 'page':'addr'}) # request
    else:
        # 添加一个收货地址
        # 0.获取登录用户的id
        # 1.接收用户的收件地址信息
        recipient_name = request.POST.get('uname')
        recipient_addr = request.POST.get('addr')
        recipient_phone = request.POST.get('phone')
        zip_code = request.POST.get('zip_code')
        # 2.添加收货地址信息
        Address.objects.add_one_address(passport_id=passport_id, recipient_name=recipient_name,
                                        recipient_addr=recipient_addr, recipient_phone=recipient_phone,
                                        zip_code=zip_code)
        # 3.查询用户的默认收货地址信息
        addr = Address.objects.get_default_address(passport_id=passport_id)
        # 4.刷新地址页面
        return render(request, 'user_center_site.html', {'addr':addr, 'page':'addr'})


# /user/
@login_required
def user(request):
    """
    用户中心－个人信息页
    """
    # 0.获取登录账户id
    passport_id = request.session.get('passport_id')
    # 1.查收用户的默认收货地址
    addr = Address.objects.get_default_address(passport_id=passport_id)
    return render(request, 'user_center_info.html', {'addr': addr, 'page':'user'})


# /user/order/
@login_required
def order(request):
    """
    用户中心-订单页
    """
    return render(request, 'user_center_order.html', {'page': 'order'})


# def test(request):
#     return render(request, 'index1.html')




























