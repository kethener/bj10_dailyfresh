from django.shortcuts import redirect

def login_required(view_func):
    '''
    用户登录判断装饰器
    '''
    def wrapper(request, *view_args, **view_kwargs):
        if request.session.has_key('is_login'):
            # 用户已登录
            return view_func(request, *view_args, **view_kwargs)
        else:
            # 用户未登录,跳转到登录页
            return redirect('/user/login/')
    return wrapper
