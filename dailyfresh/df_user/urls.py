# coding=utf-8
from django.conf.urls import url
# from df_user import views
from df_user import views

urlpatterns = [
    url(r'^register/$', views.register), # 显示用户注册页面
    # url(r'^register_handle/$', views.register_handle), # 进行用户注册
    url(r'^check_user_name_exist/$', views.check_user_name_exist),
    url(r'^login/$', views.login),
    url(r'^login_check/$', views.login_check),

]