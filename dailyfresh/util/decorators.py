from django.shortcuts import redirect


def login_required(view_func):
    """用户登陆判断装饰器"""
    def wrapper(request, *view_args, **view_kwargs):
        if request.session.has_key('is_login'):
            # 用户已经登陆
            return view_func(request, *view_args, **view_kwargs)
        else:
            # 用户名登陆，跳转到登陆页面
            return redirect('/user/login/')
    return wrapper


