
class UrlRecordMiddleware(object):
    '''
    url记录中间件
    '''
    # process_request(self, request) # 产生request对象之后，url匹配之前
    # process_view(self, request, view_func, *view_args, **view_kwargs) url匹配之后，视图函数调用之前
    exclude_path = ['/user/login/', '/user/login_check/', '/user/logout/',
                    '/user/register/', '/user/check_user_name_exist/']

    def process_view(self, request, view_func, *view_args, **view_kwargs):
        # 1.获取用户访问的url地址
        # print(request.path) url地址，不带参数
        # print(request.get_full_path()) url地址，带参数
        if request.path not in UrlRecordMiddleware.exclude_path:
            # 记录这个url地址
            request.session['pre_url_path'] = request.get_full_path() # /user/address/?a=3